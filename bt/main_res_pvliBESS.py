#encoding: utf-8
import sys
import os
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)

sys.path.append(parent_path)
from Mopso_res_bt import *

 
def main():

    particals = 50 #粒子群的数量
    cycle_ = 100 #迭代次数
    mesh_div = 10 #网格等分数量
    thresh = 300#外部存档阀值
    project_lifetime = 25
    life_time = 8760
    cost_pv = 4040
    cost_bt = 1625





    # Population, Boundary, Coding = P_objective.P_objective("init", Problem, M, particals)
    # # print(Boundary)
    Boundary = np.array([[3500.,9000.],[100.,100.]])
    print(type(Boundary))
    ''
    # Boundary =
    max_ = Boundary[0]
    print(max_,'max_')
    min_ = Boundary[1]
    print(min_,'min_')


    # mopso_ = Mopso(particals,max_,min_,thresh,mesh _div) #粒子群实例化
    mopso_ = Mopso_res(particals,max_,min_,thresh,cost_pv=cost_pv,cost_bt=cost_bt,
                      project_lifetime=project_lifetime,life_time=life_time)


    pareto_in, pareto_fitness = mopso_.done(cycle_)  # 经过cycle_轮迭代后，pareto边界粒子
    with open("pareto_in_bt.txt", "w") as f:
        pass
    file_path = os.path.abspath("pareto_in_bt.txt")

    with open("pareto_fitness_bt.txt", "w") as f:
        pass
    file_path_fitness = os.path.abspath("pareto_fitness_bt.txt")

    para = {'pv_cost:': cost_pv,  'Boundary:': Boundary,
            'el_eff': 0.75, 'fc_eff': 0.6}
    with open("pareto_fitness_para_bt.txt", "w") as f:
        for key, value in para.items():
            f.write('%s:%s\n' % (key, value))
    np.savetxt(file_path, pareto_in)  # 保存pareto边界粒子的坐标
    np.savetxt(file_path_fitness, pareto_fitness)  # 打印pareto边界粒子的适应值
    print ("\n","pareto边界的坐标保存于：/img_txt/pareto_in_olds.txt")
    print ("pareto边界的适应值保存于：/img_txt/pareto_fitness_olds.txt")
    print ("\n,迭代结束,over")

    para = {'pv_cost:': cost_pv, 'bt_cost:': cost_bt, 'Boundary:': Boundary}
    with open("pareto_fitness_para_bt.txt", "w") as f:
        for key,value in para.items():
            f.write('%s:%s\n' % (key, value))



 
if __name__ == "__main__":
    main()
