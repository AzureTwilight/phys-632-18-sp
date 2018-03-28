# /usr/bin/python3
#
# PHYS 632 Spring 2018
# Homework 05 - Problem 01
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

DATA_H0 = np.matrix([[0,1,5], [1,2,5], [2,3,4], [3,3,7], [4,5,6], [5,5,5]])
DATA_H1 = np.matrix([[1,0,4], [2,1,3], [3,1,5], [3,2,4], [5,3,4], [6,5,6]])

##################################
# Part a)                        #
# Calculate means and covariance #
##################################
meanValH0 = np.mean(DATA_H0, axis=0)
meanValH1 = np.mean(DATA_H1, axis=0)
print("Mean Value")
print("H0:", meanValH0)
print("H1:", meanValH1)

covMatH0 = np.cov(DATA_H0, rowvar = False)
covMatH1 = np.cov(DATA_H1, rowvar = False)

print("Covariance Matrices")
print("H0:\n", covMatH0)
print("H1:\n", covMatH1)

##############################
# Part b)                    #
# Fisher Linear Discriminant #
##############################

matW = covMatH0 + covMatH1
matWinv = np.linalg.inv(matW)

veca = matWinv * (meanValH0 - meanValH1).T

print("FLD Coefficients:")
print("Veca:", veca.T)

tH0 = DATA_H0 * veca
tH1 = DATA_H1* veca

print(tH0)
print(tH1)

tauH0 = meanValH0 * veca
tauH1 = meanValH1 * veca

print(tauH0, tauH1)

sigmaH0 = veca.T * covMatH0 * veca
sigmaH1 = veca.T * covMatH1 * veca

print(sigmaH0, sigmaH1)

sigmaH0 = np.sqrt(sigmaH0)
sigmaH1 = np.sqrt(sigmaH1)

def GaussianPDF(x,mu,sigma):
    return np.exp(- np.power(x - mu, 2) / (2 * np.power(sigma,2))) / np.sqrt(2 * np.pi * np.power(sigma, 2))

pltx = np.linspace(-20, 20, 500).reshape(500,1)
pltyH0 = GaussianPDF(pltx, tauH0, sigmaH0)
pltyH1 = GaussianPDF(pltx, tauH1, sigmaH1)

plt.plot(pltx, pltyH0, 'r', label = "H0")
plt.plot(pltx, pltyH1, 'b', label = "H1")
plt.legend()
plt.show()

###################
# Part c)         #
# Hypotheses Test #
###################

significanceLevel = integrate.quad(lambda x: GaussianPDF(x, tauH0, sigmaH0), 1, 20)
print(significanceLevel[0])

probErrorSecondKind = integrate.quad(lambda x: GaussianPDF(x, tauH1, sigmaH1), 1, 20)
print(probErrorSecondKind[0])

power = 1 - probErrorSecondKind[0]
print(power)
