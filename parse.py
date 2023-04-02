import pandas as pd
from sklearn.preprocessing import StandardScaler

def arrange_data(landmark_dict, distance_dict, screen_width, screen_height, x, y):
    """
    Arranges the data into a dataframe with labeled columns
    Args:
        landmark_dict: dictionary of landmark coordinates
        distance_dict: dictionary of line distances
    Returns:
        a ready to save dataframe"""

    # file path
    file_path = 'data.csv'

    # Combine the dictionaries
    combined_dict = {
        **landmark_dict,
        **distance_dict,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'x': x,
        'y': y,
    }

    # Append the combined_dict to a list
    data_list = [combined_dict]

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # add the data row to the csv file
    df.to_csv(file_path, mode='a', header=False, index=False)
