import pandas as pd
from datetime import datetime
from PVModel import PVSystem

# def data_cleaning_load(path):
#     path = r'C:\Users\王晨浩\Desktop\GPU_test\RECO_data\load_data.csv'
#     path = path
#     data  =pd.read_csv(path)
#
#     start_time = datetime(year=2019,month=1,day=1)
#     data.index = pd.date_range(start_time,periods=data.shape[0],freq='h')
#     data = data.iloc[:8760,:]
#
#     data  =data['2.169525401442797943e+02']
#     print(data)
#
#     data.to_csv('inputs_con_load_bt_HSSR/load_load.csv')
#
# def data_cleaning_load_nor(path):
#     path = r'C:\Users\王晨浩\Desktop\GPU_test\RECO_data\load_data.csv'
#     path = path
#     data = pd.read_csv(path)
#
#     start_time = datetime(year=2019, month=1, day=1)
#     data.index = pd.date_range(start_time, periods=data.shape[0], freq='h')
#     data = data.iloc[:8760, :]
#
#     data = data['2.169525401442797943e+02']
#     print(data)
#
#     data.to_csv('inputs_con_load_bt_HSSR/load_load.csv')


def data_cleaning_pv(path):
    path = path
    data = pd.read_csv(path, index_col=0)
    start_time = datetime(year=2019, month=1, day=1)
    data.index = pd.date_range(start_time, periods=data.shape[0], freq='h')
    pd_wea_T = data['气温℃'].tolist()
    pd_wea_G_dir = data['直接辐射W/m^2'].tolist()
    pd_wea_G_diff = data['散射辐射W/m^2'].tolist()
    pd_wea_G_hor = data['地表水平辐射W/m^2'].tolist()
    pv =700
    x = PVSystem(P_PV_rated=pv, pd_wea_T=pd_wea_T, pd_wea_G_dir=pd_wea_G_dir, pd_wea_G_diff=pd_wea_G_diff,
                 pd_wea_G_hor=pd_wea_G_hor)


    a = []

    for i in range(8760):
        a.append(x.PVpower(i))

    pv1 ={'pv_output':a}
    data_pv =pd.DataFrame(pv1)
    data_pv.to_csv('inputs_con_load_hy_LSSR/pv{}.csv'.format(pv))

if __name__ == '__main__':
    path_load =r'C:\Users\王晨浩\Desktop\Code\RLHydrogen\RECO_data\RECO_Load.csv'
    path_wea =r'C:\Users\王晨浩\Desktop\Code\RLHydrogen\RECO_data\RECO_Wea.csv'
    # data_cleaning_load(path_load)
    data_cleaning_pv(path_wea)


