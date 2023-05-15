import matplotlib.pyplot as plt
import numpy as  np
import pandas as pd
import math
import xlwt
import sys
import os
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)  # 添加路径到系统路径
from data_te import data_load1

class PVSystem(object):

    def __init__(self,P_PV_rated,pd_wea_T,pd_wea_G_dir,pd_wea_G_diff,pd_wea_G_hor):
        '温度信息'
        self.T = pd_wea_T
        self.pd_wea_G_dir = pd_wea_G_dir
        self.pd_wea_G_diff = pd_wea_G_diff
        self.pd_wea_G_hor =pd_wea_G_hor
        self.NocT =44
        self.P_PV_rated = P_PV_rated
        self.g_all = []

    def PVpower(self,time,f_pv = 0.86,G_stc = 1,gammaT = -0.003,T_cell_STC = 25):

        G = (float(self.pd_wea_G_dir[time])) * math.cos(2 * math.pi / 360 * 26.7) + (float(self.pd_wea_G_diff[time])) * 0.3 + (
            float(self.pd_wea_G_hor[time])) * 0.2 * 0.5

        T_cell = self.T[time] + (float(G)) / 0.5 * (45 - 20) / 1000

        P_PV = f_pv*self.P_PV_rated*(float(G))/G_stc*(1+gammaT*(T_cell-T_cell_STC))/1000


        self.g_all.append(G)
        return P_PV

if __name__ == '__main__':
    pd_load, pd_price, pd_wea_wind, pd_wea_G_dir, pd_wea_G_diff, pd_wea_T, pd_wea_G_hor = data_load1()
    x = PVSystem(P_PV_rated=1500,pd_wea_T=pd_wea_T,pd_wea_G_dir=pd_wea_G_dir,pd_wea_G_diff=pd_wea_G_diff,pd_wea_G_hor=pd_wea_G_hor)
    c = 0
    a = []

    for i in range(8760):
        a.append(x.PVpower(i))

        c += x.PVpower(i)
    diff_list =[]
    for i in range(8760):
        diff = pd_load[i]  - a[i]
        diff_list.append(diff)
    dist = list(range(len(diff_list)))
    plt.plot(dist,diff_list)
    print(max(diff_list),'max_load')
    plt.show()



    # # 例如我们要存储两个list：name_list 和 err_list 到 Excel 两列
    # # name_list和err_list均已存在
    # name_list = a  # 示例数据
    # err_list = [0.99, 0.98, 0.97]  # 示例数据
    #
    # # 导包，如未安装，先 pip install xlwt


    # 设置Excel编码
    # file = xlwt.Workbook('encoding = utf-8')
    #
    # # 创建sheet工作表
    # sheet1 = file.add_sheet('sheet1', cell_overwrite_ok=True)
    #
    # # 先填标题
    # # sheet1.write(a,b,c) 函数中参数a、b、c分别对应行数、列数、单元格内容
    # sheet1.write(0, 0, "小时")  # 第1行第1列
    # sheet1.write(0, 1, "发电量 [KW]")  # 第1行第2列
    # # sheet1.write(0, 2, "误差")  # 第1行第3列
    #
    # # 循环填入数据
    # for i in range(len(name_list)):
    #     sheet1.write(i + 1, 0, i)  # 第1列序号
    #     sheet1.write(i + 1, 1, name_list[i])  # 第2列数量
    #
    #
    # # 保存Excel到.py源文件同级目录
    # file.save('Data.xls')
    #
    #
