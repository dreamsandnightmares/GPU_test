#encoding: utf-8
import numpy as np
from test2.OptimizationAlgorithm.hybrid_olds.Mopso_res_hybid import Mopso_res
from test2.OptimizationAlgorithm.MOPSO.public.P_objective import  P_objective
from Mopso_res_hybid import *
import os
import sys
dir_now = sys.path[0]

dis_up = os.path.dirname(dir_now)
dis_upuo = os.path.dirname(dis_up)

sys.path.append(os.path.dirname(dir_now))
sys.path.append(dis_up)
sys.path.append(dis_upuo)



 
def main():

    particals = 30 #粒子群的数量
    cycle_ = 50 #迭代次数
    mesh_div = 10 #网格等分数量
    thresh = 300#外部存档阀值

    project_lifetime = 25
    life_time = 8760
    cost_pv = 3610
    cost_bt = 700

    cost_el = 2000
    cost_fc = 400
    cost_ht = 15




    Problem = "DTLZ2"
    M = 2
    # Population, Boundary, Coding = P_objective.P_objective("init", Problem, M, particals)
    # # print(Boundary)
    Boundary = np.array([[2500., 6000, 6000., 6000, 13000], [400., 200, 200., 300, 800]])
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
    with open("pareto_in_hy_olds_2030_pem.txt", "w") as f:
        pass
    file_path = os.path.abspath("pareto_in_hy_olds_2030_pem.txt")

    with open("pareto_fitness_hy_olds2030_pem.txt", "w") as f:
        pass
    file_path_fitness = os.path.abspath("pareto_fitness_hy_olds2030_pem.txt")


    np.savetxt(file_path,pareto_in)#保存pareto边界粒子的坐标
    np.savetxt(file_path_fitness,pareto_fitness) #打印pareto边界粒子的适应值
    print ("\n","pareto边界的坐标保存于：/img_txt/pareto_in_ht.txt")
    print ("pareto边界的适应值保存于：/img_txt/pareto_fitness_ht.txt")
    print ("\n,迭代结束,over")


 
if __name__ == "__main__":
    main()
