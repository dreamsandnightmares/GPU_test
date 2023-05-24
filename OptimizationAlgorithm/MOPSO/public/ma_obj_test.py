import math
import time
import os

import numpy as np

from data_te import  data_load1
from PVModel import  PVSystem
import pandas as pd

from ma_hydrogenStorage  import HT
from gridPrice import  grid_price
from MABattey import LionBattery
from maBEMS import BEMS
from maHEMS import HEMS
from maHybridESS import HybridESS
from converter import *


import matplotlib.pyplot as plt
import math



def ssr(P_grid, P_load):
    return ( (P_grid / P_load))

def device_init(in_):
    pd_load, pd_price, pd_wea_wind, pd_wea_G_dir, pd_wea_G_diff, pd_wea_T, pd_wea_G_hor = data_load1()

    pv_cap  = in_[:,0]
    pv =PVSystem(pv_cap,pd_wea_T=pd_wea_T,pd_wea_G_dir=pd_wea_G_dir,pd_wea_G_diff=pd_wea_G_diff,pd_wea_G_hor=pd_wea_G_hor)

    bt_cap = in_[:,1]
    bt = LionBattery(bt_cap,eta_BT_conv=0.98)
    bt.initializa()
    pv_output =[]
    R_init = 0
    for i in range(8760):
        pv_output.append(pv.PVpower(i))


        R_init +=pd_load[i]*grid_price(i)



    return pv,bt,pd_load,pd_price,pv_output,R_init
def device_init_ht(in_:np.array):
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
def device_init_hybrid(in_:np.array):
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


def NPV(r_0, r_bess, cost_bt, cost_h2, cost_el, cost_fc, li_cap, h2_cap, el_cap
        , fc_cap, cost_om, project_time):
    npv = 0
    cost_cap_bt = cost_bt * li_cap
    cost_cap_h2 = cost_h2 * h2_cap
    cost_cap_fc = cost_fc * fc_cap
    cost_cap_el = cost_el * el_cap
    cost_cap = cost_cap_el + cost_cap_bt + cost_cap_fc + cost_cap_h2
    for i in range(project_time):

        if i == 11:
            cost_rep = 0.60 * cost_cap_bt

            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i) - cost_cap
        elif i == 5:
            cost_rep = cost_fc * 0.775
            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i) - cost_cap
        elif i == 15:
            cost_rep = cost_fc * 0.55 + cost_el * 0.6
            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i) - cost_cap
        elif i == 20:
            cost_rep = cost_fc * 0.325
            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i) - cost_cap
        elif i == 25:
            cost_rep = cost_fc * 0.1
            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i) - cost_cap
        else:
            cost_rep = 0
            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i) - cost_cap

    return npv


def NPV_Bess(r_0, r_bess, cost_pv, cost_bt, li_cap, pv_cap, project_time):
    npv = 0
    cost_cap_bt = cost_bt * li_cap
    cost_cap_pv = pv_cap * cost_pv
    cost_om = cost_cap_bt * 0.005 + cost_cap_pv * 0.01

    # print(cost_om,'om')
    #
    # print(r_0,'r_init')
    # print(r_bess,'r_bess')

    cost_cap = cost_cap_bt + cost_cap_pv
    # print(cost_cap,'cap')
    for i in range(project_time):

        if i == 11:
            cost_rep = 0.60 * cost_cap_bt

            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i)
            # print(((r_0-r_bess) - cost_om - cost_rep) /math.pow((1+0.05),i),'rep')

        else:
            cost_rep = 0
            npv += ((r_0 - r_bess) - cost_om - cost_rep) / math.pow((1 + 0.05), i)
            # print(((r_0-r_bess) - cost_om - cost_rep) /math.pow((1+0.05),i),'not rep')
    # print(npv)
    npv = npv - cost_cap

    return npv


def lcos(cost_pv, cost_bt, li_cap, pv_cap, project_time, ele, wout):
    cost_cap_bt = cost_bt * li_cap
    cost_cap_pv = pv_cap * cost_pv
    cost_om = cost_cap_bt * 0.005 + cost_cap_pv * 0.01
    at = 0
    wout_all = 0
    cost_cap = cost_cap_bt + cost_cap_pv

    for i in range(project_time):
        if i == 11:
            cost_rep = 0.60 * cost_cap_bt

            at += (cost_om + cost_rep + 0.3 * ele) / math.pow((1 + 0.05), i)

            wout_all = wout / math.pow((1 + 0.05), i)
    return (cost_cap + at) / wout_all


