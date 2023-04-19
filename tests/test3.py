import numpy as np
import cv2

def correctRotation(measurement):

    kalman_filter = cv2.KalmanFilter(9, 3, 0)

    if measurement.shape == (3, 3):

        measurement, _ = cv2.Rodrigues(measurement)

        measurement = measurement.astype(np.float32)

        # measurementMatrix = np.eye(3,9, dtype=np.float32)
        measurementMatrix = np.eye(3,9, dtype=np.float32)

        transitionMatrix = np.array([[1, 0, 1, 0, 0, 0, 0, 0, 0],
                                 [0, 1, 0, 1, 0, 0, 0, 0, 0],
                                 [0, 0, 1, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 1, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 1, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 1, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 1, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 1]], dtype=np.float32)

        processNoiseCov = np.eye(9, dtype=np.float32) * 1e-5
        measurementNoiseCov = np.eye(3, dtype=np.float32) * 1e-1
        errorCovPre = np.ones((9,9), dtype=np.float32)
        statePre = np.zeros((9,1), dtype=np.float32)
        errorCovPost = np.zeros((9, 9), dtype=np.float32)


        kalman_filter.measurementMatrix = measurementMatrix
        kalman_filter.transitionMatrix = transitionMatrix
        kalman_filter.processNoiseCov = processNoiseCov
        kalman_filter.measurementNoiseCov = measurementNoiseCov
        kalman_filter.errorCovPre = errorCovPre
        kalman_filter.errorCovPost = errorCovPost
        kalman_filter.statePre = statePre

        kalman_filter.correct(measurement)
        prediction = kalman_filter.predict()

        final_estimate = prediction[:3, :3]

        final_estimate = final_estimate.astype(np.float32)

        return final_estimate

    

        
measurement = np.array([[0.55153656, 0.4131012, 0.72523683],
                        [0.72201407, 0.46193978, 0.5158567],
                        [0.41734803, 0.7820087, 0.46131814]])

rot_matrix = correctRotation(measurement)
print(rot_matrix)

# rot_matrix, _ = cv2.Rodrigues(final_estimate)






