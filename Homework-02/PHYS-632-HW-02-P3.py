#!/usr/bin/zsh

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

matplotlib.rcParams['text.usetex'] = True
FittedCoeffTemplate = "A = {0:.2f}, \mu = {1:.2f}, \sigma = {2:.2f}"

p1 = 0.35
p2 = p1

N1 = 4
N2 = 40

def poissonPDF(n,v):
    return np.power(v,n) / np.math.factorial(n) * np.exp(-v)

def binomialPDF(n, N, p):
    return np.math.factorial(N) / np.math.factorial(N - n) / np.math.factorial(n) * np.power(p,n) * np.power(1 - p, N - n)

def gaussianPDF(x, *params):
    A, mu, sigma = params
    return A / np.sqrt(2 * np.pi * np.power(sigma,2)) * np.exp(- np.power((x - mu),2) / 2 / np.power(sigma,2) )

sample1 = [n for n in range(N1 + 1)]
sample2 = [n for n in range(N2 + 1)]

smoothX1 = np.linspace(0,N1, 100)
smoothX2 = np.linspace(0,N2, 1000)

poisson1 = [ poissonPDF(n, p1 * N1) for n in sample1 ]
binomial1 = [ binomialPDF(n, N1, p1) for n in sample1 ]

poisson2 = [ poissonPDF(n, p2 * N2) for n in sample2 ]
binomial2 = [ binomialPDF(n, N2, p2) for n in sample2 ]

############
## Part I ##
############
params0 = [1., 0., 1.]

coeffFitted, varMatrix = curve_fit(gaussianPDF,sample1, poisson1, p0=params0)
gaussianFitted = [gaussianPDF(n, *coeffFitted) for n in smoothX1]

plt.bar(sample1, poisson1, 0.3, color='gray')
plt.plot(sample1, poisson1, 'ro-', label = 'Binomial')
plt.plot(smoothX1, gaussianFitted, 'g.:', label = 'Fitted Gaussian')
titleText = FittedCoeffTemplate.format(coeffFitted[0], coeffFitted[1], coeffFitted[2])
plt.title('The Poisson p.d.f. and Fitted Gaussian \n with ' + titleText)
plt.legend()
plt.savefig('poisson-1.png')
plt.show()

coeffFitted, varMatrix = curve_fit(gaussianPDF,sample1, binomial1, p0=params0)
gaussianFitted1 = [gaussianPDF(n, *coeffFitted) for n in smoothX1]

plt.bar(sample1, binomial1, 0.3, color='gray')
plt.plot(sample1, binomial1, 'ro-', label = 'Binomial')
plt.plot(smoothX1, gaussianFitted1, 'g.:', label = 'Fitted Gaussian')
titleText = FittedCoeffTemplate.format(coeffFitted[0], coeffFitted[1], coeffFitted[2])
plt.title('The Binomial p.d.f. and Fitted Gaussian \n with ' + titleText)
plt.legend()
plt.savefig('binomial-1.png')
plt.show()

#############
## Part II ##
#############
coeffFitted, varMatrix = curve_fit(gaussianPDF,sample2, poisson2, p0=params0)
gaussianFitted = [gaussianPDF(n, *coeffFitted) for n in smoothX2]

plt.bar(sample2, poisson2, 0.3, color='gray')
plt.plot(sample2, poisson2, 'ro-', label = 'Binomial')
plt.plot(smoothX2, gaussianFitted, 'g.:', label = 'Fitted Gaussian')
titleText = FittedCoeffTemplate.format(coeffFitted[0], coeffFitted[1], coeffFitted[2])
plt.title('The Poisson p.d.f. and Fitted Gaussian \n with ' + titleText)
plt.legend()
plt.savefig('poisson-2.png')
plt.show()

coeffFitted, varMatrix = curve_fit(gaussianPDF,sample2, binomial2, p0=params0)
gaussianFitted = [gaussianPDF(n, *coeffFitted) for n in smoothX2]

plt.bar(sample2, binomial2, 0.3, color='gray')
plt.plot(sample2, binomial2, 'ro-', label = 'Binomial')
plt.plot(smoothX2, gaussianFitted, 'g.:', label = 'Fitted Gaussian')
titleText = FittedCoeffTemplate.format(coeffFitted[0], coeffFitted[1], coeffFitted[2])
plt.title('The Binomial p.d.f. and Fitted Gaussian \n with ' + titleText)
plt.legend()
plt.savefig('binomial-2.png')
plt.show()