def lcoe(cost_pv, cost_bt, li_cap, pv_cap, project_time, energy,ele_cost):
    cost_cap_bt = cost_bt * li_cap
    cost_cap_pv = pv_cap * cost_pv
    cost_om = cost_cap_bt * 0.005 + 0.01* cost_cap_pv
    d = 0.05
    down = 0
    cost_om_all = 0
    cost_rep = (0.60 * cost_cap_bt)/(math.pow((1+d),12))
    cost_cap = cost_cap_bt + cost_cap_pv

    for i in range(project_time):
        cost_om_all += cost_om / (math.pow((1 + d), i))

        down += (energy / (math.pow((1 + d), i)))

    lcoe_ = (cost_cap + cost_om_all + cost_rep+ele_cost) / down
    print((cost_cap + cost_om_all + cost_rep+ele_cost),'cost_all')
    print(down,'down')
    print(ele_cost,'ele_cost')
    return lcoe_

def lcoe_HT(cost_pv, cost_EL,cost_fc,cost_ht,el_power,fc_power,ht_cap,pv_cap, project_time, energy,ele_cost):
    cost_cap_el = cost_EL *el_power
    cost_cap_pv = pv_cap * cost_pv
    cost_cap_ht = cost_ht*ht_cap
    cost_cap_fc = cost_fc*fc_power



    cost_om = (cost_cap_ht+cost_cap_fc+cost_cap_el)*0.025 + 0.01*cost_cap_pv
    d = 0.05
    down = 0
    cost_om_all = 0

    cost_cap =cost_cap_ht+cost_cap_fc+cost_cap_el + cost_cap_pv
    print(cost_cap,'cap_cost')
    cost_rep = 0

    for i in range(project_time):
        cost_om_all += cost_om / (math.pow((1 + d), i))

        down += (energy / (math.pow((1 + d), i)))


        if i ==5:
                cost_rep+= (cost_cap_fc*0.775/(math.pow((1 + d), i)))
        elif i == 10:
                cost_rep += cost_cap_fc * 0.55/(math.pow((1 + d), i))
        elif i ==15:
                cost_rep+=0.325*cost_cap_fc/(math.pow((1 + d), i))
                cost_rep+=0.6*cost_cap_el/(math.pow((1 + d), i))
        elif i == 20:
                cost_rep += cost_cap_fc * 0.10/(math.pow((1 + d), i))


    lcoe_ = (cost_cap + cost_om_all + cost_rep+ele_cost) / down
    print((cost_cap + cost_om_all + cost_rep+ele_cost),'cost_all')
    print(down,'down')
    print(ele_cost,'ele_cost')
    return lcoe_
def lcoe_hy(cost_pv, cost_bt,cost_EL,cost_fc,cost_ht,el_power,fc_power,ht_cap,bt_cap,pv_cap, project_time, energy,ele_cost):
    cost_cap_el = cost_EL *el_power
    cost_cap_pv = pv_cap * cost_pv
    cost_cap_ht = cost_ht*ht_cap
    cost_cap_fc = cost_fc*fc_power
    cost_cap_bt = cost_bt*bt_cap



    cost_om = (cost_cap_ht+cost_cap_fc+cost_cap_el)*0.01 +cost_cap_pv*0.01+cost_cap_bt*0.005
    d = 0.05
    down = 0
    cost_om_all = 0

    cost_cap =cost_cap_ht+cost_cap_fc+cost_cap_el + cost_cap_pv+cost_cap_bt
    cost_rep = 0

    for i in range(project_time):
        cost_om_all += cost_om / (math.pow((1 + d), i))

        down += (energy / (math.pow((1 + d), i)))

        if i == 5:
            cost_rep += cost_cap_fc * 0.775/(math.pow((1 + d), i))
        elif i == 10:
            cost_rep += cost_cap_fc * 0.55/(math.pow((1 + d), i))
        elif i == 15:
            cost_rep += 0.325 * cost_cap_fc/(math.pow((1 + d), i))
            cost_rep += 0.6 * cost_cap_el/(math.pow((1 + d), i))
            cost_rep+=0.6*cost_cap_bt/(math.pow((1 + d), i))
        elif i == 20:
            cost_rep += cost_cap_fc * 0.10/(math.pow((1 + d), i))


    lcoe_ = (cost_cap + cost_om_all + cost_rep+ele_cost) / down
    print((cost_cap + cost_om_all + cost_rep+ele_cost),'cost_all')
    return lcoe_

