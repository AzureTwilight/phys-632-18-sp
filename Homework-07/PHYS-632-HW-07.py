# /usr/bin/env python3
#
# HW 07
# Statistical Learning
#
# PHYS 632, Spring 2018

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets

SET_SIZE = 1000
NOISE_AMP = 1

###################################
# Part a) Generate Simulated Data #
# The data is simulated around x2 = x1^2 + 3 * x1 with random noise
# And then lift up/lower by a fixed amount to introduce the separation
###################################

# Generating mask
indArr = np.arange(SET_SIZE)
sample = np.random.choice(indArr, SET_SIZE // 2, replace = False)
mask = np.array([(i in sample) for i in range(SET_SIZE)])

# Choose x1 from -1 to 1
x1 = 2 * (np.random.rand(SET_SIZE) - 0.5)
x2 = 2 * x1**2 + 1 + ( np.random.rand(SET_SIZE) - 0.5) * 2 * NOISE_AMP

# Shift masked part up as part 1
x2[mask] += 1.5
x2[~mask] -= 1.5

# Draw plot of data
plt.scatter(x1[mask],x2[mask], c = 'b', marker = '.')
plt.scatter(x1[~mask],x2[~mask], c = 'r', marker = '.')
plt.title("Distribution of simulated data")
plt.show()

###########################################
# Part b) Marginalize Data & Gaussian KDE #
###########################################

# Marginalization
BINS = 200
hist2D, x1Edge, x2Edge = np.histogram2d(x1,x2, bins = BINS)

x1Center = 0.5 * ( x1Edge[:BINS] + x1Edge[1:])
x2Center = 0.5 * ( x2Edge[:BINS] + x2Edge[1:])
x1Width = np.mean(np.diff(x1Center))
x2Width = np.mean(np.diff(x2Center))

# Marginalize in X1
histX1 = np.sum(hist2D, axis = 1)
histX2 = np.sum(hist2D, axis = 0)

plt.bar(x1Center, histX1, x1Width)
plt.xlabel("X1")
plt.title("Distribution of marginalized data in X2")
plt.show()

plt.bar(x2Center, histX2, x2Width)
plt.title("Distribution of marginalized data in X1")
plt.xlabel("X2")
plt.show()

# Gaussian KDE
NODES = 200

x1Nodes = np.linspace(-1,1, NODES)
x2Nodes = np.linspace(min(x2),max(x2), NODES)

kdeX1 = np.zeros(NODES)
kdeX2 = np.zeros(NODES)

# hX1 = np.mean(np.diff(x1Nodes))
# hX2 = np.mean(np.diff(x2Nodes))

# Use formula for bandwidth -> oversmoothed curve
hX1 = ( 8 * np.sqrt(np.pi) / 3 / NODES / np.sqrt(2) )** (1/5)
hX2 = ( 8 * np.sqrt(np.pi) / 3 / NODES / np.sqrt(2) )** (1/5)


# Use cross-validation to find bandwidth

for i in range(NODES):
    kdeX1[i] = np.sum( np.exp( - ( ( x1Nodes[i] - x1 ) / hX1 ) ** 2 / 2) / np.sqrt(2 * np.pi) ) / NODES / hX1
    kdeX2[i] = np.sum( np.exp( - ( ( x2Nodes[i] - x2 ) / hX2 ) ** 2 / 2) / np.sqrt(2 * np.pi) ) / NODES / hX2

plt.plot(x1Nodes, kdeX1)
plt.title("Distribution of Gaussian KDE with X1 as parameter")
plt.xlabel("X1")
plt.show()

plt.plot(x2Nodes, kdeX2)
plt.title("Distribution of Gaussian KDE with X2 as parameter")
plt.xlabel("X2")
plt.show()

#####################################
# Part c) Support Vector Machine    #
#         v.s.                      #
#         Support Vector Classifier #
#####################################

# # Generate Train Data
trainSample = np.random.choice(indArr, 100, replace = False)

trainData = np.zeros((100,2))
realData = np.c_[x1, x2]
targetData = np.zeros(100)

ind = 0
for ii in trainSample:
    trainData[ind, : ] = [ x1[ii], x2[ii]]
    targetData[ind] = 1 if ii in sample else 0
    ind += 1


# For plotting
x1TrainMin, x1TrainMax = trainData[:, 0].min() - 0.5, trainData[:,0].max() + 0.5 
x2TrainMin, x2TrainMax = trainData[:, 1].min() - 0.5, trainData[:,1].max() + 0.5
h = ( x1TrainMax - x1TrainMin ) / 100
xx, yy = np.meshgrid(np.arange(x1TrainMin, x1TrainMax, h), np.arange(x2TrainMin, x2TrainMax, h))

# SVM

modelPoly = svm.SVC(kernel = 'poly', degree = 5)
modelRadi = svm.SVC(kernel = "rbf")

svcPoly = modelPoly.fit(trainData, targetData)
svcRadi = modelRadi.fit(trainData, targetData)

predPoly = svcPoly.predict(np.c_[xx.ravel(), yy.ravel()])
predPoly = predPoly.reshape(xx.shape)
plt.contourf(xx, yy, predPoly, cmpa = plt.cm.Paired, alpha = 0.8)
plt.scatter(x1, x2, marker = '.', c = 'r')
plt.title("Classification with Polynomial Kernel for SVM")
plt.xlim(xx.min(), xx.max())
plt.show()

predRadi = svcRadi.predict(np.c_[xx.ravel(), yy.ravel()])
predRadi = predRadi.reshape(xx.shape)
plt.contourf(xx, yy, predRadi, cmpa = plt.cm.Paired, alpha = 0.8)
plt.scatter(x1, x2, marker = '.', c = 'r')
plt.title("Classification with Radial Kernel for SVM")
plt.xlim(xx.min(), xx.max())
plt.show()


trainErrorNumber = np.zeros(2)
testErrorNumber = np.zeros(2)

for run in range(100):
    trainSample = np.random.choice(indArr, 100, replace = False)

    trainData = np.zeros((100,2))
    realData = np.c_[x1, x2]
    targetData = np.zeros(100)

    ind = 0
    for ii in trainSample:
        trainData[ind, : ] = [ x1[ii], x2[ii]]
        targetData[ind] = 1 if ii in sample else 0
        ind += 1

    # SVM
    modelPoly = svm.SVC(kernel = 'poly', degree = 5)
    modelRadi = svm.SVC(kernel = "rbf")

    svcPoly = modelPoly.fit(trainData, targetData)
    svcRadi = modelRadi.fit(trainData, targetData)

    testErrorNumber[0] += 1000 * (1 - svcPoly.score(realData, mask))
    testErrorNumber[1] += 1000 * (1 - svcRadi.score(realData, mask))

    trainErrorNumber[0] += 100 * (1 - svcPoly.score(trainData, targetData))
    trainErrorNumber[1] += 100 * (1 - svcRadi.score(trainData, targetData))

testErrorNumber /= 1000
trainErrorNumber /= 100
print("Test Error Number:\n", testErrorNumber)
print("Train Error Number:\n", trainErrorNumber)
