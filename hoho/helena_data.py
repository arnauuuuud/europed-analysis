from pylib.misc import ReadFile, BatchRun
import subprocess
import shutil
import numpy as np
import time
import sys
import os

# ======================================================================== #
#                                                                          #
#                          HELENA Data class                               #
#                                                                          #
# ======================================================================== #

# HELENA manual
# https://www.differ.nl/sites/default/files/attachments/biblio/RR96-228.pdf

class HelenaData:
    def __init__(self, output_path = None, mapping_path = None):
        
        #------------------------#
        #  Reading mapping data  #
        #------------------------#
        if mapping_path is not None:
            if r'/' not in mapping_path:
                mapping_path = os.environ['HELENA_DIR'] + "mapping/" + mapping_path

            # Unzipping if the file is gziped
            gunziped = False
            if not os.path.exists(mapping_path):
                if os.path.exists(f'{mapping_path}.gz'):
                    os.system(f'gunzip {mapping_path}.gz')
                    gunziped = True
                else:
                    raise Exception(f'{mapping_path} does not exist')
            
            with ReadFile(mapping_path) as f:
                self.js0 = f.readword(int)
                npsi = self.js0 + 1

                # Reading sqrt(psi) that HELENA has used (0-1)
                self.csh = f.readwords(npsi, float)

                # Reading q profile
                self.qs = f.readwords(npsi, float)

                # Reading qprime profile
                self.qprime0 = f.readword(float)
                self.qprime1 = f.readword(float)
                self.qprimes = f.readwords(npsi-1, float)

                # Reading current data !!!NOT USED in HELENA manual!!!
                self.vectorj = f.readwords(npsi, float)
                self.jprime0 = f.readword(float)
                self.jprime1 = f.readword(float)

                # # Skipping unimportant data
                # f.readwords(3+2*npsi, float) #TODO: find out what it is and store it

                # Reading chi data (stored later)
                nchi = f.readword(int)
                self.nchi = nchi
                if nchi % 2 == 0:
                    ias = 1
                    nch2 = nchi + 1
                else:
                    ias = 0
                    nch2 = 2*(nchi-1) + 1    

                chi = np.zeros(nch2)
                chi[:nchi] = f.readwords(nchi, float)

                # Reading matrixes (stored later)
                GEM11 = np.zeros([nch2,npsi])    #GEM11 = grad(psi)^2 i.e. g^11
                GEM11[0:nchi,1:npsi] = f.readwords((nchi,npsi-1), float)

                GEM12 = np.zeros([nch2,npsi])    #GEM12 = grad(psi).grad(theta) i.e. g^12
                GEM12[0:nchi,1:npsi] = f.readwords((nchi, npsi-1), float)

                self.cpsurf = f.readword(float)
                self.radius = f.readword(float)

                GEM33 = np.zeros([nch2,npsi])    #GEM33 = R^2 i.e. g_33
                GEM33[0:nchi,1:npsi] = f.readwords((nchi, npsi-1), float)

                # Reading R on magnetic axis
                self.raxis = f.readword(float)
                
                # Reading pressure profile
                self.pressure = f.readwords(npsi, float)
                f.readwords(2,float) #skipping unimportant data

                # Reading F ??? (Some scaling factor for CASTOR but not MISHKA)
                self.F = f.readwords(npsi, float)
                f.readwords(2, float) #skipping unimportant data TODO: find out what and store it

                # Reading VX and VY ???
                self.VX = f.readwords(nchi, float)
                self.VY = f.readwords(nchi, float)
                
                # Reading inverse aspect ratio
                self.eps = f.readword(float)

                # Reading real world coordinates XX = R, YY = Z (stored later)
                XX = np.zeros([nch2,npsi])
                XX[0:nchi,1:npsi] = f.readwords((nchi, npsi-1), float)

                YY = np.zeros([nch2,npsi])
                YY[0:nchi,1:npsi] = f.readwords((nchi, npsi-1), float)

            # Calculating derived quantities
            if ias == 1:
                # Setting values for assymetric equilibrium
                GEM11[nch2-1,:] = GEM11[0,:]
                GEM12[nch2-1,:] = GEM12[0,:]
                GEM33[nch2-1,:] = GEM33[0,:]
                XX[nch2-1,:] = XX[0,:]
                YY[nch2-1,:] = YY[0,:]
                chi[nch2-1] = 2 * np.pi
            else:
                # Setting values for symmetric equilibrium
                GEM11[nchi:nch2,:] = GEM11[nchi-2::-1,:]
                GEM12[nchi:nch2,:] = GEM12[nchi-2::-1,:]
                GEM33[nchi:nch2,:] = GEM33[nchi-2::-1,:]
                XX[nchi:nch2,:] = XX[nchi-2::-1,:]
                YY[nchi:nch2,:] = YY[nchi-2::-1,:]
                chi[nchi:nch2] = 2 * np.pi - chi[nchi-2::-1,:]   
            
            # Storing data
            self.GEM11 = GEM11
            self.GEM12 = GEM12
            self.GEM33 = GEM33
            self.XX = XX
            self.YY = YY
            self.chi = chi
            
            # Calculating GEM22
            nchi = nch2
            J = np.zeros(npsi)
            GEM22 = np.zeros([nch2,npsi])
            for i in range(nchi):
                J[1:npsi] = self.qs[1:npsi] * GEM33[i,1:npsi] / self.F[1:npsi]
                GEM22[i,1:npsi] = (GEM33[i,1:npsi] / GEM11[i,1:npsi]) \
                / (J[1:npsi] * J[1:npsi] + GEM12[i,1:npsi] * GEM12[i,1:npsi])
            
            self.GEM22 = GEM22

            # Calculating GEM22
            nchi = nch2
            J = np.zeros(npsi)
            newGEM22 = np.zeros([nch2,npsi])
            for i in range(nchi):
                newGEM22[i,1:npsi] = (GEM33[i,1:npsi] * GEM11[i,1:npsi]) - GEM12[i,1:npsi] * GEM12[i,1:npsi]

            self.test2 = 'aaaaaaa'            
            self.lolo = newGEM22

            if gunziped:
                os.system(f'gzip {mapping_path}')
        
        #------------------------#
        #  Reading output data   #
        #------------------------#
        if output_path is not None:
            if '/' not in output_path:
                output_path = os.environ['HELENA_DIR'] + 'output/' + output_path

            with open(output_path) as f:
                line = f.readline()
                while '* I, FLUX,  RHO,   Q,    SHEAR,   SHEAR1, ALPHA,  ALPHA1,  FMARG,  BALLOONING *' not in line:
                    line = f.readline()
                f.readline()

                psi_eq = []
                q_eq = []

                spl = f.readline().split()
                while len(spl) == 10:
                    psi_eq.append(float(spl[1]))
                    q_eq.append(float(spl[3]))
                    spl = f.readline().split()
                
                self.eq_q = q_eq
                self.eq_psi = psi_eq
                
                line = f.readline()
                while 'REAL WORLD OUTPUT' not in line:
                    line = f.readline()
                f.readline()
                self.r = float(f.readline().split()[-2])
                self.b0 = float(f.readline().split()[-2])
                self.ip = float(f.readline().split()[-2])
                self.a = float(f.readline().split()[-2])
                self.psib = float(f.readline().split()[-2])
                self.n0 = float(f.readline().split()[-3]) * 1e19
                self.zeff = float(f.readline().split()[-1])
                self.te_frac = float(f.readline().split()[-1])

                

                while 'S,   P [Pa], Ne [10^19m^-3], Te [eV],  Ti [eV],' not in line:
                    line = f.readline()
                f.readline()

                s = []
                p = []
                ne = []
                te = []
                ti = []

                spl = f.readline().split()
                while len(spl) == 10:
                    s.append(float(spl[0]))
                    p.append(float(spl[1]))
                    ne.append(float(spl[2]))
                    te.append(float(spl[3]))
                    ti.append(float(spl[4]))
                    spl = f.readline().split()

                self.s = np.array(s)
                self.p = np.array(p)
                self.ne = np.array(ne)
                self.te = np.array(te)
                self.ti = np.array(ti)
                
                while "*   S,     AVERAGE JPHI,   CIRCUMFRENCE *" not in line:
                    line = f.readline()
                f.readline()
                s_jphi = []
                jphi = []

                spl = f.readline().split()
                while len(spl) == 3:
                    s_jphi.append(float(spl[0]))
                    jphi.append(float(spl[1]))
                    spl = f.readline().split()
                self.s_jphi = s_jphi
                self.jphi = jphi
                
                while 'SIG(Spitz)' not in line:
                    line = f.readline()
                f.readline()
                
                q = []
                spitzer = []
                neo = []

                spl = f.readline().split()
                while len(spl) == 7:
                    q.append(float(spl[1]))
                    spitzer.append(float(spl[5]))
                    neo.append(float(spl[6]))
                    spl = f.readline().split()
                
                self.eta_spitz = np.array(spitzer)
                self.eta_neo = np.array(neo)

                

    def write_eqdsk(self, filepath):
        pass
        # #-*-Python-*-
        # # Created by saarelma at 27 Nov 2019  14:35
        # """
        # This script uses the mapping file to fill the eqdsk grid
        # """
        
        # if '/' not in filepath:
        #     filepath = os.environ['HELENA_DIR'] + 'geqdsk/' + filepath

        # psigrid = np.tile(self.mapping['csh']**2 - self.mapping['csh'][-1]**2,(self.mapping['nchi'],1)).transpose()

        # psiflat = psigrid.flatten()
        # rflat = self.mapping['XX'].flatten()
        # zflat = self.mapping['YY'].flatten()

        # minr = min(rflat) - 0.1         #Why added 0.1?
        # maxr = max(rflat) + 0.1
        # minz = min(zflat)
        # maxz = max(zflat)
        # if maxz > -minz :
        #     maxz += 0.1
        #     minz = -maxz
        # else:
        #     minz -= 0.1
        #     maxz = -minz

        # rgrid,zgrid = np.mgrid[minr:maxr:complex(0,root['OUTPUTS']['gEQDSK']['NW']),minz:maxz:complex(0,root['OUTPUTS']['gEQDSK']['NH'])]

        # psigrid = griddata((rflat,zflat),psiflat,(rgrid,zgrid),method = 'cubic',fill_value = 0.0) #,fill_value = mapping['1d']['psi']['data'][-1])

        # rcentr = self.mapping['XX'][0,0]
        # zcentr = self.mapping['YY'][0,0]
        # psidif = self.mapping['csh'][-1]**2 - self.mapping['csh'][0]**2

        # theta = np.arctan2(self.mapping['YY'][-1,:] - zcentr, self.mapping['XX'][-1,:] - rcentr)
        # for i in range(len(theta)):
        #     if theta[i] < 0 and i > 0:
        #         theta[i] += 2 * np.pi
        # theta[-1] = 2 * np.pi

        # radbnd = np.sqrt((self.mapping['XX'][-1,:]-rcentr) ** 2 + (self.mapping['YY'][-1,:]-zcentr) ** 2)
        # radspl = interp1d(theta, radbnd, 'cubic')

        # for i in range(np.size(rgrid,0)):
        #     for j in range(np.size(zgrid,1)):
        #         if psigrid[i,j] == 0.0 :
        #             th =  np.arctan2(zgri/d[0,j] - zcentr, rgrid[i,0] - rcentr)
        #             if th < 0:
        #                 th += 2 * np.pi
        #             rad = np.sqrt((rgrid[i,0]-rcentr) ** 2 + (zgrid[0,j]-zcentr) ** 2)
        #             psigrid[i,j] = (rad/radspl(th) - 1.0) * psidif

        # #Do not know what this is or does
        # argminr = np.argmin(root['OUTPUTS']['gEQDSK']['RBBBS'])
        # if argminr > 1:
        #     rb_new=root['OUTPUTS']['gEQDSK']['RBBBS'][argminr::-1]
        #     rb_new=append(rb_new,root['OUTPUTS']['gEQDSK']['RBBBS'][:argminr:-1])
        #     zb_new=root['OUTPUTS']['gEQDSK']['ZBBBS'][argminr::-1]
        #     zb_new=append(zb_new,root['OUTPUTS']['gEQDSK']['ZBBBS'][:argminr:-1])
        #     root['OUTPUTS']['gEQDSK']['RBBBS']=rb_new
        #     root['OUTPUTS']['gEQDSK']['ZBBBS']=zb_new

        # root['OUTPUTS']['gEQDSK']['PSIRZ'] = psigrid.transpose()
        # root['OUTPUTS']['gEQDSK']['RDIM'] = maxr-minr
        # root['OUTPUTS']['gEQDSK']['ZDIM'] = maxz-minz
        # root['OUTPUTS']['gEQDSK']['RLEFT'] = minr
        # root['OUTPUTS']['gEQDSK']['ZMID'] = (maxz + minz) / 2.0
        # root['OUTPUTS']['gEQDSK']['SIBRY'] = 0.0 #mapping['1d']['psi']['data'][-1]
        # root['OUTPUTS']['gEQDSK']['SIMAG'] = -self.mapping['csh'][-1]**2

        # root['OUTPUTS']['gEQDSK'].save()
        # root['OUTPUTS']['gEQDSK'].load(raw=True, add_aux=False)


        # CS=contourPaths(rgrid[:,0],zgrid[0,:],psigrid.T,[0.01])
        # vert=CS[0][0].vertices

        # rlim=vert[:,0]
        # zlim=vert[:,1]

        # root['OUTPUTS']['gEQDSK']['RLIM']=rlim
        # root['OUTPUTS']['gEQDSK']['ZLIM']=zlim
        # root['OUTPUTS']['gEQDSK']['LIMITR']=len(zlim)
        # root['OUTPUTS']['gEQDSK']['RVTOR']=root['OUTPUTS']['gEQDSK']['RCENTR']
        # root['OUTPUTS']['gEQDSK']['KVTOR']=0
        # root['OUTPUTS']['gEQDSK']['NMASS']=0

