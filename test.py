import numpy as np

array = [1,2,3,4,5,6,7,8,9,10]

for i, j in zip(range(0, len(array)), range(1, len(array))):
    print(array[i], array[j])
    
