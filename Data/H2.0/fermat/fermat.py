# -*- coding: utf-8 -*-
import numpy as np

fermat_path = "C:/Users/Hang/Desktop/ANN/Zigzag/NoContinuiousZigzag/Data/fermat/fermat.txt"
save_fermat_path = "C:/Users/Hang/Desktop/ANN/Zigzag/NoContinuiousZigzag/Data/fermat/youhua_fermat.txt"

Xmin = -25.5
Ymin = -15.5
paths = np.loadtxt(fermat_path)
print("fermat paths",paths)
for path in paths:
    path[0] = path[0] + Xmin
    path[1] = path[1] + Ymin
    path[2] = 0.40000
np.savetxt(save_fermat_path,paths)

