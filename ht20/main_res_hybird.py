#encoding: utf-8
import numpy as np
import os
import sys
dir_now = sys.path[0]

dis_up = os.path.dirname(dir_now)
dis_upuo = os.path.dirname(dis_up)

sys.path.append(os.path.dirname(dir_now))
sys.path.append(dis_up)
sys.path.append(dis_upuo)
from Mopso_res_hybid import *
import os




 
def main():

    particals = 30 #粒子群的数量
    cycle_ = 50 #迭代次数
    mesh_div = 10 #网格等分数量
    thresh = 300#外部存档阀值
    project_lifetime = 25
    life_time = 8760
    cost_pv = 4040
    cost_bt =1625
    cost_el = 1600
    cost_fc =4000
    cost_ht = 800





    Problem = "DTLZ2"
    M = 2
    # Population, Boundary, Coding = P_objective.P_objective("init", Problem, M, particals)
    # # print(Boundary)
    Boundary = np.array([[4500. ,6000., 4500. ,1500. ,12000.],[ 100. , 100. , 100. , 100. ,1000.]])
    print(type(Boundary))
    ''
    # Boundary =
    max_ = Boundary[0]
    print(max_,'max_')
    min_ = Boundary[1]
    print(min_,'min_')


    # mopso_ = Mopso(particals,max_,min_,thresh,mesh _div) #粒子群实例化
    mopso_ = Mopso_res(particals,max_,min_,thresh,cost_pv=cost_pv,cost_el=cost_el,cost_ht=cost_ht,cost_fc=cost_fc,
                      project_lifetime=project_lifetime,life_time=life_time,cost_bt=cost_bt)
    pareto_in,pareto_fitness = mopso_.done(cycle_) #经过cycle_轮迭代后，pareto边界粒子
    with open("pareto_in_hy_2030_pem{}.txt".format(cost_bt), "w")as f:
        pass
    file_path = os.path.abspath("pareto_in_hy_2030_pem{}.txt".format(cost_bt))

    with open("pareto_fitness_hy_2030_pem{}.txt".format(cost_bt), "w") as f:
        pass
    file_path_fitness = os.path.abspath("pareto_fitness_hy_2030_pem_hy{}.txt".format(cost_bt))
    para = {'pv_cost:': cost_pv, 'el_cost:': cost_el, 'fc_cost': cost_fc, 'cost_ht': cost_ht, 'Boundary:': Boundary,
            'el_eff': 0.75, 'fc_eff': 0.6,'bt_cost':cost_bt}
    with open("pareto_fitness_para_hy{}.txt".format(cost_bt), "w") as f:
        for key, value in para.items():
            f.write('%s:%s\n' % (key, value))

    np.savetxt(file_path,pareto_in)#保存pareto边界粒子的坐标
    np.savetxt(file_path_fitness,pareto_fitness) #打印pareto边界粒子的适应值
    print ("\n","pareto边界的坐标保存于：/img_txt/pareto_in_ht.txt")
    print ("pareto边界的适应值保存于：/img_txt/pareto_fitness_ht.txt")
    print ("\n,迭代结束,over")


 
if __name__ == "__main__":
    main()
