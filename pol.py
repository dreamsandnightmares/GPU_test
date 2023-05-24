import pandas as pd
import matplotlib.pyplot as plt
import  numpy as  np

path =r"C:\Users\王晨浩\Desktop\5.15\5.19\5.15_4\GPU_test\hy_bt\pareto_fitness_hy_2030_pem_hy.txt"

# path1 =r"C:\Users\王晨浩\Desktop\5.15\5.16\5.15\GPU_test\ht\pareto_fitness_ht.txt"
# # # 打开txt文件
# path2 =r"C:\Users\王晨浩\Desktop\5.15\5.16\5.15\GPU_test\hy_test\pareto_fitness_hy_2030_pem.txt"
# 读取txt文件
df = pd.read_csv(path, sep=' ', header=None, names=['col1', 'col2'])

x = df.sort_values('col1')




lcoe_list_bt =x['col1'].to_list()
ssr_list_bt =x['col2'].to_list()


for i in range(len(ssr_list_bt)):
    ssr_list_bt[i] = 1 - ssr_list_bt[i]







#
#
# df1 =pd.read_csv(path1, sep=' ', header=None, names=['col1', 'col2'])
# lcoe_list_ht = df1['col1'].to_list()
# ssr_list_ht =df1['col2'].to_list()
# for i in range(len(ssr_list_ht)):
#     ssr_list_ht[i] = 1 - ssr_list_ht[i]
#
# #
# df2 =pd.read_csv(path2, sep=' ', header=None, names=['col1', 'col2'])
# lcoe_list_hy = df2['col1'].to_list()
# ssr_list_hy =df2['col2'].to_list()
# for i in range(len(ssr_list_hy)):
#     ssr_list_hy[i] = 1 - ssr_list_hy[i]
#
#
#
plt.scatter(lcoe_list_bt,ssr_list_bt,label ='bt')
print(min(lcoe_list_bt))
print(max(lcoe_list_bt))

# plt.scatter(lcoe_list_ht,ssr_list_ht,label ='ht')
# plt.scatter(lcoe_list_hy,ssr_list_hy,label ='hy')
plt.legend()
# # plt.scatter(lcoe_list_ht,ssr_list_ht)
plt.show()
#
# print(max(ssr_list_hy),'max_hy_ssr')
# # print(max(ssr_list_ht))
# print(max(ssr_list_bt))



x = np.array([1,2,3,4])
a =np.array([2,3,4,5])
print(x/a)

