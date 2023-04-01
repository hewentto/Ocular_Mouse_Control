import cv2 as cv
import mediapipe as mp
import numpy as np

def draw_face_connections(image, face_landmarks):
    nose_tip_landmark_index = 4
    nose_x, nose_y, nose_z = int(face_landmarks.landmark[nose_tip_landmark_index].x * image.shape[1]), \
                             int(face_landmarks.landmark[nose_tip_landmark_index].y * image.shape[0]), \
                             face_landmarks.landmark[nose_tip_landmark_index].z

    left_eye_x, left_eye_y, left_eye_z = int(face_landmarks.landmark[473].x * image.shape[1]), \
                                         int(face_landmarks.landmark[473].y * image.shape[0]), \
                                         face_landmarks.landmark[473].z
    right_eye_x, right_eye_y, right_eye_z = int(face_landmarks.landmark[468].x * image.shape[1]), \
                                             int(face_landmarks.landmark[468].y * image.shape[0]), \
                                             face_landmarks.landmark[468].z

    line_color = (0, 255, 0)
    line_thickness = 1


    # Define landmark indices for eyebrows
    eyebrow_landmarks = [105, 107, 336, 334]

    dot_radius = 2
    dot_thickness = -1
    # Draw circles for eyebrow landmarks
    for landmark_index in eyebrow_landmarks:
        x, y = int(face_landmarks.landmark[landmark_index].x * image.shape[1]), int(face_landmarks.landmark[landmark_index].y * image.shape[0])
        dot_color = (255, 0, 255)
        cv.circle(image, (x, y), dot_radius, dot_color, dot_thickness)

    cv.line(image, (nose_x, nose_y), (left_eye_x, left_eye_y), line_color, line_thickness)
    cv.line(image, (nose_x, nose_y), (right_eye_x, right_eye_y), line_color, line_thickness)
    cv.line(image, (left_eye_x, left_eye_y), (right_eye_x, right_eye_y), line_color, line_thickness)

    # Define landmark indices for different regions of the face
    forehead_landmark_index = 10
    chin_landmark_index = 152
    left_cheek_landmark_index = 234
    right_cheek_landmark_index = 454

    # Get the landmark coordinates
    landmarks = [(nose_x, nose_y), (left_eye_x, left_eye_y), (right_eye_x, right_eye_y)]
    for index in [forehead_landmark_index, chin_landmark_index, left_cheek_landmark_index, right_cheek_landmark_index]:
        x, y = int(face_landmarks.landmark[index].x * image.shape[1]), int(face_landmarks.landmark[index].y * image.shape[0])
        landmarks.append((x, y))

    # Calculate the average position of the landmarks
    center_x = int(sum(x for x, y in landmarks) / len(landmarks))
    center_y = int(sum(y for x, y in landmarks) / len(landmarks))

    # Draw a circle at the calculated center of the head
    center_color = (255, 0, 0)
    center_radius = 3
    center_thickness = -1
    cv.circle(image, (center_x, center_y), center_radius, center_color, center_thickness)
    # draw line from cennter of head to nose, and eyes and eyebrows
    cv.line(image, (center_x, center_y), (nose_x, nose_y), line_color, line_thickness)
    cv.line(image, (center_x, center_y), (left_eye_x, left_eye_y), line_color, line_thickness)
    cv.line(image, (center_x, center_y), (right_eye_x, right_eye_y), line_color, line_thickness)

    # Calculate distance of each line
    nose_to_center = np.sqrt((nose_x - center_x) ** 2 + (nose_y - center_y) ** 2)
    left_eye_to_center = np.sqrt((left_eye_x - center_x) ** 2 + (left_eye_y - center_y) ** 2)
    right_eye_to_center = np.sqrt((right_eye_x - center_x) ** 2 + (right_eye_y - center_y) ** 2)
    nose_to_left_eye = np.sqrt((nose_x - left_eye_x) ** 2 + (nose_y - left_eye_y) ** 2)
    nose_to_right_eye = np.sqrt((nose_x - right_eye_x) ** 2 + (nose_y - right_eye_y) ** 2)
    left_eye_to_right_eye = np.sqrt((left_eye_x - right_eye_x) ** 2 + (left_eye_y - right_eye_y) ** 2)

    # on click, print each distance
    def print_distances():
        print("nose_to_center", nose_to_center)
        print("left_eye_to_center", left_eye_to_center)
        print("right_eye_to_center", right_eye_to_center)
        print("nose_to_left_eye", nose_to_left_eye)
        print("nose_to_right_eye", nose_to_right_eye)
        print("left_eye_to_right_eye", left_eye_to_right_eye)


    

mp_face_mesh = mp.solutions.face_mesh
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
                draw_face_connections(image, face_landmarks)

        cv.imshow('MediaPipe Face Mesh', cv.flip(image, 1))
        key = cv.waitKey(1)

        if key == ord('q'):
            break

cap.release()
