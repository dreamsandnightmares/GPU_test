from MABattey import LionBattery
from ma_hydrogenStorage  import HT
from PVModel import PVSystem
import matplotlib.pyplot as plt
import math
from gridPrice import  grid_price
from data_te import data_load1
import numpy as np
import sys
import os
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径


class HybridESS(object):
    def __init__(self, bt: LionBattery,ht:HT,el_power,fc_power):
        self.bt = bt
        self.ht = ht
        self.len = len(bt.readSoc())
        self.GridToEnergy = np.zeros(self.len)
        self.storageToEnergy = np.zeros(self.len)
        self.energyToStorage = np.zeros(self.len)

        self.el_power= el_power
        self.fc_power= fc_power

    def initializa(self):
        self.bt.initializa()
        self.ht.initializa()
        self.GridToEnergy = np.zeros(self.len)
        self.storageToEnergy = np.zeros(self.len)
        self.energyToStorage = np.zeros(self.len)

    def energyStorage(self, energy):
        for i in range(self.len):

            P_BT_dc = np.zeros([self.bt.len_])
            P_BT_ch = np.zeros([self.bt.len_])
            P_fc = np.zeros([self.ht.len_])
            P_el = np.zeros([self.ht.len_])

            if energy[i] >= 0:
                '充电过程'
                max_charge = self.bt.max_charge()[i]
                if energy[i] <= max_charge:
                    P_BT_ch[i] = energy[i]
                    self.bt.StateOfCharge1(P_BT_ch=P_BT_ch, P_BT_dc=P_BT_dc)
                    self.bt.soc(i)

                    self.GridToEnergy[i] = 0
                    self.storageToEnergy[i] = 0
                    self.energyToStorage[i] = energy[i]

                else:
                    P_BT_ch[i] = max_charge
                    self.bt.StateOfCharge1(P_BT_ch=P_BT_ch, P_BT_dc=P_BT_dc)
                    self.bt.soc(i)
                    self.GridToEnergy[i] = 0
                    self.storageToEnergy[i] = 0
                    self.energyToStorage[i] = max_charge

                    energyToStorage = max_charge
                    energy_ = energy[i] -max_charge

                    max_charge = min(self.ht.max_charge()[i],self.el_power[i])
                    if energy_ <= max_charge:
                        P_el[i] = energy[i]
                        self.ht.SOC(P_el=P_el,P_fc=P_fc)

                        self.GridToEnergy[i] = 0
                        self.storageToEnergy[i] = 0
                        self.energyToStorage[i] = energy[i]+energyToStorage

                    else:
                        P_el[i] = max_charge
                        self.ht.SOC(P_el=P_el,P_fc=P_fc)
                        self.GridToEnergy[i] = 0
                        self.storageToEnergy[i] = 0
                        self.energyToStorage[i] = max_charge+energyToStorage

            elif energy[i] < 0:
                P_BT_dc = np.zeros([self.bt.len_])
                P_BT_ch = np.zeros([self.bt.len_])
                P_fc = np.zeros([self.ht.len_])
                P_el = np.zeros([self.ht.len_])

                '放电过程'
                SOC = self.bt.readSoc()[i]
                if SOC > self.bt.SOC_min[i]:
                    max_discharge = self.bt.max_discharge()[i]

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

                        energy_ = abs(energy[i]) - max_discharge
                        stoToenergy=max_discharge

                        SOC = self.ht.readSOC()[i]
                        if SOC > self.ht.SOC_Min()[i]:
                            max_discharge = min(self.ht.max_discharge()[i],self.fc_power[i])
                            if energy_ <= max_discharge:
                                P_fc[i] = energy_
                                self.ht.SOC(P_el=P_el,P_fc=P_fc)
                                self.GridToEnergy[i] = 0
                                self.storageToEnergy[i] = energy_ +stoToenergy
                                self.energyToStorage[i] = 0
                            else:
                                P_fc[i] = max_discharge
                                self.ht.SOC(P_el=P_el,P_fc=P_fc)
                                self.GridToEnergy[i] = energy_ - max_discharge
                                self.storageToEnergy[i] = max_discharge+stoToenergy
                                self.energyToStorage[i] = 0

                        else:

                            self.GridToEnergy[i] = abs(energy[i]) -stoToenergy
                            self.energyToStorage[i] = 0
                            self.storageToEnergy[i] = stoToenergy


                else:
                        P_fc = np.zeros([self.ht.len_])
                        P_el = np.zeros([self.ht.len_])
                        SOC = self.ht.readSOC()[i]
                        if SOC > self.ht.SOC_Min()[i]:
                            max_discharge = min(self.ht.max_discharge()[i],self.fc_power[i])
                            if abs(energy[i]) <= max_discharge:

                                P_fc[i] = abs(energy[i])
                                self.ht.SOC(P_el=P_el, P_fc=P_fc)
                                self.GridToEnergy[i] = 0
                                self.storageToEnergy[i] = abs(energy[i])
                                self.energyToStorage[i] = 0
                            else:
                                P_fc[i] = max_discharge
                                self.ht.SOC(P_el=P_el, P_fc=P_fc)

                                self.GridToEnergy[i] = abs(energy[i]) - max_discharge
                                self.storageToEnergy[i] = max_discharge
                                self.energyToStorage[i] = 0

                        else:
                            self.GridToEnergy[i] = abs(energy[i])
                            self.energyToStorage[i] = 0
                            self.storageToEnergy[i] = 0

        return  self.GridToEnergy, self.storageToEnergy, self.energyToStorage


