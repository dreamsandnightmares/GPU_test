from OptimizationAlgorithm.MOPSO.public.ma_obj_test import fitness_hy
import numpy as np
cap  = np.array([[2500., 1300, 1000, 600, 7000]])
print(cap)
cost_pv = 4040

cost_bt = 1625
cost_el = 1600
cost_fc = 4000
cost_ht = 100

lcoe = fitness_hy(cap,cost_el=cost_el,cost_bt=cost_bt,cost_ht=cost_ht,cost_fc=cost_fc,cost_pv=cost_pv,project_lifetime=25,life_time=8760)

print(lcoe)