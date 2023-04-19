import numpy as np
import cv2

# Initialize Kalman filter variables
state = np.zeros((9,1), dtype=np.float32)
state_transition = np.eye(9, dtype=np.float32)
measurement_matrix = np.zeros((3,9), dtype=np.float32)

# Initialize measurement variables
measurement = np.array([[0],[0],[0]], dtype=np.float32)

# Create Kalman filter object
kalman_filter = cv2.KalmanFilter(9, 3, 0)

# Set state transition matrix and measurement matrix
kalman_filter.transitionMatrix = state_transition
kalman_filter.measurementMatrix = measurement_matrix

# Set measurement noise and process noise covariance matrices
kalman_filter.measurementNoiseCov = np.eye(3, dtype=np.float32) * 0.1
kalman_filter.processNoiseCov = np.eye(9, dtype=np.float32) * 0.01

# Correct rotation using Kalman filter
def correctRotation(measurement):
    # Reshape measurement to a 3x1 matrix
    measurement = cv2.Rodrigues(measurement)
    kalman_filter.correct(measurement)
    return kalman_filter.predict()

# Test the Kalman filter
measurement = np.array([[0.55153656, 0.4131012, 0.72523683],
                        [0.72201407, 0.46193978, 0.5158567],
                        [0.41734803, 0.7820087, 0.46131814]])

rot_matrix = correctRotation(measurement)
print(rot_matrix)
