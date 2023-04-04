import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

# Load the dataset
# Replace the file path with the path to your dataset
data = pd.read_csv("data.csv")

# Shuffle the dataset
data = data.sample(frac=1).reset_index(drop=True)

# Preprocess the target column
data["target"] = data["target"].apply(lambda s: tuple(map(int, s.strip("()").split(","))))
data["target_x"] = data["target"].apply(lambda t: t[0])
data["target_y"] = data["target"].apply(lambda t: t[1])
data = data.drop("target", axis=1)

# Split the dataset into training and testing sets
X = data.drop(["target_x", "target_y"], axis=1)
y_x = data["target_x"]
y_y = data["target_y"]

X_train, X_test, y_x_train, y_x_test = train_test_split(X, y_x, test_size=0.2, random_state=42)
_, _, y_y_train, y_y_test = train_test_split(X, y_y, test_size=0.2, random_state=42)

# Create a pipeline with StandardScaler and SVR
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('svr', SVR())
])

# Define the hyperparameter search space
param_grid = {
    'svr__C': np.logspace(-3, 3, 7),
    'svr__epsilon': np.logspace(-3, 3, 7),
    'svr__kernel': ['linear', 'poly', 'rbf', 'sigmoid']
}

# Create the GridSearchCV object
grid_search = GridSearchCV(pipeline, param_grid, scoring='neg_mean_squared_error', cv=5, verbose=2, n_jobs=-1)

# Fit the GridSearchCV object to the training data
grid_search.fit(X_train, y_x_train)

# Print the best hyperparameters found
print('Best hyperparameters:', grid_search.best_params_)

# Evaluate the best model on the test set
best_model_x = grid_search.best_estimator_
y_x_pred = best_model_x.predict(X_test)
mse_x = mean_squared_error(y_x_test, y_x_pred)
r2_x = r2_score(y_x_test, y_x_pred)

print('Mean squared error for x predictions:', mse_x)
print('R2 score for x predictions:', r2_x)

# Fit the GridSearchCV object to the training data for y
grid_search.fit(X_train, y_y_train)

# Print the best hyperparameters found for y
print('Best hyperparameters for y:', grid_search.best_params_)

# Evaluate the best model on the test set for y
best_model_y = grid_search.best_estimator_
y_y_pred = best_model_y.predict(X_test)
mse_y = mean_squared_error(y_y_test, y_y_pred)
r2_y = r2_score(y_y_test, y_y_pred)

print('R2 score for x predictions:', r2_x)
print('R2 score for y predictions:', r2_y)

# Save the best model to disk
joblib.dump(best_model_x, 'best_model_x.pkl')
joblib.dump(best_model_y, 'best_model_y.pkl')

