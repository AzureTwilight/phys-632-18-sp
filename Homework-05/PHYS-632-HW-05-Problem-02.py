#! /usr/bin/python3

from scipy.optimize import minimize_scalar
from scipy.optimize import brentq
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

############################
# Global Constant Variable #
############################
SIMULATION_NUM = 1000
DATASET_SIZE_LIST = [2, 4, 8, 16, 32, 64, 128, 500, 1000]
M0 = 0.8
GAMMA = 1

def GetCauchyPDF(m, m0 = M0, gamma = GAMMA):
    return (gamma) / ( np.power( m - m0, 2) + np.power(gamma / 2, 2) ) / 2 / np.pi

############################################
# STEP 1 | Generate Simulated Mearusements #
#-------------------------------------------
# Use Acceptance-Rejection Algorithm
# Truncate the range of m within [-5, 5]
############################################
simulatedData = np.zeros(SIMULATION_NUM)

# Choose w(x) as uniform (a box)
weightFunction = GetCauchyPDF(M0)

ind = 0
runNum = 0
while ind < SIMULATION_NUM:

    r = np.random.rand()
    p = np.random.rand() * 10 - 5
    if r < GetCauchyPDF(p) / weightFunction:
        simulatedData[ind] = p
        ind += 1 

    runNum += 1
    # If the efficiency is less than 1%
    if runNum > 100 * SIMULATION_NUM:
        raise ValueError("Too many runs when simulating data, try a different weighting function." + str(runNum))

# Check the distribution of simulated data
# tmpx = np.linspace(-5,5, 150)
# plt.hist(simulatedData, bins = tmpx, density = True)
# plt.plot(tmpx, GetCauchyPDF(tmpx) ) 
# plt.show()

# Initialize Result Array
MMResult = np.empty((len(DATASET_SIZE_LIST)))
MMResult[:] = np.nan
MLResult = np.empty((len(DATASET_SIZE_LIST)))
MLResult[:] = np.nan
MMMeanResult = np.empty((len(DATASET_SIZE_LIST)))
MMMeanResult[:] = np.nan

ind = 0
for i in DATASET_SIZE_LIST:
    dataset = simulatedData[:i]
    
    #############################################
    # STEP 2 | Method of Moments to Estimate m0 #
    #--------------------------------------------
    # Use sample mean estimator to estimate m0
    # though this is not correct
    #############################################
    MMResult[ind] = np.median(dataset)
    MMMeanResult[ind] = np.mean(dataset)

    # STEP 3
    # Aim is to minimize "sum of ln[ (m_i - m0)^2 + (gamma/2)^2 ]"

    def MinusLikelihoodFunction(m0):
        return sum( np.log(np.power(dataset - m0, 2) + 0.25) ) + i * np.log(2 * np.pi)

    res = minimize_scalar(MinusLikelihoodFunction)
    bestEstimate = res.x
    MLResult[ind] = bestEstimate 
    ind += 1

    # STEP 4
    # Get uncertainty
    if i == 64 or i == 1000:
        def UncertaintyBoundFunction(m0, bestEstimate = bestEstimate):
            tmp = sum( np.log(np.power(dataset - m0, 2) + 0.25) ) + i * np.log(2 * np.pi)
            tmp2 = sum( np.log(np.power(dataset - bestEstimate, 2) + 0.25) ) + i * np.log(2 * np.pi)
            return  ( - tmp + 0.5 + tmp2)
        upperBound = brentq(UncertaintyBoundFunction, bestEstimate, 1.5)
        lowerBound = brentq(UncertaintyBoundFunction, 0.1, bestEstimate)
        uncertainty = max(abs(bestEstimate - lowerBound), abs(bestEstimate - upperBound))


        print("i = {0:d} :\n\tBest Estimate: {1:.4f}, Lower Bound: {2:.4f}, Upper Bound: {3:.4f}\n\t => {4:.4f} +/- {5:.4f}".format(i, bestEstimate, lowerBound, upperBound, bestEstimate, uncertainty))

        pltx = np.linspace(bestEstimate - 3 * uncertainty,bestEstimate + 3 * uncertainty,100)

        plty = []
        for ind2 in range(len(pltx)):
            plty.append(- MinusLikelihoodFunction(pltx[ind2]))
        plt.plot(pltx, plty)
        plt.plot([lowerBound, upperBound], [- MinusLikelihoodFunction(upperBound), - MinusLikelihoodFunction(lowerBound)])
        plt.ylabel("Ln-likelihood Function")
        plt.xlabel("M_0")
        plt.show()

# Print out results
t = PrettyTable(["i", "MM", "ML", "MM Mean"])
for ind in range(len(DATASET_SIZE_LIST)):
    t.add_row([DATASET_SIZE_LIST[ind], '{:.4f}'.format(MMResult[ind]), '{:.4f}'.format(MLResult[ind]), '{:.4f}'.format(MMMeanResult[ind])] )
print("\n",t)
