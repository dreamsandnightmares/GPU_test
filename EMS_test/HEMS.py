import math

from maHEMS import *
import numpy as np
import matplotlib.pyplot as plt
from converter import *
from gridPrice import grid_price
def test_HEMS():
    in_ = np.array([[1287,479,145,6000]])
    pv,el_power,fc_power,ht,pd_load,pd_price,pv_output,R_init = device_init(in_)
    EMS = HEMS(el_power=el_power,fc_power=fc_power,ht=ht)
    EMS.initializa()
    timerange = 8760
    SOC = []
    eTs = []
    GridToEnergy = 0
    storageToEnergy = 0
    energyToStorage = 0
    ernergy_list = []
    x_list = []
    price = 0
    power =[]
    for i in range(timerange):
        energy =DC_DC_converter(pv.PVpower(i)) - reverse_DC_AC_converter(pd_load[i])

        x1,x2,x3 =EMS.energyStorage(energy)
        power.append(x2[0])
        SOC.append(EMS.ht.readSOC()[0])

        GridToEnergy+=x1
        storageToEnergy+=x2
        energyToStorage +=x3

        eTs.append(x3[0]/350)
        ernergy_list.append(abs(energy))
        x_list.append(x1[0]+x2[0]+x3[0])
        price += pd_price[i]*x1

    print(GridToEnergy, 'GridToEnergy')
    print(storageToEnergy, 'storageToEnergy')
    print(energyToStorage, 'energyToStorage')

    dist = list(range(len(power)))
    plt.plot(dist, power)

    # plt.plot(dist, ernergy_list)
    plt.show()




if __name__ == '__main__':
    test_HEMS()
