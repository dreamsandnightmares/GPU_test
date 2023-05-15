import math

from maBEMS import BEMS,device_init
import numpy as np
import matplotlib.pyplot as plt
from converter import *
from gridPrice import grid_price

def test_BEMS():
    in_ = np.array([[900, 2000]])

    pv, bt, pd_load, pd_price, pv_output, R_init = device_init(in_)
    EMS = BEMS(bt=bt)
    EMS.initializa()
    timerange =8760
    SOC =[]
    eTs = []
    GridToEnergy=0
    storageToEnergy=0
    energyToStorage=0
    ernergy_list =[]
    x_list =[]
    price =0

    for i in range(timerange):
        energy =DC_DC_converter(pv.PVpower(i)) - reverse_DC_AC_converter(pd_load[i])

        x1,x2,x3 =EMS.energyStorage(energy)
        SOC.append(EMS.bt.readSoc()[0])

        GridToEnergy+=x1
        storageToEnergy+=x2
        energyToStorage +=x3

        eTs.append(x3[0]/350)
        ernergy_list.append(abs(energy))
        x_list.append(x1[0]+x2[0]+x3[0])
        price += pd_price[i]*x1






    print(GridToEnergy,'GridToEnergy')
    print(storageToEnergy,'storageToEnergy')
    print(energyToStorage,'energyToStorage')
    print(price*25)
    print(900*4040+2000*1600)
    dist = list(range(len(SOC)))
    plt.plot(dist,SOC)



    # plt.plot(dist,ernergy_list)
    plt.show()

def test_price():
    in_ = np.array([[900, 2000]])

    pv, bt, pd_load, pd_price, pv_output, R_init = device_init(in_)
    x = 0
    down = 0
    d =0.05
    a  =0
    for i in range(8760):
        x += pd_load[i]*grid_price(i)
    energy = sum(pd_load[:8760])
    for i in range(25):
        # a +=(x / math.pow((1 + d), i))

        down += (energy / math.pow((1 + d), i))
    print(x*25)
    print(x/energy)
    print(x*25/down)


    # for i in range(25):
    #     down += (energy/math.pow((1+d),i)

if __name__ == '__main__':
    test_BEMS()






