import pandas as pd
import numpy as np
import math

# Function to calculate pitch, yaw, and roll angles
def calculate_angles(p1, p2, p3):
    # Calculate vectors
    v1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])

    # Calculate cross product for normal vector
    normal = (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    )

    # Calculate pitch (rotation around X-axis)
    pitch = math.atan2(normal[1], normal[2])

    # Calculate yaw (rotation around Y-axis)
    yaw = math.atan2(-normal[0], math.sqrt(normal[1] ** 2 + normal[2] ** 2))

    # Calculate roll (rotation around Z-axis)
    roll = math.atan2(v2[1], v2[0])

    return pitch, yaw, roll

# Calculate head pose angles
def calculate_head_pose(row):
    nose = (row['nose_x'], row['nose_y'], row['nose_z'])
    left_eye = (row['left_eye_x'], row['left_eye_y'], row['left_eye_z'])
    right_eye = (row['right_eye_x'], row['right_eye_y'], row['right_eye_z'])
    return calculate_angles(nose, left_eye, right_eye)

# Calculate eye gaze angles (horizontal and vertical)
def calculate_eye_gaze(row, eye_x, eye_y, eye_z):
    nose = (row['nose_x'], row['nose_y'], row['nose_z'])
    eye = (row[eye_x], row[eye_y], row[eye_z])

    # Horizontal gaze
    horizontal_gaze = math.atan2(eye[0] - nose[0], eye[2] - nose[2])

    # Vertical gaze
    vertical_gaze = math.atan2(eye[1] - nose[1], eye[2] - nose[2])

    return horizontal_gaze, vertical_gaze

# Function to add additional features to the dataset
def add_features_to_dataset(df):
    # Interaction features
    df['nose_to_left_eye3_times_right_eye'] = df['nose_to_left_eye3'] * df['nose_to_right_eye3']
    df['left_eye_to_right_eye3_times_nose_to_center2'] = df['left_eye_to_right_eye3'] * df['nose_to_center2']

    # Ratios
    df['left_eye_to_right_eye_ratio'] = df['left_eye_to_right_eye3'] / (df['nose_to_left_eye3'] + 1e-5)
    df['nose_to_center_ratio'] = df['nose_to_center2'] / (df['left_eye_to_right_eye3'] + 1e-5)

    # Differences
    df['forehead_chin_y_diff'] = df['forehead_y'] - df['chin_y']
    df['left_right_eye_y_diff'] = df['left_eye_y'] - df['right_eye_y']

    # Distances from the center of the screen
    df['nose_center_screen_dist'] = np.sqrt((df['nose_x'] - df['center_x'])**2 + (df['nose_y'] - df['center_y'])**2)
    df['left_eye_center_screen_dist'] = np.sqrt((df['left_eye_x'] - df['center_x'])**2 + (df['left_eye_y'] - df['center_y'])**2)

    # Head pose angles
    df[['head_pitch', 'head_yaw', 'head_roll']] = df.apply(calculate_head_pose, axis=1, result_type='expand')

    # Eye gaze angles
    df[['left_eye_horizontal_gaze', 'left_eye_vertical_gaze']] = df.apply(
        lambda row: calculate_eye_gaze(row, 'left_eye_x', 'left_eye_y', 'left_eye_z'), axis=1, result_type='expand'
    )

    df[['right_eye_horizontal_gaze', 'right_eye_vertical_gaze']] = df.apply(
        lambda row: calculate_eye_gaze(row, 'right_eye_x', 'right_eye_y', 'right_eye_z'), axis=1, result_type='expand'
    )

    return df

# Load the original dataset
data = pd.read_csv('data2.csv')

# Add new features
data_enhanced = add_features_to_dataset(data)

# Move the 'target' column to the end
target = data_enhanced.pop('target')
data_enhanced['target'] = target

# Save the new dataset to a CSV file
data_enhanced.to_csv('data3.csv', index=False)

# Confirm the operation is complete
'data3.csv created with additional features and target column moved to the end.'