def energy_management(project_lifetime:int,life_time:int,bt:np.array,pv_output:np.array,pd_load):
    res_output = pv_output
    # price_path = r'C:\Users\王晨浩\Desktop\GPU_test\RECO_data\price.csv'
    # price = pd.read_csv(price_path)
    # price = price['price'].tolist()

    ems  = BEMS(bt=bt)
    ems.initializa()
    ele_cost = 0
    soc_ = []
    gridTopower = 0
    stoTopower = 0
    energyTosto = 0
    energy_BESS = []

    soc_BESS = []

    ele_all = 0
    energy_sto = []
    energy_sto_dis = []
    for y in range(project_lifetime):
        for i in range(life_time):


            energy = DC_DC_converter(res_output[i]) - reverse_DC_AC_converter(pd_load[i])
            # print(energy,'energy')
            # print(energy.shape)
            soc_.append(bt.readSoc())
            soc_BESS.append(bt.readSoc())
            ele, sto, eTs = ems.energyStorage(energy)
            gridTopower += ele
            stoTopower += sto
            energyTosto += eTs
            energy_BESS.append(ele)
            ele_cost += ele * grid_price(i)
            ele_all += pd_load[i]
            energy_sto.append(eTs)
            energy_sto_dis.append(sto)
    print(ele_cost,'ele_cost')
    return gridTopower/project_lifetime,stoTopower/project_lifetime,energyTosto/project_lifetime,ele_cost,ele_all/project_lifetime

def energy_management_ht(project_lifetime:int,life_time:int,ht:HT,el:np.array,fc:np.array,pv_output:np.array,pd_load):
    res_output = pv_output
    # price_path = r'C:\Users\王晨浩\Desktop\GPU_test\RECO_data\price.csv'
    # price = pd.read_csv(price_path)
    # price = price['price'].tolist()


    ems  = HEMS(ht=ht,el_power=el,fc_power=fc)
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
    sto_ = []
    ets_=[]
    elel = []
    for y in range(project_lifetime):
        for i in range(life_time):
            energy = res_output[i] - pd_load[i]
            energy = np.round(energy, 8)
            # print(energy,'energy')
            # print(energy.shape)
            soc_.append(ht.readSOC())
            soc_BESS.append(ht.readSOC())
            ele, sto, eTs = ems.energyStorage(energy)
            elel.append(ele[0])
            sto_.append(sto[0])
            ets_.append(eTs[0])

            soc_.append(ht.readSOC())
            gridTopower += ele
            stoTopower += sto
            energyTosto += eTs
            energy_BESS.append(ele)
            ele_cost += ele * grid_price(i)
            ele_all += pd_load[i]
            energy_sto.append(eTs)
            energy_sto_dis.append(sto)
    print(sum(elel),'ele')
    return gridTopower/project_lifetime,stoTopower/project_lifetime,energyTosto/project_lifetime,ele_cost,ele_all/project_lifetime


def energy_management_hybid(project_lifetime:int,life_time:int,bt:LionBattery,ht:HT,el:np.array,fc:np.array,pv_output:np.array,pd_load):
    res_output = pv_output
    # price_path  =r'C:\Users\王晨浩\Desktop\GPU_test\RECO_data\price.csv'
    # price = pd.read_csv(price_path)
    # price = price['price'].tolist()


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
    sto_  =[]
    ets_ =[]
    for y in range(project_lifetime):
        for i in range(life_time):


            energy = res_output[i] - pd_load[i]
            energy = np.round(energy,8)
            # print(energy,'energy')
            # print(energy.shape)
            soc_.append(ht.readSOC())
            soc_BESS.append(ht.readSOC())
            ele, sto, eTs = ems.energyStorage(energy)
            sto_.append(sto[0])
            ets_.append(eTs[0])


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
    print(max(sto_),'最大发电')
    print(sum(sto_))
    print(sum(ets_))
    return gridTopower/project_lifetime,stoTopower/project_lifetime,energyTosto/project_lifetime,ele_cost,ele_all/project_lifetime

