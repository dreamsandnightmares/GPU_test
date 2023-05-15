
from Battey import LionBattery
from hydrogenStorage import HT
from PVModel import PVSystem
import matplotlib.pyplot as plt
import math
from gridPrice import  grid_price
from data_te import data_load1
import sys
import os
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径

class HybridESS(object):
    def __init__(self, bt: LionBattery,ht:HT,el_power,fc_power):
        self.bt = bt
        self.GridToEnergy = 0
        self.storageToEnergy = 0
        self.energyToStorage = 0
        self.ht = ht
        self.el = el_power
        self.fc = fc_power

    def initializa(self):
        self.bt.initializa()
        self.ht.initializa()
        self.GridToEnergy = 0
        self.storageToEnergy = 0
        self.energyToStorage = 0

    def energyStorage(self, energy):
        if energy >= 0:
            '充电过程'
            max_charge = self.bt.max_charge()
            if energy <= max_charge:
                self.bt.StateOfCharge(P_BT_ch=energy, P_BT_dc=0)
                self.GridToEnergy = 0
                self.storageToEnergy = 0
                self.energyToStorage = energy
            else:
                self.bt.StateOfCharge(P_BT_ch=max_charge, P_BT_dc=0)
                self.GridToEnergy = 0
                self.storageToEnergy = 0
                self.energyToStorage = max_charge

                energyToStorage = max_charge
                energy = energy -max_charge

                max_charge = min(self.ht.max_charge(), self.el)
                if energy <= max_charge:
                    self.ht.soc(P_el=energy, P_fc=0)
                    self.GridToEnergy = 0
                    self.storageToEnergy = 0
                    self.energyToStorage = energy+energyToStorage
                else:
                    self.ht.soc(P_el=max_charge, P_fc=0)
                    self.GridToEnergy = 0
                    self.storageToEnergy = 0
                    self.energyToStorage = max_charge+energyToStorage
        elif energy < 0:
            '放电过程'
            SOC = self.bt.readSoc()
            if SOC > self.bt.SOC_min:
                max_discharge = self.bt.max_discharge()
                if abs(energy) <= max_discharge:
                    self.bt.StateOfCharge(P_BT_ch=0, P_BT_dc=abs(energy))
                    self.GridToEnergy = 0
                    self.storageToEnergy = abs(energy)
                    self.energyToStorage = 0
                else:

                    self.bt.StateOfCharge(P_BT_ch=0, P_BT_dc=max_discharge)
                    energy = abs(energy) - max_discharge
                    stoToenergy=max_discharge
                    SOC = self.ht.readSOC()
                    if SOC > self.ht.SOC_Min():
                        max_discharge = min(self.ht.max_discharge(), self.fc*0.6)
                        if abs(energy) <= max_discharge:
                            self.ht.soc(P_el=0, P_fc=abs(energy))
                            self.GridToEnergy = 0
                            self.storageToEnergy = abs(energy)+stoToenergy
                            self.energyToStorage = 0
                        else:
                            self.ht.soc(P_el=0, P_fc=abs(max_discharge))
                            self.GridToEnergy = abs(energy) - max_discharge
                            self.storageToEnergy = max_discharge+stoToenergy
                            self.energyToStorage = 0
                    else:
                        self.GridToEnergy = abs(energy)
                        self.energyToStorage = 0
                        self.storageToEnergy = stoToenergy


            else:
                    SOC = self.ht.readSOC()
                    if SOC > self.ht.SOC_Min():
                        max_discharge = min(self.ht.max_discharge(), self.fc*0.6)
                        if abs(energy) <= max_discharge:
                            self.ht.soc(P_el=0, P_fc=abs(energy))
                            self.GridToEnergy = 0
                            self.storageToEnergy = abs(energy)
                            self.energyToStorage = 0
                        else:
                            self.ht.soc(P_el=0, P_fc=abs(max_discharge))
                            self.GridToEnergy = abs(energy) - max_discharge
                            self.storageToEnergy = max_discharge
                            self.energyToStorage = 0
                    else:
                        self.GridToEnergy = abs(energy)
                        self.energyToStorage = 0
                        self.storageToEnergy = 0

        return  self.GridToEnergy, self.storageToEnergy, self.energyToStorage



def device_init():
    pd_load, pd_price, pd_wea_wind, pd_wea_G_dir, pd_wea_G_diff, pd_wea_T, pd_wea_G_hor = data_load1()

    pv_cap  = 650
    pv =PVSystem(pv_cap,pd_wea_T=pd_wea_T,pd_wea_G_dir=pd_wea_G_dir,pd_wea_G_diff=pd_wea_G_diff,pd_wea_G_hor=pd_wea_G_hor)

    bt_cap = 600
    bt = LionBattery(bt_cap,eta_BT_conv=0.98)
    bt.initializa()

    el_cap = 15
    el  =PEM()
    el_n = math.ceil(el_cap/el.max_power())

    fc_cap =15
    fc = PEMFC()
    fc_n  =math.ceil(fc_cap/fc.max_power())

    ht_cap = 2000
    ht = HT(ht_cap,eta_FC=0.6,eta_EL=0.86,delta_t=1)
    ht.initializa()
    pv_output =[]
    R_init = 0
    for i in range(8760):
        pv_output.append(pv.PVpower(i))
        R_init +=pd_load[i]*grid_price(i)



    return pv,bt,el,el_n,fc,fc_n,ht,pd_load,pd_price,pv_output,R_init






