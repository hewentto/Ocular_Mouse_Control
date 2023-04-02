import pandas as pd
from sklearn.preprocessing import StandardScaler

def arrange_data(landmark_dict, distance_dict, screen_width, screen_height, x, y):
    """
    Arranges the data into a dataframe with labeled columns, preprocesses it, and saves it to a CSV file
    Args:
        landmark_dict: dictionary of landmark coordinates
        distance_dict: dictionary of line distances
        screen_width: screen width in pixels
        screen_height: screen height in pixels
        x: x coordinate in pixels
        y: y coordinate in pixels
        file_path: file path to save the preprocessed data
    Returns:
        None
    """

    # filepath
    file_path = 'data.csv'
    # Combine the dictionaries
    combined_dict = {**landmark_dict, **distance_dict}

    # Create a DataFrame from the combined dictionary
    df = pd.DataFrame(combined_dict, index=[0])

    # Add screen dimensions, x, and y coordinates as additional columns
    df['screen_width'] = screen_width
    df['screen_height'] = screen_height
    df['x'] = x
    df['y'] = y

    # Normalize or standardize the numerical features
    scaler = StandardScaler()
    numerical_features = ['screen_width', 'screen_height', 'x', 'y']
    df[numerical_features] = scaler.fit_transform(df[numerical_features])

    # Save the preprocessed data to a CSV file
    df.to_csv(file_path, index=False)
