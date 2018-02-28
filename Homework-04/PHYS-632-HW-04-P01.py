#!/usr/bin/env python3
"""
PHYS 632 Homework 04
Problem 01
RNG obeying Gaussian Distribution with MC

Yaqi Hou
Feb. 21, 2018
"""
import random
import time
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import pprint

MU = 0.0
SIGMA  = 1.0
SAMPLE_SIZE = 10000

BINS = 100

reportDict = dict()

def UniRand(size = 1):
    """
    Wrapper for uniform random number between 0 to 1
    """
    return np.random.random(size)

def FittingFunction(x, mu, sigma):
    return 1 / np.sqrt(2 * np.pi * sigma**2) * np.exp(- (x - mu)**2 / 2 / sigma**2)

def FitAndDraw(data, bins = BINS, title = None):
    hist, edges = np.histogram(data, bins = bins, density = True)

    # Get Center from Edges
    centers = (edges[:-1] + edges[1:] ) / 2

    coeff, var = curve_fit(FittingFunction, centers, hist, p0 = [0.0, 1.0])

    plt.hist(data, bins=BINS, density = True)
    labelText = "mu = {:.3f}, sigma = {:.3f}".format(*coeff)
    plt.plot(centers, FittingFunction(centers, *coeff), "r:", label = labelText)
    plt.legend()
    if title:
        plt.title(title)
    plt.show()

    return coeff

#############################
# Part a) Box-Muller Method #
#############################

print("Generating Random Number with Box-Muller Method...")
## Unoptimized Version: Picking Random Number in Unit Square

tstart = time.clock()
randNum1 = UniRand(int(SAMPLE_SIZE / 2)) 
randNum2 = UniRand(int(SAMPLE_SIZE / 2))

rho = -np.log(randNum1) # Generate rho: exponential distribution
theta = 2 * np.pi * randNum2 # Generate theta: uniform distribution between 0 to 2*pi

# Origin Version for Generating
x = SIGMA * np.sqrt(2 * rho) * np.cos(theta) + MU
y = SIGMA * np.sqrt(2 * rho) * np.sin(theta) + MU

randomResult = np.append(x,y)
tcost = time.clock() - tstart
coeff = FitAndDraw(randomResult, title = "Box-Muller Method")
reportDict.update({'pa' : np.append(coeff,tcost)})

########################################
# Part b) Neumann Acceptance-Rejection #
########################################
print("Generating Random Numbers with A/R Method...")

def GaussianPDF(x, sigma=SIGMA, mu=MU):
    return 1 / np.sqrt(2 * np.pi * sigma**2) * np.exp(- (x - mu)**2 / 2 / sigma**2)

# Step 1 | Choose w(x): here we choose a "box"
def weightPDF(x, sigma=SIGMA, mu=MU):
    maxGaussianPDF = 1 / np.sqrt(2 * np.pi * sigma**2)
    # weight =( - np.power((x - mu),2) + 25 ) * maxGaussianPDF / 25
    weight = maxGaussianPDF
    return weight 

tstart = time.clock()
randomResult = np.zeros(SAMPLE_SIZE)
successCount = 0
runCount = 0
while successCount < SAMPLE_SIZE:

    runCount = runCount + 1
    if runCount > 10 * SAMPLE_SIZE:
        print("                          ", end = "\r")
        print("Takes too long.")
        break
    # Step 2 | Generate Uniform Random Number within [min and max]
    r = UniRand()

    # Step 3 | Generate Random Number p: w(x)
    p = 10 * UniRand() - 5

    # Step 4&5 | Comparision of r and f(p) / w(p)
    if r < GaussianPDF(p, SIGMA, MU) / weightPDF(p):
        randomResult[successCount] = p
        successCount = successCount + 1
        print("Finished {:d} out of {:d}".format(successCount, SAMPLE_SIZE), end = "\r")

print("                                   ", end = "\r")

tcost = time.clock() - tstart
coeff = FitAndDraw(randomResult, title = "Accept/Rejection Method")
reportDict.update({'pb' : np.append(coeff,tcost)})
# plt.hist(randomResult, bins = BINS)
# plt.show()

#############################
# Part c) Metropolis Method #
#############################
def GaussianPDF(x, sigma = SIGMA, mu = MU):
    return 1 / np.sqrt(2 * np.pi * sigma**2) * np.exp(- (x - mu)**2 / 2 / sigma**2)

print("Generating Random Numbers with Metropolis Method...")

tstart = time.clock()
STEP_SIZE = 1

randomResult = np.zeros(SAMPLE_SIZE)
ind = 0
for ind in range(1,SAMPLE_SIZE): # take x0 = 0
    delta = 2 * UniRand() - 1

    x0 = randomResult[ind - 1]
    xT = x0 + delta * STEP_SIZE

    probabilityRatio = GaussianPDF(xT) / GaussianPDF(x0)
    if probabilityRatio >= 1:
        randomResult[ind] = xT
    else:
        r = UniRand()
        if r > probabilityRatio:
            randomResult[ind] = x0
        else:
            randomResult[ind] = xT

    print("Finished {:d} out of {:d}".format(ind+1, SAMPLE_SIZE), end = "\r")

tcost = time.clock() - tstart
coeff = FitAndDraw(randomResult, title = "Metropolis Method")
reportDict.update({'pc' : np.append(coeff,tcost)})
# plt.hist(randomResult, bins = BINS)
# plt.show()

###########################
# Part d) Given Algorithm #
###########################
print("Generating Random Numbers with Given Method...")

tstart = time.clock()
randomResult = np.zeros(SAMPLE_SIZE)
n = 12
for ind in range(SAMPLE_SIZE):
    randomResult[ind] = np.sum(UniRand(n))
    print("Finished {:d} out of {:d}".format(ind+1, SAMPLE_SIZE), end = "\r")

randomResult = randomResult - n / 2
    
tcost = time.clock() - tstart
coeff = FitAndDraw(randomResult, title = "Summation of Random Variable")
reportDict.update({'pd' : np.append(coeff,tcost)})
# plt.hist(randomResult, bins = BINS)
# plt.show()

pprint.pprint(reportDict)