# ======================================================================== #

def create_eqdsk_chease(namelist):
    """ Runs helena and then CHEASE to produce an eqdsk for a given HELENA equilibrium"""
    # Assumes:
    # A directoty called "geqdsk" has been created under the
    # HELENA directory
    # Chease namelist file in /home/hnystrom/work/templates/
    # Have access to Samuli's CHEASE binary
    # "runhel.py" is in the top level of HELENA_DIR environment variable
    # If running on Heimdall, you have added :" export LIBRARY_PATH=$LD_LIBRARY_PATH":/usr/local/depot/hdf5-1.8.19-ifort12/lib":/usr/local/depot/INTEL/intel/lib/intel64/'" to your .bashrc file
    # find and edit the helena namelist for use with CHEASE
    def edit_helena_nml(namelist):
        if '/' not in namelist:
            namelist = os.environ['HELENA_DIR'] + 'namelist/' + namelist

        output = []
        try:
            ifile = open(namelist,'r')
        except IOError:
            sys.exit("Helena namelist does not exist. Aborting.")
        lines = ifile.readlines()
        set_npr2 = True
        for line in lines:
            if 'NPR2' in line.upper():
                set_npr2 = False
        nlines = len(lines)
        del lines
        ifile.close()
        ifile = open(namelist,'r')

        if set_npr2:
            npr1count = 0
            for _ in range(0, nlines):
                line = ifile.readline()
                output.append(line)
                if (("NPR1" in line) and (npr1count==0)): 
                    output.append("NPR2=1, \n")
                    npr1count = 1
                elif (("npr1" in line) and (npr1count==0)): 
                    output.append("   npr2 = 1\n")
                    npr1count = 1
            ifile.close()

            ofile = open(namelist+'_new','w') #note this is overwritten!
            for line in output:
                ofile.write(line)
            ofile.close()
            return namelist.split('/')[-1]+'_new'
        else:
            return namelist.split('/')[-1]

    def runhel_eqdsk(namelist):
        cwd = os.getcwd()
        os.chdir(os.environ['HELENA_DIR']) # this is where my "runhel.py" is located
        subprocess.call(['python', 'runhel.py', '-eqdsk', namelist], stdout=open(os.devnull,'w'))
        os.chdir(cwd)
        return # Subprocess might require full path to runhel.py 

    def run_chease(eqdsk_name, chease_nml, chease_run):
        eqdskfname = os.environ['HELENA_DIR'] + 'geqdsk/' + eqdsk_name + '.gz'
        cwd = os.getcwd()

        print("cwd: ", cwd)	
        print("Will try to open this eqdsk file: %s"%eqdskfname)
        try: 
            shutil.copyfile(eqdskfname, 'EXPEQ.gz')
        except FileNotFoundError:
            sys.exit("For some reason helena has not created the eqdsk file. Aborting.")

        subprocess.call(['gunzip', 'EXPEQ.gz'])
        shutil.copyfile(chease_nml, 'chease_namelist')
        subprocess.call([chease_run], stdout=open('output.txt','w'), stderr=open('error.txt', 'w'))

        # Don't exit this function until we know Chease has finished
        count = 0
        while not os.path.exists(cwd+'/EQDSK_COCOS_02.OUT'):
            time.sleep(60)
            count = count + 1
            if (count == 25): #Don't wait longer than 25 minutes
                sys.exit("Waited too long for Chease to finish. Aborting.")
        return

    # this shouldn't have to be changed if running on Heimdall
    chease_run = '/home/ssaar/LINUX/chease/trunk/src-f90/chease_64'
    chease_nml = '/home/jwp9427/work/templates/chease_namelist'
    eqdskdir = '/home/jwp9427/work/chease/eqdsk/'
    
    # Modify Helena namelist to add "NPR2=1" at the end.
    namelist_new = edit_helena_nml(namelist)
    if namelist_new != namelist:
        print("Edited the HELENA namelist.")

    runhel_eqdsk(namelist_new) # run helena with your namelist (which has been modified to have "NPR2=1") to produce an eqdsk file
    print("Finished running HELENA and produced eqdsk file.")
    
    cwd = os.getcwd()
    
    rundir = '/home/jwp9427/work/chease/rundir/' + namelist_new
    subprocess.call(['mkdir', rundir])
    os.chdir(rundir)

    run_chease(namelist_new, chease_nml, chease_run) # run Chease and get the final eqdsk file
    print("Finished running Chease.")
    
    os.chdir(cwd)
    
    subprocess.call(['mv', rundir + '/EQDSK_COCOS_02.OUT', eqdskdir + namelist_new])
    subprocess.call(['rm', rundir + '/*'])
    subprocess.call(['rmdir', rundir])


