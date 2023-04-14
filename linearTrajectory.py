import matplotlib.pyplot as plot
import numpy as np
import math

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

#generate parabolic trajectories from an acceleration value, speeds are automatically calculated
def generateSplineTrajectory(points, speed):
    return


