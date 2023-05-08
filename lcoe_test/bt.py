from OptimizationAlgorithm.MOPSO.public.ma_obj_test import fitness_bt
import numpy as np
cap  = np.array([[1000,1267]])
print(cap)
cost_pv = 4040
cost_bt = 1625


lcoe = fitness_bt(cap,cost_bt=cost_bt,cost_pv=cost_pv,project_lifetime=25,life_time=8760)

print(lcoe)