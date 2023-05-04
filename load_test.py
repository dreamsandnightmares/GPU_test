import numpy as np
import matplotlib.pyplot as plt

import numpy as np


def generate_load_data(num_hours, min_load, max_load, max_variation):
    # 生成一个长度为num_hours的随机数列
    load_data = np.random.rand(num_hours)

    # 将随机数列缩放到0到1之间
    load_data = load_data / np.max(load_data)

    # 将0到1之间的数列转换到min_load到max_load之间
    load_data = load_data * (max_load - min_load) + min_load

    # 计算负荷数据的平均值
    mean_load = np.mean(load_data)

    # 计算每个小时的波动幅度
    variation = np.random.rand(num_hours) * max_variation

    # 根据波动幅度和平均值来生成每小时的负荷数据
    load_data = load_data + (mean_load * variation)

    # 将负荷数据限制在min_load到max_load之间
    load_data = np.clip(load_data, min_load, max_load)

    return load_data


load_data = generate_load_data(num_hours=8760, min_load=150, max_load=250, max_variation=0.2)





print(load_data)
np.savetxt("load_data.csv", load_data, delimiter=",")
dist =list(range(len(load_data)))
plt.plot(dist,load_data)
plt.show()