def fitness_ht(in_,cost_pv,cost_el,cost_fc,cost_ht,project_lifetime,life_time):

    pv,el_power,fc_power,ht,pd_load,pd_price,pv_output,R_init = device_init_ht(in_=in_,)
    gridTopower, stoTopower, energyTosto, ele_cost, ele_all = energy_management_ht(project_lifetime=project_lifetime,
                                                                                     life_time=life_time, ht=ht,
                                                                                     pv_output=pv_output,
                                                                                     pd_load=pd_load,el=el_power,fc=fc_power)

    Lcoe = lcoe_HT(cost_pv=cost_pv, cost_EL=cost_el,cost_fc=cost_fc,cost_ht=cost_ht, el_power=el_power,
                   pv_cap=in_[:,0], project_time=project_lifetime,
                energy=(ele_all), ele_cost=ele_cost,fc_power=fc_power,ht_cap=in_[:,3])
    SSR = ssr(gridTopower, ele_all)
    obj = np.array(list(zip(Lcoe,SSR)))

    # obj =np.array([Lcoe,SSR])
    print(obj)



    return obj

def fitness_hy(in_,cost_bt,cost_pv,cost_el,cost_fc,cost_ht,project_lifetime,life_time):
    pv, bt, el_power, fc_power, ht, pd_load, pd_price, pv_output, R_init = device_init_hybrid(in_)
    gridTopower, stoTopower, energyTosto, ele_cost, ele_all = energy_management_hybid(project_lifetime=project_lifetime,
                                                                                life_time=life_time, bt=bt, ht=ht,
                                                                                pv_output=pv_output,
                                                                                pd_load=pd_load, el=el_power,
                                                                                fc=fc_power)
    print(ele_cost,'ele_cost')

    Lcoe = lcoe_hy(cost_pv=cost_pv, cost_EL=cost_el,cost_fc=cost_fc,cost_ht=cost_ht, el_power=el_power,
                   pv_cap=in_[:,0], project_time=project_lifetime,
                energy=(ele_all), ele_cost=ele_cost,fc_power=fc_power,ht_cap  = in_[:,4],bt_cap=in_[:, 1],cost_bt=cost_bt)
    SSR = ssr(gridTopower, ele_all)
    # obj = np.array(list(zip(Lcoe,SSR)))
    obj =[]
    obj.append(Lcoe[0])
    obj.append(SSR[0])

    # obj =np.array([Lcoe,SSR])
    print(obj)



    return obj


def fitness_bt(in_,cost_bt,cost_pv,project_lifetime,life_time):
    pv, bt,  pd_load, pd_price, pv_output, R_init = device_init(in_)
    gridTopower, stoTopower, energyTosto, ele_cost, ele_all = energy_management(project_lifetime=project_lifetime,
                                                                                life_time=life_time, bt=bt,
                                                                                pv_output=pv_output,
                                                                                pd_load=pd_load,
                                                                                )



    Lcoe = lcoe(cost_pv=cost_pv,
                   pv_cap=in_[:,0], project_time=project_lifetime,
                energy=(ele_all), ele_cost=ele_cost,cost_bt=cost_bt,li_cap=in_[:,1])
    SSR = ssr(gridTopower, ele_all)
    obj = np.array(list(zip(Lcoe,SSR)))

    # obj =np.array([Lcoe,SSR])
    print(obj)



    return obj










