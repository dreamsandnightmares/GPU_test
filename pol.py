import pandas as pd
import matplotlib.pyplot as plt


path =r"C:\Users\王晨浩\Desktop\mopso_data\nor\pareto_fitness_bt.txt"
path1 =r"C:\Users\王晨浩\Desktop\mopso_data\nor\pareto_fitness_ht.txt"
# # 打开txt文件
path2 =r"C:\Users\王晨浩\Desktop\mopso_data\nor\pareto_fitness_hy_2030_pem.txt"

# 读取txt文件
df = pd.read_csv(path, sep=' ', header=None, names=['col1', 'col2'])

lcoe_list_bt =df['col1'].to_list()
ssr_list_bt =df['col2'].to_list()
print(min(lcoe_list_bt))

for i in range(len(ssr_list_bt)):
    ssr_list_bt[i] = 1 - ssr_list_bt[i]


df1 =pd.read_csv(path1, sep=' ', header=None, names=['col1', 'col2'])
lcoe_list_ht = df1['col1'].to_list()
ssr_list_ht =df1['col2'].to_list()
for i in range(len(ssr_list_ht)):
    ssr_list_ht[i] = 1 - ssr_list_ht[i]

#
df2 =pd.read_csv(path2, sep=' ', header=None, names=['col1', 'col2'])
lcoe_list_hy = df2['col1'].to_list()
ssr_list_hy =df2['col2'].to_list()
for i in range(len(ssr_list_hy)):
    ssr_list_hy[i] = 1 - ssr_list_hy[i]



plt.scatter(lcoe_list_bt,ssr_list_bt)
plt.scatter(lcoe_list_ht,ssr_list_ht)
plt.scatter(lcoe_list_hy,ssr_list_hy)
# plt.scatter(lcoe_list_ht,ssr_list_ht)
plt.show()

print(max(ssr_list_hy),'max_hy_ssr')
print(max(ssr_list_ht))
print(max(ssr_list_bt))


