import matplotlib.pyplot as plot
import numpy as np
import math
from matplotlib.animation import FuncAnimation
import numpy.linalg as lin

# generate a linear trajectory from a set of points using polynomial regression
# returns coefficents of the function of points, and the angle of the line relative to the postive
# x, and positive y axes. All these form a 1d tuple of (coefficent1, coefficent 2, theta1, theta).
# where coefficents1 and 2 represents the equation y=mx+b, m is coefficent1, b is coefficent2.

def generateLinearTrajectory(points):
    secondList = points
    x = [secondList[i][0] for i in range(len(secondList))]
    y = [points[i][1] for i in range(len(points))]
    a, b = np.polyfit(x, y, 1)
    theta = np.degrees(np.arctan(a))
    secondTheta = 90 - theta
    return a,b,theta,secondTheta


def draw(coefficents, points):
    yList = []
    x_points = np.linspace(points[0][0], points[1][0], 10)

    for x in x_points:
        elementsY = (coefficents[0] * x) + coefficents[1]
        yList.append(elementsY)

    fig, ax = plot.subplots()

    ax.set_xlim(0, 250)
    ax.set_ylim(0, 100)

    line = ax.plot(points[0][0], points[0][1])

    line.set_xdata(x_points)
    line.set_ydata(yList)
    
    animation = plot.plot(x_points, yList)
    anim = FuncAnimation(fig, func=line, frames=np.arange(0, 10, 0.01),  interval=10)
    plot.show()

points = np.array([(0,0), (13, 17)], dtype=np.float32)

coefficents = generateLinearTrajectory(points)

draw(coefficents, points)


