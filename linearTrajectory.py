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


def draw(coefficents, points):
    xList = []
    yList = []

    for x in range(round(points[1][0])):
         elementsY = coefficents[0] * x + coefficents[1]
         yList.append(elementsY)
         xList.append(x)

    fig, ax = plot.subplot()
    animation = FuncAnimation(fig, )


def drawTwo(points):
    xList = np.linspace(0, points[1][0], 50)
    yList = np.linspace(0, points[1][1], 50)
    animation = plot.plot(xList,yList)
    fig, ax = plot.subplot()
    anim = FuncAnimation(fig, animation, interval=700)
    plot.show()
    


points = np.array([(0,0), (13, 17)], dtype=np.float32)
drawTwo(points)


