from hoho import startup,useful_recurring_functions,europed_analysis_2, helena_read, pedestal_values, getprofile
import numpy as np
import matplotlib.pyplot as plt

dict_SET_profile = {
    'J_phi':'SET4',
    'Q':'SET4', 
    'PSI':'SET4'
}


def get_profile(q='J_phi', europed_name='jt-60sa_7_mishka', device_name='jt60-sa', crit='alfven', crit_value=0.03, exclud_mode = None, list_consid_mode = None):
    runid = europed_analysis_2.get_runid(europed_name)
    fixed_width = europed_name.startswith('fw')
    p1, p2, ratio = pedestal_values.critical_profile_number(europed_name, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)

    ho1 = f'{device_name}0.{runid}_{p1}'
    ho2 = f'{device_name}0.{runid}_{p2}'

    print(ho1)

    b1 = helena_read.read_output(ho1)
    b2 = helena_read.read_output(ho2)

    setnb = dict_SET_profile[q]

    q1 = np.array(b1[setnb][q])
    q2 = np.array(b2[setnb][q])

    qfinal = q1 + ratio*(q2-q1)
    return qfinal

def get_profile_eliteinp(q='q', europed_name='jt-60sa_7_mishka', device_name='jt-60sa', shot_number=0, crit='alfven', crit_value=0.03, exclud_mode = None, list_consid_mode = None):
    runid = europed_analysis_2.get_runid(europed_name)
    fixed_width = europed_name.startswith('fw')
    p1, p2, ratio = pedestal_values.critical_profile_number(europed_name, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)

    ho1 = f'{device_name}{shot_number}.{runid}_{p1}'
    ho2 = f'{device_name}{shot_number}.{runid}_{p2}'

    b1 = helena_read.read_eliteinp(ho1)
    b2 = helena_read.read_eliteinp(ho2)

    q1 = np.array(b1[q])
    q2 = np.array(b2[q])

    # plt.plot(range(len(q1)),q1)
    # plt.plot(range(len(q2)),q2)

    qfinal = q1 + ratio*(q2-q1)

    # plt.plot(range(len(qfinal)),qfinal)
    # plt.show()
    return qfinal



def get_profile_psij(europed_name='jt-60sa_7_mishka', device_name='jt-60sa', shot_number=0, crit='alfven', crit_value=0.03, exclud_mode = None, list_consid_mode = None):
    runid = europed_analysis_2.get_runid(europed_name)
    fixed_width = europed_name.startswith('fw')
    p1, p2, ratio = pedestal_values.critical_profile_number(europed_name, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)

    ho1 = f'{device_name}{shot_number}.{runid}_{p1}'
    ho2 = f'{device_name}{shot_number}.{runid}_{p2}'

    print(ho1)
    print(ho2)

    psi1, j1 = getprofile.extract_psi_and_j(ho1)
    psi2, j2 = getprofile.extract_psi_and_j(ho2)

    psi1 = np.array(psi1)
    psi2 = np.array(psi2)
    j1 = np.array(j1)
    j2 = np.array(j2)

    psif = psi1 + ratio*(psi2-psi1)
    jf = j1 + ratio*(j2-j1)
    return psif,jf


def get_profile_psij_bis(europed_name='jt-60sa_7_mishka', device_name='jt-60sa', shot_number=0, crit='alfven', crit_value=0.03, exclud_mode = None, list_consid_mode = None):
    runid = europed_analysis_2.get_runid(europed_name)
    fixed_width = europed_name.startswith('fw')
    p1, p2, ratio = pedestal_values.critical_profile_number(europed_name, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)

    ho1 = f'{device_name}{shot_number}.{runid}_{p1}'
    ho2 = f'{device_name}{shot_number}.{runid}_{p2}'

    print(ho1)
    print(ho2)

    psi1, j1 = getprofile.extract_psi_and_j_bis(ho1)
    psi2, j2 = getprofile.extract_psi_and_j_bis(ho2)

    psi1 = np.array(psi1)
    psi2 = np.array(psi2)
    j1 = np.array(j1)
    j2 = np.array(j2)

    psif = psi1 + ratio*(psi2-psi1)
    jf = j1 + ratio*(j2-j1)
    return psif,jf


