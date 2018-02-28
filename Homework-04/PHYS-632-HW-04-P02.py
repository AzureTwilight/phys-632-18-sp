#!/usr/bin/env python3
"""
PHYS 632 Homework 04
Problem 02
Importance Sampling Monte Carlo

Yaqi Hou
Feb. 21, 2018
"""
import scipy
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_SIZE = int(1e6)

def UniRand(size = 1):
    """
    Wrapper for uniform random number between 0 to 1
    """
    return np.random.random(size)

############
# Part a)  #
############

print("Part a) Expected Result is {:.5f}".format(0.922271))

def changeOfVariable(y):
    return - np.log(1 - (1 - np.exp(-3)) * y)

# f(x) = x^(3/2) e^{-x}
# w(x) = e^{-x}
def f_by_w(x):
    return np.power(x, 1.5) * (1 - np.exp(-3))

randNum1 = UniRand(SAMPLE_SIZE)

samplingResult = f_by_w(changeOfVariable(randNum1))
numericalI = np.mean(samplingResult)

print("\tNumerical Result is {:.5f}".format(numericalI))

################
# Part b) - I  #
################

print("Part b) Expected Results is {:.5f}".format(1.58119))
def changeOfVariable(y, a):
    # x = - ln[1 - (a / A) * y] / a
    # with A / a = 1 - exp(- a * pi)
    return - np.log(1 - ( 1 - np.exp(- a * np.pi)) * y) / a

def f_by_w(x, a):
    A = a / (1 - np.exp(- a * np.pi))
    # f(x) / w(x) = exp(ax) / [A * (x^2 + cos^2 x) ]
    return np.exp(a * x) / A / (np.power(x,2) + np.power(np.cos(x),2))


print("\t a       I         sigma")
print("========================")
for a in np.arange(0.1, 2.001, 0.1):
    randNum1 = UniRand(SAMPLE_SIZE)
    
    samplingResult = f_by_w(changeOfVariable(randNum1, a), a)
    numericalI = np.mean(samplingResult)
    variance = np.sqrt(np.mean(np.power(samplingResult,2)) - np.power(np.mean(samplingResult),2))

    print("\t{:2.1f} | {:6.5f} | {:6.5f}".format(a, numericalI, variance))
