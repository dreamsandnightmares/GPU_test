'外送电路问题  '
'效率问题'
'适用场景问题'

'为什么充电变多了BESS OLDS'

from  PVModel import PVSystem
import numpy as np

from  hydrogenStorage import HT
from  gridPrice import grid_price
from  data_te import data_load1
from  HEMS import HEMS

from  HybridESS import HybridESS

from  MABattey import LionBattery
import matplotlib.pyplot as plt
import math
import sys
import os
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径
'''
project time 20:
光+储 ： 0.065
光    ： 0.038


project time 30:
光+储 ：0.054 
光    ：0.031

光伏系统验证完成


'''

'实例化设备'


class BEMS(object):
    def __init__(self, bt: LionBattery):
        self.bt = bt
        self.len =len(bt.readSoc())
        self.GridToEnergy = np.zeros(self.len)
        self.storageToEnergy = np.zeros(self.len)
        self.energyToStorage = np.zeros(self.len)

    def initializa(self):
        self.bt.initializa()
        self.GridToEnergy = np.zeros(self.len)
        self.storageToEnergy = np.zeros(self.len)
        self.energyToStorage = np.zeros(self.len)

    def energyStorage(self, energy):
       for i in range(len(energy)):
           P_BT_dc = np.zeros([self.bt.len_]  )
           P_BT_ch = np.zeros([self.bt.len_]  )

           if energy[i] >= 0:

                # print(energy[i])

                '充电过程'
                max_charge = self.bt.max_charge()[i]
                if energy[i] <= max_charge:
                    P_BT_ch[i] = energy[i]
                    self.bt.StateOfCharge1(P_BT_ch=P_BT_ch, P_BT_dc=P_BT_dc)
                    self.bt.soc(i)

                    self.GridToEnergy[i] = 0
                    self.storageToEnergy[i] =0
                    self.energyToStorage[i] =energy[i]
                else:
                    P_BT_ch[i] = max_charge
                    self.bt.StateOfCharge1(P_BT_ch=P_BT_ch, P_BT_dc=P_BT_dc)
                    self.bt.soc(i)
                    self.GridToEnergy[i] = 0
                    self.storageToEnergy[i] = 0
                    self.energyToStorage [i]=max_charge
           elif energy[i] < 0:
                P_BT_dc = np.zeros([self.bt.len_])
                P_BT_ch = np.zeros([self.bt.len_])
                '放电过程'
                SOC = self.bt.readSoc()[i]
                # print(SOC,'SOC')
                # print(self.bt.SOC_min)
                if SOC > self.bt.SOC_min[i]:
                    max_discharge = self.bt.max_discharge()[i]
                    # print(type(max_discharge))
                    # print(max_discharge[i,:])

                    if abs(energy[i]) <= max_discharge:

                        P_BT_dc[i] = abs(energy[i])
                        self.bt.StateOfCharge1(P_BT_ch=P_BT_ch, P_BT_dc=P_BT_dc)
                        self.bt.soc(i)
                        self.GridToEnergy[i] = 0
                        self.storageToEnergy[i] = abs(energy[i])
                        self.energyToStorage[i] = 0
                    else:
                        P_BT_dc[i] = max_discharge
                        self.bt.StateOfCharge1(P_BT_ch=P_BT_ch, P_BT_dc=P_BT_dc)
                        self.bt.soc(i)
                        self.GridToEnergy[i] =abs(energy[i]) - max_discharge
                        self.storageToEnergy[i] =  max_discharge
                        self.energyToStorage[i] =  0
                else:
                    P_BT_dc = np.zeros([self.bt.len_])
                    P_BT_ch = np.zeros([self.bt.len_])
                    self.bt.StateOfCharge1(P_BT_ch=P_BT_ch, P_BT_dc=P_BT_dc)
                    self.bt.soc(i)
                    self.GridToEnergy[i] =  abs(energy[i])
                    self.energyToStorage[i] = 0
                    self.storageToEnergy[i] = 0


       return self.GridToEnergy, self.storageToEnergy, self.energyToStorage



def device_init(in_:np.array):
    pd_load, pd_price, pd_wea_wind, pd_wea_G_dir, pd_wea_G_diff, pd_wea_T, pd_wea_G_hor = data_load1()

    pv_cap  = in_[:,0]
    print(pv_cap,'PV_CAP')
    pv =PVSystem(pv_cap,pd_wea_T=pd_wea_T,pd_wea_G_dir=pd_wea_G_dir,pd_wea_G_diff=pd_wea_G_diff,pd_wea_G_hor=pd_wea_G_hor)

    bt_cap = in_[:,1]
    print(bt_cap,'BT_CAP')
    bt = LionBattery(bt_cap,eta_BT_conv=0.98)
    bt.initializa()
    pv_output =[]
    R_init = 0
    for i in range(8760):
        pv_output.append(pv.PVpower(i))
        R_init +=pd_load[i]*grid_price(i)



    return pv,bt,pd_load,pd_price,pv_output,R_init