#! /usr/bin/zsh

import random
import matplotlib.pyplot as plt

simulationNumber = 2000
peopleNumber = 5
numberOfOccurrences = [0] * 200

averageFlipNumber = 0
for ii in range(simulationNumber):

    flipNumber = 0
    while True:
        flipNumber += 1
        flipResult =  0

        for pp in range(peopleNumber - 1):
            flipResult += random.randint(0,1)

        if random.random() < 0.9:
            flipResult += 1
        
        # flipResultList = [random.randint(0,1) for x in range(peopleNumber)]
        # flipResult = sum(flipResultList)

        if flipResult == 1 or flipResult == 4:
            numberOfOccurrences[flipNumber] += 1
            break
    
    averageFlipNumber += flipNumber

averageFlipNumber = averageFlipNumber / simulationNumber
print("The average flip number is " + str(averageFlipNumber))

lastNoneZeroIdx = next((len(numberOfOccurrences) - idx for idx, item in enumerate(reversed(numberOfOccurrences), 1) if item), None)

if lastNoneZeroIdx == None:
    print("Error, Cannot find non zero index")

plt.plot(numberOfOccurrences[1:lastNoneZeroIdx],"o:")
plt.ylabel("Number of Occurences")
plt.xlabel("Game Length")
plt.title("Number of Occurences vs Duration of Games")
plt.savefig("problem-1.png")
plt.show()