if __name__ == '__main__':
    print(time.time())

    project_lifetime =25
    life_time = 8760
    cost_bt = 1625
    cost_pv =4040
    cost_el = 1600
    cost_fc =4000
    cost_ht = 200



    in_ =np.array([[1135,1726],[1135,1726]])

    obj =fitness_bt(in_=in_,project_lifetime=project_lifetime,life_time=life_time,cost_bt=cost_bt,cost_pv=cost_pv)


    # in_ = np.array([[1439, 557,172,8182],[1651,599,305,6252] ])
    # #
    # obj_2 = fitness_ht(in_=in_, project_lifetime=project_lifetime, life_time=life_time, cost_el=cost_bt,cost_fc= cost_fc,cost_pv=cost_pv,cost_ht=cost_ht)

    # in_ = np.array([[1315, 1050, 547, 100,9205], [1391, 1250, 511, 149,8350]])
    # obj_3 = fitness_hy(in_=in_, project_lifetime=project_lifetime, life_time=life_time, cost_el=cost_bt,
    #                    cost_fc=cost_fc, cost_pv=cost_pv, cost_ht=cost_ht,cost_bt=cost_bt)

    # pv, bt, pd_load, pd_price, pv_output, R_init = device_init(in_)
    # gridTopower, stoTopower, energyTosto, ele_cost, ele_all = energy_management(project_lifetime=project_lifetime,life_time=life_time,bt=bt,
    #                                                                             pv_output =pv_output,pd_load=pd_load,)



    # print(ele_all)
    # p  = 0
    # print(len(pd_load))
    # for i in range(len(pd_load)):
    #     p+= pd_load[i]*grid_price(i)
    # print(p/ele_all,'电价')
    # print(time.time())

    # print(gridTopower)
    # print(stoTopower)
    # print(energyTosto)
    # path = r"C:\Users\王晨浩\Desktop\1.csv"
    # pd = pd.read_csv(path)
    # print(pd)
    # PV = pd['列1.1'].tolist()
    # bt = pd['列1.2'].tolist()
    # el = pd['列1.3'].tolist()
    # fc =pd['列1.4'].tolist()
    # ht =pd['列1.5'].tolist()
    # project_lifetime = 25
    # life_time = 8760
    # cost_pv = 4040
    # cost_bt = 1462
    # cost_el =1600
    # cost_fc = 4000
    # cost_ht = 200
    # res =[]
    # cost_bt_ = [1625*0.9,1625*0.8,1625*0.7,1625*0.6]
    # cost_el_ =[1600*0.9,1600*0.8,1600*0.7,1600*0.6]
    # cost_fc_ =[4000*0.9,4000*0.8,4000*0.7,4000*0.6]
    #
    # for j in cost_bt_:
    #     res = []
    #     list = [0, 23, 40, 53, 71, 84, 97, 111, 125, 136, 145, 151, 156, 159, 161, 168, 170, 172, 175, 179, 180]
    #     for i in  list:
    #         in_ = np.array([[PV[i],bt[i],el[i],fc[i],ht[i]]])
    #         obj_3 = fitness_hy(in_=in_, project_lifetime=project_lifetime, life_time=life_time, cost_el=cost_el,
    #                            cost_fc=cost_fc, cost_pv=cost_pv, cost_ht=cost_ht, cost_bt=j)
    #         res.append(obj_3)
    #     x ='bt{}'.format(j)
    #
    #     with open("test{}.txt".format(x), "w") as f:
    #         pass
    #     res = np.array(res)
    #     print(res)
    #     file_path = os.path.abspath("test{}.txt".format(x))
    #     np.savetxt(file_path, res)
    # res = []
    # for j in cost_el_:
    #     res = []
    #     list = [0, 23, 40, 53, 71, 84, 97, 111, 125, 136, 145, 151, 156, 159, 161, 168, 170, 172, 175, 179, 180]
    #     for i in list:
    #         in_ = np.array([[PV[i], bt[i], el[i], fc[i], ht[i]]])
    #         obj_3 = fitness_hy(in_=in_, project_lifetime=project_lifetime, life_time=life_time, cost_el=j,
    #                            cost_fc=cost_fc, cost_pv=cost_pv, cost_ht=cost_ht, cost_bt=cost_bt)
    #         res.append(obj_3)
    #     x = 'el{}'.format(j)
    #
    #     with open("test{}.txt".format(x), "w") as f:
    #         pass
    #     res = np.array(res)
    #     print(res)
    #     file_path = os.path.abspath("test{}.txt".format(x))
    #     np.savetxt(file_path, res)
    # res = []
    # for j in cost_fc_:
    #     res = []
    #     list = [0, 23, 40, 53, 71, 84, 97, 111, 125, 136, 145, 151, 156, 159, 161, 168, 170, 172, 175, 179, 180]
    #     for i in list:
    #         in_ = np.array([[PV[i], bt[i], el[i], fc[i], ht[i]]])
    #         obj_3 = fitness_hy(in_=in_, project_lifetime=project_lifetime, life_time=life_time, cost_el=cost_el,
    #                            cost_fc=j, cost_pv=cost_pv, cost_ht=cost_ht, cost_bt=cost_bt)
    #         res.append(obj_3)
    #     x = 'fc{}'.format(j)
    #
    #     with open("test{}.txt".format(x), "w") as f:
    #         pass
    #     res = np.array(res)
    #     print(res)
    #     file_path = os.path.abspath("test{}.txt".format(x))
    #     np.savetxt(file_path, res)





