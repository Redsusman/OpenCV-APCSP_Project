import keyboard as key
import detectCone
import detectCube



while True:
    if key.is_pressed('u'):
        detectCube.run()
        break
    elif key.is_pressed('o'):
        detectCone.run()
        break

