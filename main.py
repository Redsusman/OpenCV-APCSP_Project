import keyboard as key
import detectCone
import detectCube
import cameraCalibration as calib
import linearTrajectory as lt


while True:
       if key.is_pressed('u'):
           detectCube.run()
           while True:
                n = 0
           break
       elif key.is_pressed('o'):
           detectCone.run()
           break
       
lt.generateLinearTrajectory()





