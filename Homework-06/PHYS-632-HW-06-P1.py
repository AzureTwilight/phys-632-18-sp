#! /usr/bin/env python3
#
# Optimization: Perform a minimization of Rosenbrock's Function of n = 2
# using Simplex method
#
# Yaqi Hou
# Spr. 2018

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from prettytable import PrettyTable
# from scipy.optimize import 

a = 3.1578
b = 20

def rosefunc(p, a = a, b = b):
    return (a - p[0]) ** 2 + b * (p[1] - p[0] ** 2)**2

N = 2 # dimension n = 2
FTOL = 1e-6

scale = 10  # lambda, the scaling factor
p0 = np.array([-1.0, 1.0])
plist = [p0]
# Generate the other 2 points
p1 = p0 + np.array([1, 0]) * scale
p2 = p0 + np.array([0, 1]) * scale
plist.append(p1)
plist.append(p2)

phist = []
# For output
t = PrettyTable(["Steps", "Lowest Point", "min", "mid", "max", "Diff"])
# Remove max from p
difference = 1
step = 1
while difference > FTOL:
    flist = []
    indTmp = [0,1,2]
    for p in plist:
        flist.append(rosefunc(p))
    maxInd = flist.index(max(flist))
    indTmp.remove(maxInd)
    minInd = flist.index(min(flist))
    indTmp.remove(minInd)
    midInd = indTmp[0]
    pbar = (sum(plist) - plist[maxInd]) / 2
    pl = plist[minInd]

    difference = flist[maxInd] - flist[minInd]

    t.add_row([step, "({:.3f},{:.3f})".format(plist[minInd][0], plist[minInd][1]), "{:.2e}".format(flist[minInd]), "{:.2e}".format(flist[midInd]), "{:.2e}".format(flist[maxInd]), "{:.2e}".format(difference)])
    phist.append(plist[minInd])
    # print("Step {0:d}:\n\tLowest Point: ({1:.2f},{1:.2f}) ".format(step, plist[minInd][0], plist[minInd][1]))
    # print("Difference: ", difference)
    step += 1


    pnew = pbar + (pbar - plist[maxInd])
    fnew = rosefunc(pnew)
    fl = rosefunc(pl)
    
    if fnew < fl:
        # Reflection point is better
        # try reflection and expansion
        ptry = pbar + 2 * (pbar - plist[maxInd])
        ftry = rosefunc(ptry)
        if ftry < fnew:
            pnew = ptry

        # update simplex
        plist[maxInd] = pnew
    else:
        # Reflection point is not the best
        # try 1d contraction
        ptry = (pbar + plist[maxInd]) / 2
        ftry = rosefunc(ptry)

        if ftry >= flist[maxInd]:
            # The Contraction is no better than highest
            # Take multiple contraction around lowest
            scale *= 0.5
            plist[0] = plist[minInd]
            plist[1] = plist[minInd] + np.array([1,0]) * scale
            plist[2] = plist[minInd] + np.array([0,1]) * scale
        else:
            # 1D contraction is smaller than highest
            pnew = ptry
            # update simplex
            plist[maxInd] = pnew


print(t)

# Compare to scipy.optimize result
x0 = [-1, 1]
res = minimize(rosefunc, x0, method = 'nelder-mead', options={'xtol': FTOL, 'disp': True})
print(res.x)

# Making Plots
xlimit = a * 1.3 
ylimit = a**2 * 1.3 
number = 100
x1 = np.linspace(-xlimit,xlimit,number)
x2 = np.linspace(-ylimit,ylimit,number)
Z = np.zeros((number,number))
for i in range(number):
    for j in range(number):
        Z[i][j] = rosefunc([x1[i],x2[j]])
plt.contour(x1, x2, Z, 30)

plt.plot(a, a**2, "ro")

for point in phist:
    plt.plot(point[0], point[1], 'k.')

plt.title("Contour Plot for 2D Rosenbrock Function")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