def device_init(in_:np.array):
    pd_load, pd_price, pd_wea_wind, pd_wea_G_dir, pd_wea_G_diff, pd_wea_T, pd_wea_G_hor = data_load1()

    pv_cap  = in_[:,0]
    print(pv_cap,'PV_CAP')
    pv =PVSystem(pv_cap,pd_wea_T=pd_wea_T,pd_wea_G_dir=pd_wea_G_dir,pd_wea_G_diff=pd_wea_G_diff,pd_wea_G_hor=pd_wea_G_hor)

    bt_cap = in_[:, 1]
    print(bt_cap, 'BT_CAP')
    bt = LionBattery(bt_cap, eta_BT_conv=0.98)
    bt.initializa()

    el_power = in_[:,2]
    print(el_power,'el_power')

    fc_power= in_[:,3]
    ht_cap  = in_[:,4]
    print(ht_cap,'ht_cap')
    ht = HT(Cap_H2=ht_cap)
    ht.initializa()
    print(fc_power,'fc_power')
    pv_output =[]
    R_init = 0
    for i in range(8760):
        pv_output.append(pv.PVpower(i))
        R_init +=pd_load[i]*grid_price(i)



    return pv,bt,el_power,fc_power,ht,pd_load,pd_price,pv_output,R_init
def energy_management(project_lifetime:int,life_time:int,bt:LionBattery,ht:HT,el:np.array,fc:np.array,pv_output:np.array,pd_load):
    res_output = pv_output


    ems  =HybridESS (bt=bt,ht=ht,el_power=el,fc_power=fc)

    ems.initializa()
    ele_cost = 0
    soc_ = []
    gridTopower = 0
    stoTopower = 0
    energyTosto = 0
    energy_BESS = []
    energy_BESS_OLDS = []
    soc_BESS = []
    soc_BESS_OLDS = []
    ele_all = 0
    energy_sto = []
    energy_sto_dis = []
    for y in range(project_lifetime):
        for i in range(life_time):


            energy = res_output[i] - pd_load[i]
            energy = np.round(energy,8)
            # print(energy,'energy')
            # print(energy.shape)
            soc_.append(ht.readSOC())
            soc_BESS.append(ht.readSOC())
            ele, sto, eTs = ems.energyStorage(energy)
            gridTopower += ele
            stoTopower += sto
            energyTosto += eTs
            energy_BESS.append(ele)
            ele_cost += ele * grid_price(i)
            ele_all += pd_load[i]
            energy_sto.append(eTs)
            energy_sto_dis.append(sto)
    print(ht.LOH_t)
    a = bt.readSoc()
    print(a,'soc')
    return gridTopower,stoTopower,energyTosto,ele_cost,ele_all
def energy_management_OLDS(project_lifetime:int,life_time:int,bt,ht:HT,el:np.array,fc:np.array,pv_output:np.array,pd_load,
                           t_start,t_end,limit_cloudy,limit_sunny,):
    res_output = pv_output


    ems  = HybridESS_OLDS(bt=bt,ht=ht,el_power=el,fc_power=fc,t_start=t_start,t_end=t_end,LIMIT_CLOUDY=limit_cloudy,LIMIT_SUNNY=limit_sunny)
    ems.initializa()
    ele_cost = 0
    soc_ = []
    gridTopower = 0
    stoTopower = 0
    energyTosto = 0
    energy_BESS = []
    energy_BESS_OLDS = []
    soc_BESS = []
    soc_BESS_OLDS = []
    ele_all = 0
    energy_sto = []
    energy_sto_dis = []
    for y in range(project_lifetime):
        for i in range(life_time):


            energy = res_output[i] - pd_load[i]
            energy = np.round(energy,8)
            # print(energy,'energy')
            # print(energy.shape)
            soc_.append(ht.readSOC())
            soc_BESS.append(ht.readSOC())
            ele, sto, eTs = ems.energyStorage(energy,i)
            gridTopower += ele
            stoTopower += sto
            energyTosto += eTs
            energy_BESS.append(ele)
            ele_cost += ele * grid_price(i)
            ele_all += pd_load[i]
            energy_sto.append(eTs)
            energy_sto_dis.append(sto)
    return gridTopower,stoTopower,energyTosto,ele_cost,ele_all