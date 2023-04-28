import matplotlib.pyplot as plot
import numpy as np
import math
from matplotlib.animation import FuncAnimation
import numpy.linalg as lin

# generate a linear trajectory from a set of points using polynomial regression
# returns coefficents of the linear function of points, and the angle of the line relative to the postive
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

# simulate linear trajectories between points using matplotlib graph
def draw(coefficents, points):
    yList = []
    x_points = np.linspace(points[0][0], points[1][0], 50)

    for x in x_points:
        elementsY = (coefficents[0] * x) + coefficents[1]
        yList.append(elementsY)

    fig = plot.gcf()
    ax = fig.gca()
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    line = ax.plot(points[0][0], points[0][1])[0]
    line.set_data(x_points, yList)
    ax.relim()
    anim = FuncAnimation(fig, func=line, frames=np.arange(0, 100),  interval=100)
    plot.pause(0.01)
   

