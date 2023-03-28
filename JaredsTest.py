import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui


def move_mouse(iris_x, iris_y):
    screen_x = int(iris_x * screen_width)
    screen_y = int(iris_y * screen_height)
    pyautogui.moveTo(screen_x, screen_y, duration=0.1)


def draw_face_connections(image, face_landmarks):
    nose_tip_landmark_index = 4
    nose_x, nose_y, nose_color, nose_radius = assign_values(image, face_landmarks, nose_tip_landmark_index)
    nose_thickness = 2
    cv.circle(image, (nose_x, nose_y), nose_radius, nose_color, nose_thickness)

    left_eye_x, left_eye_y = int(face_landmarks.landmark[473].x * image.shape[1]), \
                             int(face_landmarks.landmark[473 ].y * image.shape[0])
    right_eye_x, right_eye_y = int(face_landmarks.landmark[468].x * image.shape[1]), \
                               int(face_landmarks.landmark[468].y * image.shape[0])
    line_color = (0, 255, 0)
    line_thickness = 1

    cv.line(image, (nose_x, nose_y), (left_eye_x, left_eye_y), line_color, line_thickness)
    cv.line(image, (nose_x, nose_y), (right_eye_x, right_eye_y), line_color, line_thickness)
    cv.line(image, (left_eye_x, left_eye_y), (right_eye_x, right_eye_y), line_color, line_thickness)

    nose_left_eye_length = np.sqrt((nose_x - left_eye_x)**2 + (nose_y - left_eye_y)**2)
    nose_right_eye_length = np.sqrt((nose_x - right_eye_x)**2 + (nose_y - right_eye_y)**2)
    left_right_eye_length = np.sqrt((left_eye_x - right_eye_x)**2 + (left_eye_y - right_eye_y)**2)

    print("Nose to left eye length:", nose_left_eye_length)
    print("Nose to right eye length:", nose_right_eye_length)
    print("Left eye to right eye length:", left_right_eye_length)

def assign_values(image, face_landmarks, nose_tip_landmark_index):
    nose_x, nose_y = int(face_landmarks.landmark[nose_tip_landmark_index].x * image.shape[1]), \
                     int(face_landmarks.landmark[nose_tip_landmark_index].y * image.shape[0])
    nose_color = (0, 0, 255)
    nose_radius = 2
    return nose_x,nose_y,nose_color,nose_radius
    

mp_face_mesh = mp.solutions.face_mesh
mp_drawing_styles = mp.solutions.drawing_styles
cap = cv.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv.VideoCapture(0)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
                )

                left_eye_x = face_landmarks.landmark[473].x
                left_eye_y = face_landmarks.landmark[473].y
                right_eye_x = face_landmarks.landmark[468].x
                right_eye_y = face_landmarks.landmark[468].y

                avg_eye_x = (left_eye_x + right_eye_x) / 2
                avg_eye_y = (left_eye_y + right_eye_y) / 2

                move_mouse(1 - avg_eye_x, avg_eye_y)

                draw_face_connections(image, face_landmarks)

        cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
        key = cv.waitKey(1)

        if key == ord('q'):
            break

cap.release()


