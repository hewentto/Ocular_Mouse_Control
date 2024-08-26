import ctypes
import cv2 as cv
import mediapipe as mp
from pynput.mouse import Button, Controller, Listener
import threading
import csv
import math
import parse
import pandas as pd
import pyautogui as pag 


# Set the DeviceID of the camera
device_id = r"USB\VID_1D6C&PID_1278&MI_00\8&1ACFF732&0&0000"

def initialize_face_mesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
    return mp.solutions.face_mesh.FaceMesh(
        max_num_faces=max_num_faces,
        refine_landmarks=refine_landmarks,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence)

def get_landmarks(image, face_mesh):
    image.flags.writeable = False
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    return results, image

def draw_landmarks(image, results):
    if not results.multi_face_landmarks:
        return None, None

    # Draw the specified landmarks and lines
    nose_tip_landmark_index = 4
    # Define landmark indices for different regions of the face
    forehead_landmark_index = 10
    chin_landmark_index = 152
    left_cheek_landmark_index = 234
    right_cheek_landmark_index = 454

    def extract_landmarks(face_landmarks, image_shape):
        landmark_labels = ['nose', 'left_eye', 'right_eye', 'forehead', 'chin', 'left_cheek', 'right_cheek', 'center']
        landmark_dict = {}

        nose_x, nose_y, nose_z = face_landmarks.landmark[nose_tip_landmark_index].x * image_shape[1], \
                                face_landmarks.landmark[nose_tip_landmark_index].y * image_shape[0], \
                                face_landmarks.landmark[nose_tip_landmark_index].z
        landmark_dict[landmark_labels[0]] = (nose_x, nose_y, nose_z)

        left_eye_x, left_eye_y, left_eye_z = face_landmarks.landmark[473].x * image_shape[1], \
                                            face_landmarks.landmark[473].y * image_shape[0], \
                                            face_landmarks.landmark[473].z
        landmark_dict[landmark_labels[1]] = (left_eye_x, left_eye_y, left_eye_z)

        right_eye_x, right_eye_y, right_eye_z = face_landmarks.landmark[468].x * image_shape[1], \
                                                face_landmarks.landmark[468].y * image_shape[0], \
                                                face_landmarks.landmark[468].z
        landmark_dict[landmark_labels[2]] = (right_eye_x, right_eye_y, right_eye_z)

        additional_landmark_indices = {
            landmark_labels[3]: forehead_landmark_index,
            landmark_labels[4]: chin_landmark_index,
            landmark_labels[5]: left_cheek_landmark_index,
            landmark_labels[6]: right_cheek_landmark_index
        }

        for label, index in additional_landmark_indices.items():
            x, y, z = face_landmarks.landmark[index].x * image_shape[1], \
                    face_landmarks.landmark[index].y * image_shape[0], \
                    face_landmarks.landmark[index].z * image_shape[0]
            landmark_dict[label] = (x, y, z)

        center_x = sum(x for x, y, z in landmark_dict.values()) / len(landmark_dict)
        center_y = sum(y for x, y, z in landmark_dict.values()) / len(landmark_dict)
        center_z = sum(z for x, y, z in landmark_dict.values()) / len(landmark_dict)

        landmark_dict[landmark_labels[7]] = (center_x, center_y, center_z)

        return landmark_dict

    for face_landmarks in results.multi_face_landmarks:
        landmark_dict = extract_landmarks(face_landmarks, image.shape)
    return landmark_dict

# Define the main function
def main():
    # Find and define monitor width and height
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Initialize the face mesh
    face_mesh = initialize_face_mesh()

    # Initialize the camera
    cap = cv.VideoCapture(int(device_id.split("&")[-1], 16))

    # Loop until the 'q' key is pressed
    while True:
        # Read a frame from the camera
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # get mouse x and y
        x, y = pag.position()

        # Get the landmarks from the face mesh and draw them on the image
        results, image = get_landmarks(image, face_mesh)
        landmark_dict= draw_landmarks(image, results)

        # Check if landmark_dict is not None and if any of the required landmarks are missing
        if landmark_dict is None or any(
            key not in landmark_dict
            for key in ['nose', 'left_eye', 'right_eye']
        ):
            continue

        # If all landmarks are present, call move_mouse
        parse.move_mouse(landmark_dict, screen_width, screen_height, x, y)

        key = cv.waitKey(1)

        # If the 'q' key is pressed, break the loop
        if key == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv.destroyAllWindows()


# If this file is being run as the main program, call the main function
if __name__ == "__main__":
    main()  # Call the main function        