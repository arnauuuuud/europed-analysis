from ppf import ppfuid, ppfget


def alpha_operational_point(shot=84794, dda='T052', uid='lfrassin', plot=False, alpha=None,
                            pos_alpha=None, corr_zeff=False, only_pe=False, out=None,
                            equi_dda='EFTP', equi_uid='JETPPF', equi_seq=0):
    import numpy as np

    def ppfread(shot, dda, dtype, uid, seq=0):
        ppfuid(uid)
        ihdat,iwdat,data,x,time,ier = ppfget(pulse=shot,dda=dda,dtyp=dtype)
        return data, time

    nefit, _ = ppfread(shot, dda, 'NEF3', uid)
    tefit, _ = ppfread(shot, dda, 'TEF5', uid)
    psif, _ = ppfread(shot, dda, 'PSIF', uid)
    volf, _ = ppfread(shot, dda, 'VOLF', uid)
    kt1, _ = ppfread(shot, dda, 'KT1', uid)
    kt2, _ = ppfread(shot, dda, 'KT2', uid)
    psi0a, tpsi = ppfread(shot, equi_dda, 'FAXS', equi_uid, equi_seq)
    
    if tpsi is None:
        equi_seq = 0
        psi0a, tpsi = ppfread(shot, equi_dda, 'FAXS', equi_uid, equi_seq)
    
    psi1a, _ = ppfread(shot, equi_dda, 'FBND', equi_uid, equi_seq)
    volma, _ = ppfread(shot, equi_dda, 'VOLM', equi_uid, equi_seq)
    rgeoa, _ = ppfread(shot, equi_dda, 'RGEO', equi_uid, equi_seq)
    cr0a, _ = ppfread(shot, equi_dda, 'CR0', equi_uid, equi_seq)
    zeff, tz = ppfread(shot, 'KS3', 'ZEFV', 'JETPPF')
    
    if tz is None:
        tz = tpsi
        zeff = np.full_like(tz, 1.7 if shot <= 80000 else 1.3)
    
    ##print(kt1[0], kt2[0])
    ind = np.where((tpsi >= kt1[0]) & (tpsi <= kt2[0]))
    psi0 = np.mean(psi0a[ind])
    psi1 = np.mean(psi1a[ind])
    volm = np.mean(volma[ind])
    rgeo = np.mean(rgeoa[ind])
    cr0 = np.mean(cr0a[ind])
    ind = np.where((tz >= kt1[0]) & (tz <= kt2[0]))
    zeff = np.mean(zeff[ind])
    corr = 2
    
    if corr_zeff:
        corr = 1 + (7 - zeff) / 6 if shot <= 80000 else 1 + (5 - zeff) / 4
    
    if only_pe:
        corr = 1

    
    isep = np.argmin(np.abs(tefit - 0.1))
    ilcfs = np.argmin(np.abs(psif - 1))
    dpsi = psif[ilcfs] - psif[isep]
    psif += dpsi


    ilcfs = np.argmin(np.abs(volf - 1))
    dvol = volf[ilcfs] - volf[isep]
    volf += dvol

    der = -np.gradient(1.6 * nefit * tefit * corr, psif)
    ind = np.where(psif >= 0.8)
    gradmax = np.max(der[ind])
    psimax = psif[ind][np.argmax(der[ind])]
    
    vol = volf * volm
    mu0 = 4 * np.pi * 1e-7
    alpha = 2 / (2 * np.pi) ** 2 * np.sqrt(vol / (2 * np.pi ** 2 * rgeo)) * np.gradient(vol,psif) * (der * 1e3) * mu0 / (psi1 - psi0) ** 2
    
    alphamax = np.nanmax(alpha[ind])
    psiamax = psif[ind][np.argmax(alpha[ind])]
    
    #print(psi0)
    #print(psi1)
    #print(psi1 - psi0)
    
    #print(np.mean(vol))

    if plot:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(7, 9))
        plt.subplot(2, 1, 1)
        plt.plot(psif, np.gradient(vol, psif), label='grad(p) (kPa/psi)')
        plt.xlabel('w')
        plt.ylabel('grad(p) (kPa/psi)')
        plt.legend()
        
        plt.subplot(2, 1, 2)
        plt.plot(psif, alpha, label='alpha')
        plt.xlabel('w')
        plt.ylabel('alpha')
        plt.legend()
        
        plt.show()

    out = {'alphamax': alphamax, 'pos_alpha': psiamax, 'psi': psif, 'alpha': alpha}
    return out

