from pylib.misc import ReadFile
import numpy as np
import os

def readfile(fort22_path):
    fort22_path = os.environ['CASTOR_DIR'] + 'eigfuncs/' + fort22_path
    with ReadFile(fort22_path) as f:
        # Reading eigenvalue
        ew = f.readwords(2, float)

        # Reading size of dimensions 
        ng = f.readword(int)
        manz = f.readword(int)
        neq = f.readword(int)

        # Reading list of poloidal harmonics
        rfour = f.readwords(manz, float)
        
        # Reading sqrt(psi) that CASTOR/MISHKA has used (Sbegin-Send)
        cs = f.readwords(ng, float)

        # Reading eigenvectors
        nbg = 2 * neq * manz
        ev = np.zeros([2,nbg,ng])
        for i in range(ng):
            ev[:,:,i] = f.readwords((2, nbg), float)
        ev[0,:,0] = 0


    # Reorganizing eigenvectors
    eigvec = np.zeros([2 * neq, 2, manz, ng])
    for i in range(neq):
        i1 = 2*i*manz
        i2 = 2*i*manz + 1
        m1 = i1 + 2*manz
        # v1, v2
        eigvec[2*i,:,0:manz,:] = ev[:,i1:m1:2,:]
        # dv1/ds, v2 midnode
        eigvec[2*i+1,:,0:manz,:] = ev[:,i2:m1:2,:]
    return manz,ng,cs,eigvec

def get_eigenfunc(castor_name, ivar, phase = 0):

    manz,ng,cs,eigvec = readfile(castor_name)
    ns = 1

    vec = []
    for m in range(manz):
        eig = (eigvec[2*ivar-2,0,m,ns:ng] * np.cos(phase) \
                        - eigvec[2*ivar-2,1,m,ns:ng] * np.sin(phase))
        eig *= -1
        vec.append(eig * 1e4)
    x = cs[ns:ng]
    x = x**2
    return x, vec