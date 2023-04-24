import matplotlib.pyplot as plot
import numpy as np
import math
from matplotlib.animation import FuncAnimation
import numpy.linalg as lin

# generate a linear trajectory from a set of points using polynomial regression
# specify the speed to drive along the trajectory

def generateLinearTrajectory(points):
    secondList = points
    x = [secondList[i][0] for i in range(len(secondList))]
    y = [points[i][1] for i in range(len(points))]
    a, b = np.polyfit(x, y, 1)
    theta = np.degrees(np.arctan(a))
    secondTheta = 90 - theta
    print(a,"x+", b)
    return a,b,theta,secondTheta


def draw(coefficents):
    xList = []
    yList = []

    listerr = np.linspace()
    for x, y in enumerate(coefficents):
        xList.append()
    fig, ax = plot.subplot()
    animation = FuncAnimation(fig, )





