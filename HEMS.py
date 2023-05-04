from hydrogenStorage import HT
import sys
import os
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径
class HEMS(object):
    def __init__(self,ht:HT,el_power,fc_power):
        self.ht =ht
        self.GridToEnergy =0
        self.el = el_power
        self.fc =fc_power

    def initializa(self):
        '初始化'
        self.ht.initializa()
        self.GridToEnergy = 0
        self.storageToEnergy = 0
        self.energyToStorage = 0
    def energyStorage(self,energy):
        if energy >= 0:
            '充电过程'
            max_charge = min(self.ht.max_charge(),self.el)
            if energy <= max_charge:
                self.ht.soc(P_el=energy,P_fc=0)
                self.GridToEnergy = 0
                self.storageToEnergy = 0
                self.energyToStorage = energy
            else:
                self.ht.soc(P_el=max_charge,P_fc=0)
                self.GridToEnergy = 0
                self.storageToEnergy = 0
                self.energyToStorage = max_charge
        elif energy < 0:
            '放电过程'
            SOC = self.ht.readSOC()
            if SOC > self.ht.SOC_Min():
                max_discharge =min(self.ht.max_discharge(),self.fc)
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
        return self.GridToEnergy, self.storageToEnergy, self.energyToStorage


















