from OptimizationAlgorithm.MOPSO.public.ma_obj_test import fitness_ht
import numpy as np
cap  = np.array([[1000.,600.,100,1000]])
print(cap)
cost_pv = 4040

cost_el = 1600
cost_fc = 4000
cost_ht = 400
#1.700890340966969461e+03 7.362577108973966915e+02 1.637990522240229438e+02 7.975387556881136334e+03
lcoe = fitness_ht(cap,cost_el=cost_el,cost_ht=cost_ht,cost_fc=cost_fc,cost_pv=cost_pv,project_lifetime=25,life_time=8760)

print(lcoe)