from PVModel import PVSystem
from ma_hydrogenStorage import HT
from gridPrice import   grid_price
from data_te import data_load1
import matplotlib.pyplot as plt
import math
import numpy as np
import sys
import os
from  converter import *
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径


class HEMS(object):
    def __init__(self,ht:HT,el_power,fc_power):
        self.ht =ht
        self.len =len(ht.LOH_t)
        self.GridToEnergy = np.zeros(self.len)
        self.storageToEnergy = np.zeros(self.len)
        self.energyToStorage = np.zeros(self.len)
        self.el_power= el_power
        self.fc_power= fc_power


    def initializa(self):
        self.ht.initializa()
        self.GridToEnergy = np.zeros(self.len)
        self.storageToEnergy = np.zeros(self.len)
        self.energyToStorage = np.zeros(self.len)

    def energyStorage(self, energy):
       for i in range(len(energy)):
           P_fc = np.zeros([self.ht.len_]  )
           P_el = np.zeros([self.ht.len_]  )

           if energy[i] >= 0:

                # print(energy[i])

                '充电过程'
                max_charge = min(self.ht.max_charge()[i],self.el_power[i])
                if energy[i] <= reverse_DC_DC_converter(max_charge):
                    P_el[i] = DC_DC_converter(energy[i])
                    self.ht.SOC(P_el=P_el,P_fc=P_fc)


                    self.GridToEnergy[i] = 0
                    self.storageToEnergy[i] =0
                    self.energyToStorage[i] =energy[i]
                else:
                    P_el[i] = max_charge
                    self.ht.SOC(P_el=P_el,P_fc=P_fc)
                    self.GridToEnergy[i] = 0
                    self.storageToEnergy[i] = 0
                    self.energyToStorage [i]=max_charge
           elif energy[i] < 0:
                P_fc = np.zeros([self.ht.len_])
                P_el = np.zeros([self.ht.len_])
                '放电过程'
                SOC = self.ht.readSOC()[i]
                # print(SOC,'SOC')
                # print(self.bt.SOC_min)
                if SOC > self.ht.SOC_Min()[i]:
                    max_discharge = min(self.ht.max_discharge()[i],self.fc_power[i]*0.6)
                    # print(type(max_discharge))
                    # print(max_discharge[i,:])

                    if abs(energy[i]) <= DC_DC_converter(max_discharge):

                        P_fc[i] = abs(reverse_DC_DC_converter(energy[i]))
                        self.ht.SOC(P_el=P_el,P_fc=P_fc)
                        self.GridToEnergy[i] = 0
                        self.storageToEnergy[i] = abs(energy[i])
                        self.energyToStorage[i] = 0
                    else:
                        P_fc[i] = max_discharge
                        self.ht.SOC(P_el=P_el,P_fc=P_fc)

                        self.GridToEnergy[i] =DC_AC_converter(abs(energy[i]) - DC_DC_converter(max_discharge))
                        self.storageToEnergy[i] =  max_discharge
                        self.energyToStorage[i] =  0
                else:
                    P_fc = np.zeros([self.ht.len_])
                    P_el = np.zeros([self.ht.len_])
                    self.ht.SOC(P_el=P_el,P_fc=P_fc)
                    self.GridToEnergy[i] =  DC_AC_converter(abs(energy[i]))
                    self.energyToStorage[i] = 0
                    self.storageToEnergy[i] = 0


       return self.GridToEnergy, self.storageToEnergy, self.energyToStorage

def device_init(in_:np.array):
    pd_load, pd_price, pd_wea_wind, pd_wea_G_dir, pd_wea_G_diff, pd_wea_T, pd_wea_G_hor = data_load1()

    pv_cap  = in_[:,0]
    print(pv_cap,'PV_CAP')
    pv =PVSystem(pv_cap,pd_wea_T=pd_wea_T,pd_wea_G_dir=pd_wea_G_dir,pd_wea_G_diff=pd_wea_G_diff,pd_wea_G_hor=pd_wea_G_hor)



    el_power = in_[:,1]
    print(el_power,'el_power')

    fc_power= in_[:,2]
    ht_cap  = in_[:,3]
    print(ht_cap,'ht_cap')
    ht = HT(Cap_H2=ht_cap)
    ht.initializa()
    print(fc_power,'fc_power')
    pv_output =[]
    R_init = 0
    for i in range(8760):
        pv_output.append(pv.PVpower(i))
        R_init +=pd_load[i]*grid_price(i)



    return pv,el_power,fc_power,ht,pd_load,pd_price,pv_output,R_init
