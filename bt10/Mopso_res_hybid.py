#encoding: utf-8


import sys
import os
curr_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path)  # 父路径
sys.path.append(parent_path)
import numpy as np
from OptimizationAlgorithm.MOPSO.public import init,update,plot,P_objective

import time

from OptimizationAlgorithm.MOPSO.public import ma_obj_test

class Mopso_res:
    def __init__(self,particals,max_,min_,thresh,cost_pv,cost_bt,cost_el,cost_fc,cost_ht,project_lifetime,life_time,mesh_div=10):


        self.mesh_div = mesh_div
        self.particals = particals
        self.thresh = thresh
        self.max_ = max_
        self.min_ = min_
        self.cost_pv =cost_pv
        self.cost_el = cost_el
        self.cost_fc =cost_fc
        self.cost_ht =cost_ht
        self.cost_bt =cost_bt
        self.project_lifetime =project_lifetime
        self.life_time = life_time


        # self.max_v = (max_-min_)*0.5  #速度上限
        # self.min_v = (max_-min_)*(-1)*0.5 #速度下限

        self.max_v = 1000 * np.ones(len(max_), )  # 速度上限,速度不存在上下限，因此设置很大
        self.min_v = -1000 * np.ones(len(min_), )  # 速度下限

        self.plot_ = plot.Plot_pareto()

    def evaluation_fitness(self):
        '只输出 函数值'
        # self.fitness_ = P_objective.P_objective("value", "DTLZ2", 2, self.in_)
        print(self.in_,'in')
        self.fitness_ = ma_obj_test.fitness_hy(self.in_,cost_pv=self.cost_pv,cost_el=self.cost_el,cost_fc=self.cost_fc,
                                               cost_ht=self.cost_ht,
                                         project_lifetime=self.project_lifetime,life_time=self.life_time,cost_bt=self.cost_bt)
        print(self.fitness_,'fitness')
    def evaluation_fitness_olds(self):
        '只输出 函数值'
        # self.fitness_ = P_objective.P_objective("value", "DTLZ2", 2, self.in_)
        print(self.in_,'in')
        self.fitness_ = ma_obj_test.fitness_hy(self.in_,cost_pv=self.cost_pv,cost_el=self.cost_el,cost_fc=self.cost_fc,
                                               cost_ht=self.cost_ht,
                                         project_lifetime=self.project_lifetime,life_time=self.life_time,cost_bt=self.cost_bt)
        print(self.fitness_,'fitness')



    def initialize(self):

        #初始化粒子位置
        self.in_ = init.init_designparams(self.particals,self.min_,self.max_)
        print(self.min_,'min_')
        print(self.max_,'max_')

        #初始化粒子速度
        self.v_ = init.init_v(self.particals,self.max_v,self.min_v)
        #计算适应度ֵ
        self.evaluation_fitness()
        '更新 fitness'
        #初始化个体最优

        print(self.fitness_.shape,'self.fitness_.shape')

        self.in_p,self.fitness_p = init.init_pbest(self.in_,self.fitness_)

        #初始化外部存档
        print(self.fitness_,'fitness')
        self.archive_in,self.archive_fitness = init.init_archive(self.in_,self.fitness_)


        #初始化全局最优
        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in,self.archive_fitness,self.mesh_div,self.particals)
    def update_(self):

        #更新粒子速度、位置、适应度、个体最优、外部存档、全局最优
        self.v_ = update.update_v(self.v_,self.min_v,self.max_v,self.in_,self.in_p,self.in_g)
        self.in_ = update.update_in(self.in_,self.v_,self.min_,self.max_)

        self.evaluation_fitness()

        self.in_p,self.fitness_p = update.update_pbest(self.in_,self.fitness_,self.in_p,self.fitness_p)

        self.archive_in, self.archive_fitness = update.update_archive_1(self.in_, self.fitness_, self.archive_in,
                                                                      self.archive_fitness,
                                                                      self.thresh, self.mesh_div)


        self.in_g,self.fitness_g = update.update_gbest_1(self.archive_in,self.archive_fitness,self.mesh_div,self.particals)

    def done(self,cycle_):
        self.initialize()
        # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,-1)
        since = time.time()
        for i in range(cycle_):
            self.update_()

            print('第',i,'代已完成，time consuming: ',np.round(time.time() - since, 2), "s")

            # self.plot_.show(self.in_,self.fitness_,self.archive_in,self.archive_fitness,i)
        return self.archive_in,self.archive_fitness

