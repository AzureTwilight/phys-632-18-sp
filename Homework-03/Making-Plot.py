#! /usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

err = []
h = []

with open("p2-ptb-data.txt", "r") as f:
    lines = f.readlines()[1:]
    for line in lines:
        split_result = line.replace("\\\\", "").split("&")
        err.append(float(split_result[3]))
        h.append(float(split_result[1]))

slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(h), np.log(err))
        
plt.text(-6,-2, "f(x)={:.2f} * x + {:.2f}\nR^2 = {:.4f}".format(slope,intercept, r_value**2))
plt.plot(np.log(h), np.log(err), 'bo-')
plt.xlabel("log(h)")
plt.ylabel("log(err)")
plt.title("Log-log Plot for Relative Error vs Step Size")

plt.show()

# err = []
# n = []

# with open("p2-ptd-data.txt", "r") as f:
#     lines = f.readlines()[1:]
#     for line in lines:
#         split_result = line.replace("\\\\", "").split("&")
#         err.append(float(split_result[2]))
#         n.append(float(split_result[0]))

# fitted_coeff = np.polyfit(n, err, 1)
# print(fitted_coeff)
        
# plt.plot(np.log(n), np.log(err), 'bo-')
# plt.xlabel("log(n)")
# plt.ylabel("log(err)")
# plt.title("Log-log Plot for Relative Error vs Sample Size")

# plt.show()

# err = []
# n = []

# with open("p04-data.txt", "r") as f:
#     lines = f.readlines()[1:]
#     for line in lines:
#         split_result = line.replace("\\\\", "").split("\t")
#         err.append(float(split_result[1]))
#         n.append(float(split_result[0]))

# slope, intercept, r_value, p_value, std_err = stats.linregress(1./np.sqrt(n), err)
# print(slope)
# print(intercept)

# print(r_value**2)

        
# plt.plot(1./ np.sqrt(n), err, 'bo')
# plt.plot(1./np.sqrt(n), intercept + slope / np.sqrt(n), 'r-')
# plt.xlabel("1/sqrt(n)")
# plt.ylabel("Absolute Error")
# plt.text(0.05,2.5, "f(x)={:.2f} * x + {:.2f}\nR^2 = {:.4f}".format(slope,intercept, r_value**2))
# plt.title("Absolute Error vs 1/SQRT(n)")

# plt.savefig("p04-plot.png")
# plt.show()
