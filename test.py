import numpy as np

array = np.array([(1, 3), (5, 4)], dtype=np.float32)
secondList = array

x = [secondList[i][0] for i in range(len(secondList))]
y = [array[i][1] for i in range(len(array))]

# x = x.ravel()
# y= y.ravel()

a,b = np.polyfit(x,y,1)

print(a,b)