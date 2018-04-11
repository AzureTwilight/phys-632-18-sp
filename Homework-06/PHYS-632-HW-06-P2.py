#! /usr/bin/env python3
#
# Statistical Learning
#
#
# Yaqi Hou
# Spr. 2018

import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand as uniRand
from numpy.random import choice
from numpy.random import poisson as getPoisson
from scipy.stats import chi2
from prettytable import PrettyTable


################
# Read in data #
################

with open('prob_6_2.dat','r') as fp:
    lines = fp.readlines()

dataList = []
t1List = []
t2List = []
dataFlag = False
t1Flag = False
t2Flag = False
for line in lines:
    if line[0] == '/':
        # Comments Line
        if 'data' in line:
            dataFlag = True
            t1Flag = False
            t2Flag = False
        elif 'theory 1' in line:
            dataFlag = False
            t1Flag = True
            t2Flag = False
        elif 'theory 2' in line:
            dataFlag = False
            t1F了ag = False
            t2Flag = True
    else:
        if dataFlag:
            tmp = line.split()
            tmp = [float(x) for x in tmp]
            dataList.append(tmp)
        if t1Flag:
            tmp = line.split()
            tmp = [float(x) for x in tmp]
            t1List.append(tmp)
        if t2Flag:
            tmp = line.split()
            tmp = [float(x) for x in tmp]
            t2List.append(tmp)
        
binNumber = len(dataList)


t1nuList = [None] * binNumber
t2nuList = [None] * binNumber
datanuList = [None] * binNumber
err1List = [None] * binNumber
err2List = [None] * binNumber

for i in range(binNumber):
    t1nuList[i] = t1List[i][2]
    t2nuList[i] = t2List[i][2]
    datanuList[i] = dataList[i][2]
    err1List[i] = abs(t1nuList[i] - datanuList[i])
    err2List[i] = abs(t2nuList[i] - datanuList[i])


plt.bar(np.linspace(0,10,21)[:20], datanuList, width = 0.5, align = 'edge', yerr = err1List, color = 'none', edgecolor = 'blue', label = 'Data')
plt.bar(np.linspace(0,10,21)[:20], t1nuList, width = 0.5, align = 'edge', color = 'None', edgecolor = 'orange', label = "Theory 1")
plt.title("Histogram for Data and Theory 1 with error bar")
plt.legend()
plt.show()

plt.bar(np.linspace(0,10,21)[:20], datanuList, width = 0.5, align = 'edge', yerr = err1List, color = 'none', edgecolor = 'blue', label = 'Data')
plt.bar(np.linspace(0,10,21)[:20], t2nuList, width = 0.5, align = 'edge', color = 'None', edgecolor = 'orange', label = "Theory 2")
plt.title("Histogram for Data and Theory 2 with error bar")
plt.legend()
plt.show()
#--------------------------------#

# Pearson chi-square
chiSquareData1 = 0
chiSquareData2 = 0
for ind in range(binNumber):
    chiSquareData1 += (dataList[ind][2] - t1List[ind][2])** 2 / t1List[ind][2]
    chiSquareData2 += (dataList[ind][2] - t2List[ind][2])** 2 / t2List[ind][2]

DOF = binNumber

pValue1 = 1 - chi2.cdf(chiSquareData1, DOF)
pValue2 = 1 - chi2.cdf(chiSquareData2, DOF)

print("pValue1 from Data is {:.4f}, chi-2 is {:.4f}".format(pValue1, chiSquareData1))
print("pValue2 from Data is {:.4f}, chi-2 is {:.4f}".format(pValue2, chiSquareData2))

#--------------------------------#

SIM_NUMBER = int(1e5)
chiTrueDist1 = [None] * SIM_NUMBER
chiTrueDist2 = [None] * SIM_NUMBER

print("Simulating data...")
for i in range(SIM_NUMBER):
    # Generate new data
    tmpData1 = [None] * binNumber
    tmpData2 = [None] * binNumber
    for b in range(binNumber):
        tmpData1[b] = getPoisson(t1List[b][2])
        tmpData2[b] = getPoisson(t2List[b][2])
        
    # Calculate chi-square
    chiSquare1 = 0
    chiSquare2 = 0
    for ind in range(binNumber):
        chiSquare1 += (tmpData1[ind] - t1List[ind][2])** 2 / t1List[ind][2]
        chiSquare2 += (tmpData2[ind] - t2List[ind][2])** 2 / t2List[ind][2]

    chiTrueDist1[i] = chiSquare1
    chiTrueDist2[i] = chiSquare2
print("Done.")

bins = np.linspace(0, 80, 500)
(dist1, _, _) = plt.hist(chiTrueDist1, bins = bins, density = True)
plt.title("Generated True Distribution for Theory 1")
plt.show()

diff = [abs(x - chiSquareData1) for x in bins]
ind = diff.index(min(diff))
pValue1 = sum(dist1[:ind]) * (bins[1] - bins[0])


(dist2, _, _)= plt.hist(chiTrueDist2, bins = bins, density = True)
plt.title("Generated True Distribution for Theory 2")
plt.show()

diff = [abs(x - chiSquareData2) for x in bins]
ind = diff.index(min(diff))
pValue2 = sum(dist2[:ind])  * (bins[1] - bins[0])
    
print("pValue1 from Simulated Events is {:.4f}".format(pValue1))
print("pValue2 from Simulated Events is {:.4f}".format(pValue2))

#-----------------------------#

SIM_NUMBER = int(1e4)

print("Generating Sample Events")
t1nuList = [None] * binNumber
for i in range(binNumber):
    t1nuList[i] = t1List[i][2]

totalNu = sum(t1nuList)
# The pdf is step-wise, with width as the bin width 0.5
t1pdfList = [x / totalNu / 0.5 for x in t1nuList]
weight = max(t1pdfList)

# Generate with A/R Method
events = [None] * SIM_NUMBER
success = 0
run = 0
while success < SIM_NUMBER:

    run += 1
    if run > 100 * SIM_NUMBER:
        print("Takes too long...")
        break

    p = 10 * uniRand()
    r = uniRand()

    pPdf = t1pdfList[min(int(p // 0.5), 19)]

    if r < pPdf / weight:
        events[success] = p
        success += 1
print("Done.")
    
    
# A quick check
plt.hist(events, bins = np.linspace(0,10,20), density = True)
plt.plot(np.linspace(0,10,20), t1pdfList)
plt.show()

# #----------------------------#

SET_NUM = 100
EVN_NUM = 100

bins = np.linspace(0,10, 21)
totalHist = [0] * binNumber
for ind in range(SET_NUM):
    subevents = choice(events, EVN_NUM)
    hist = np.histogram(subevents, bins = bins)

    for ind in range(binNumber):
        totalHist[ind] += hist[0][ind]
    
totalHist = [x / 10000 / 0.5 for x in totalHist]

plt.plot(np.linspace(0,10,20), totalHist, label = "Simulated Events")
plt.plot(np.linspace(0,10,20), t1pdfList, label = "Theory 1")
plt.legend()
plt.show()
