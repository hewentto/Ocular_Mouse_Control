import pandas as pd
import pyautogui
import joblib
import numpy as np
import keras
import math
from sklearn.preprocessing import StandardScaler

pyautogui.FAILSAFE = False


# Load the models and feature names
xModel = joblib.load('best_svr_x_tuned.pkl')
yModel = joblib.load('best_svr_y_tuned.pkl')

def predict_coordinates(input_data):
    """Predicts the coordinates of the mouse pointer using the trained SVR models"""
    
    # drop target
    x = xModel.predict(input_data.values.reshape(1, -1))
    y = yModel.predict(input_data.values.reshape(1, -1))
    return x, y


# Initialize a list to keep track of the previous predicted coordinates
prev_coords = []

def predict_and_smooth_coordinates(input_data, n=5):
    """Predicts the coordinates of the mouse pointer using the trained model and applies a low-pass filter"""
    x_pred, y_pred = predict_coordinates(input_data)

    # Add the current predicted coordinates to the list
    prev_coords.append((x_pred, y_pred))

    # If the list is longer than n, remove the oldest coordinates
    if len(prev_coords) > n:
        prev_coords.pop(0)

    # Take the average of the previous n predicted coordinates
    x_smoothed = np.mean([coord[0] for coord in prev_coords])
    y_smoothed = np.mean([coord[1] for coord in prev_coords])

    return x_smoothed, y_smoothed

# Update move_mouse function to use predict_and_smooth_coordinates
def move_mouse(landmark_dict, screen_width, screen_height, x, y):
    df = arrange_data(landmark_dict, screen_width, screen_height, x, y)

    # Drop 'target' column if present
    df.drop(columns=['target'], errors='ignore', inplace=True)
    
    # Debugging: Print columns to ensure 'target' is removed
    print("Columns after dropping 'target':", df.columns.tolist())

    x_smoothed, y_smoothed = predict_and_smooth_coordinates(df)

    # Ensure the coordinates stay within screen boundaries
    x_smoothed = max(0, min(screen_width - 1, x_smoothed))
    y_smoothed = max(0, min(screen_height - 1, y_smoothed))

    pyautogui.moveTo(x_smoothed, y_smoothed, duration=0)


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

def calculate_head_pose(row):
    nose = (row['nose_x'], row['nose_y'], row['nose_z'])
    left_eye = (row['left_eye_x'], row['left_eye_y'], row['left_eye_z'])
    right_eye = (row['right_eye_x'], row['right_eye_y'], row['right_eye_z'])
    return calculate_angles(nose, left_eye, right_eye)

def calculate_eye_gaze(row, eye_x, eye_y, eye_z):
    nose = (row['nose_x'], row['nose_y'], row['nose_z'])
    eye = (row[eye_x], row[eye_y], row[eye_z])

    # Horizontal gaze
    horizontal_gaze = math.atan2(eye[0] - nose[0], eye[2] - nose[2])

    # Vertical gaze
    vertical_gaze = math.atan2(eye[1] - nose[1], eye[2] - nose[2])

    return horizontal_gaze, vertical_gaze

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

def arrange_data(landmark_dict, screen_width, screen_height, x, y):
    """Arranges the data into a dataframe with labeled columns"""
    # Calculate distances between landmarks
    distance_dict = Get_distances(landmark_dict, screen_width, screen_height)

    # Combine the dictionaries
    combined_dict = {
        'nose_x': landmark_dict['nose'][0],
        'nose_y': landmark_dict['nose'][1],
        'nose_z': landmark_dict['nose'][2],
        'left_eye_x': landmark_dict['left_eye'][0],
        'left_eye_y': landmark_dict['left_eye'][1],
        'left_eye_z': landmark_dict['left_eye'][2],
        'right_eye_x': landmark_dict['right_eye'][0],
        'right_eye_y': landmark_dict['right_eye'][1],
        'right_eye_z': landmark_dict['right_eye'][2],
        'forehead_x': landmark_dict['forehead'][0],
        'forehead_y': landmark_dict['forehead'][1],
        'forehead_z': landmark_dict['forehead'][2],
        'chin_x': landmark_dict['chin'][0],
        'chin_y': landmark_dict['chin'][1],
        'chin_z': landmark_dict['chin'][2],
        'left_cheek_x': landmark_dict['left_cheek'][0],
        'left_cheek_y': landmark_dict['left_cheek'][1],
        'left_cheek_z': landmark_dict['left_cheek'][2],
        'screen_height': screen_height,
        'right_cheek_x': landmark_dict['right_cheek'][0],
        'right_cheek_y': landmark_dict['right_cheek'][1],
        'right_cheek_z': landmark_dict['right_cheek'][2],
        'center_x': landmark_dict['center'][0],
        'center_y': landmark_dict['center'][1],
        'center_z': landmark_dict['center'][2],   
    }
    # Add the distances to the dictionary
    combined_dict.update(distance_dict)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame([combined_dict])

    # Add new features based on the input data
    df = add_features_to_dataset(df)

    df['target'] = f"({x}, {y})"

    return df

