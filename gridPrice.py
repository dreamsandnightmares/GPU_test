from data_te import data_load1
from PVModel import PVSystem
import sys
import os
import pandas as pd
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径

def grid_price(time):
    price = 0
    if 19<=time%24<21 :
        price = 1.3917
    elif 8<= time%24<11 or 13<=time%24<19 or 21<=time%22:
        price =1.0377
    else:
        price = 0.4344
    return price

def grid_price1(time):
    path = r'/home/WCH/Code/M_con_load/GPU_test/RECO_data/price.csv'
    price  =pd.read_csv(path)
    price = price['price'].tolist()


    # price = {'price': pd_price}
    # data_price = pd.DataFrame(price)
    # data_price.to_csv('RECO_data/price.csv')


    return price[time]





if __name__ == '__main__':
    x= grid_price1(8760)
    print(x)


    # print(grid_cost*25)
    # x = PVSystem(P_PV_rated=900, pd_wea_T=pd_wea_T, pd_wea_G_dir=pd_wea_G_dir, pd_wea_G_diff=pd_wea_G_diff,
    #              pd_wea_G_hor=pd_wea_G_hor)
    # c = 0
    # a = []
    #
    # for i in range(8760):
    #     a.append(x.PVpower(i))
    #
    #     c += x.PVpower(i)
    # print(c,'pv_all')
    # print(load_all)
    #
    #
