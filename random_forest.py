import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


n_trees = 1000
# Read CSV file
data = pd.read_csv("data.csv")

# Separate feature and target variables
X = data.drop(columns=["target"])
y = data["target"].apply(lambda target: eval(target))  # Convert string coordinates to tuples
y_x = [coord[0] for coord in y]  # Separate x coordinates
y_y = [coord[1] for coord in y]  # Separate y coordinates

X_train, X_test, y_x_train, y_x_test, y_y_train, y_y_test = train_test_split(X, y_x, y_y, test_size=0.2, random_state=42)

# Train the model for x coordinates
regressor_x = RandomForestRegressor(n_estimators=n_trees)
regressor_x.fit(X_train, y_x_train)

# Train the model for y coordinates
regressor_y = RandomForestRegressor(n_estimators=n_trees)
regressor_y.fit(X_train, y_y_train)

# Make predictions for x and y coordinates
y_x_pred = regressor_x.predict(X_test)
y_y_pred = regressor_y.predict(X_test)

# Calculate the mean squared error
mse_x = mean_squared_error(y_x_test, y_x_pred)
mse_y = mean_squared_error(y_y_test, y_y_pred)

# Calculate the R^2 score
r2_x = r2_score(y_x_test, y_x_pred)
r2_y = r2_score(y_y_test, y_y_pred)

print("Mean Squared Error for x: ", mse_x)
print("Mean Squared Error for y: ", mse_y)
print("R^2 Score for x: ", r2_x)
print("R^2 Score for y: ", r2_y)

# Get feature importances for x coordinates
feature_importances_x = regressor_x.feature_importances_

# Get feature importances for y coordinates
feature_importances_y = regressor_y.feature_importances_

# Combine feature importances for x and y coordinates
importances_combined = list(zip(X.columns, feature_importances_x, feature_importances_y))

# Sort the combined importances in descending order based on the average importance
importances_sorted = sorted(importances_combined, key=lambda x: (x[1] + x[2]) / 2, reverse=True)

# Create a DataFrame with the sorted feature importances
importances_df = pd.DataFrame(importances_sorted, columns=["Feature", "X Importance", "Y Importance"])

# Save the DataFrame as a CSV file
importances_df.to_csv("feature_importances.csv", index=False)