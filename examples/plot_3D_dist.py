import numpy as np
import pandas as pd
import SymPyVol as spv

traj = pd.read_pickle("traj.pkl")
print(traj)
states = traj["state"].__array__(dtype=np.float64)
energies = traj["energy"].__array__(dtype=np.float64)
indices = traj["indices"]
s1,s2 = [],[]
ind = indices.__array__()
for i in range(len(ind)):
    s1.append(int(ind[i][0][0]))
    s2.append(int(ind[i][1][0]))
s1 = np.array(s1,dtype=int)
s2 = np.array(s2,dtype=int)
data = np.matrix([s1, s2, energies])

p = spv.Plot(axis_labels=["sigma1","sigma2","energy"],
        xlim=[np.min(data[0]),np.max(data[0])],
        ylim=[np.min(data[1]),np.max(data[1])],
        zlim=[np.min(data[2]),np.max(data[2])])

p.plot_data(data, size=1, marker="sphere", plot_type="scatter", outPath="./energy_min")