def save_data(landmark_dict, screen_width, screen_height, x, y):

    df = arrange_data(landmark_dict, screen_width, screen_height, x, y)
    # file path
    file_path = 'data2.csv'
    # add the data row to the csv file
    df.to_csv(file_path, mode='a', header=False, index=False)

def euclidean_distance_3(x1, y1, z1, x2, y2, z2):
    """
    Calculates the euclidean distance between two points
    Args:
        x1: x coordinate of point 1
        y1: y coordinate of point 1
        z1: z coordinate of point 1
        x2: x coordinate of point 2
        y2: y coordinate of point 2
        z2: z coordinate of point 2
    Returns:
        the euclidean distance between the two points"""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def euclidean_distance_2(x1, y1, x2, y2):
    """
    Calculates the euclidean distance between two points
    Args:
        x1: x coordinate of point 1
        y1: y coordinate of point 1
        x2: x coordinate of point 2
        y2: y coordinate of point 2
    Returns:
        the euclidean distance between the two points"""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def Get_distances(landmark_dict, screen_width, screen_height):
    """
    returns data frame with relevant euclidean distances lengths
    Args:
        landmark_dict: dictionary of landmark coordinates
    Returns:
        a dictionary of distances between landmarks"""
    return {
        'nose_to_left_eye3': euclidean_distance_3(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][2],
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][2],
        ),
        'nose_to_right_eye3': euclidean_distance_3(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][2],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][2],
        ),
        'nose_to_image_edge': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            screen_width,
            landmark_dict['nose'][1],
        ),
        'nose_to_image_top': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][0],
            0,
        ),
        'nose_to_image_bottom': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][0],
            screen_height,
        ),
        'left_eye_to_right_eye3': euclidean_distance_3(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][2],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][2],
        ),
        'left_eye_to_image_edge': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            0,
            landmark_dict['left_eye'][1],
        ),
        'left_eye_to_image_top': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][0],
            0,
        ),
        'left_eye_to_image_bottom': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][0],
            screen_height,
        ),
        'right_eye_to_image_edge': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            screen_width,
            landmark_dict['right_eye'][1],
        ),
        'right_eye_to_image_top': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][0],
            0,
        ),
        'right_eye_to_image_bottom': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][0],
            screen_height,
        ),
        'center_to_nose3': euclidean_distance_3(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['nose'][2],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][2],
        ),
        'center_to_left_eye3': euclidean_distance_3(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['left_eye'][2],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][2],
        ),
        'center_to_right_eye3': euclidean_distance_3(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['right_eye'][2],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][2],
        ),
        'center_to_image_edge': euclidean_distance_2(
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            screen_width,
            landmark_dict['center'][1],
        ),
        'center_to_image_top': euclidean_distance_2(
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][0],
            0,
        ),
        'center_to_image_bottom': euclidean_distance_2(
            landmark_dict['center'][0],
            landmark_dict['center'][1],
            landmark_dict['center'][0],
            screen_height,
        ),
        'nose_to_left_eye2': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
        ),
        'nose_to_right_eye2': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
        ),
        'left_eye_to_right_eye2': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
        ),
        'left_eye_to_center2': euclidean_distance_2(
            landmark_dict['left_eye'][0],
            landmark_dict['left_eye'][1],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
        ),
        'right_eye_to_center2': euclidean_distance_2(
            landmark_dict['right_eye'][0],
            landmark_dict['right_eye'][1],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
        ),
        'nose_to_center2': euclidean_distance_2(
            landmark_dict['nose'][0],
            landmark_dict['nose'][1],
            landmark_dict['center'][0],
            landmark_dict['center'][1],
        ),
    }