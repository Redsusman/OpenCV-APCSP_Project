import matplotlib.pyplot as plot
import numpy as np
import math

array = np.array([(1, 3), (5, 4)], dtype=np.float32)

# generate a linear trajectory from a set of points using polynomial regression
def generateLinearTrajectory(points):
    secondList = points
    x = [secondList[i][0] for i in range(len(secondList))]
    y = [points[i][1] for i in range(len(points))]
    a, b = np.polyfit(x, y, 1)
    print(a,"x+", b)
    return a,b

generateLinearTrajectory(array)


# generate parabolic trajectories from an acceleration value, speeds are automatically calculated

def generateSplineTrajectory(points, speed):
    return


