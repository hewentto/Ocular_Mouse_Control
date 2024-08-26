import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras
import joblib


# Replace this with the path to your dataset file
data_file = 'data2.csv'

# Load the dataset
data = pd.read_csv(data_file)

# shuffle the dataset
data = data.sample(frac=1).reset_index(drop=True)

# Preprocess the target column
data["target"] = data["target"].apply(lambda s: tuple(map(int, s.strip("()").split(","))))
data["target_x"] = data["target"].apply(lambda t: t[0])
data["target_y"] = data["target"].apply(lambda t: t[1])
data = data.drop("target", axis=1)

# Separate input features and target
X = data.iloc[:, :-2].values
y = data.iloc[:, -2:].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

feature_names = data.iloc[:, :-2].columns

joblib.dump(scaler, "scaler.pkl")
joblib.dump(feature_names, "feature_names.pkl")
# Create a sequential model
model = keras.models.Sequential()

# Add input layer
model.add(keras.layers.Dense(256, activation='relu', input_dim=X_train_scaled.shape[1]))

# Add hidden layers
model.add(keras.layers.Dense(512, activation='relu'))
model.add(keras.layers.Dense(256, activation='relu'))

# Add output layer with 2 output units (for x and y coordinates)
model.add(keras.layers.Dense(2))

optimizer = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])

# Define early stopping
early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

model.fit(X_train_scaled, y_train, batch_size=32, epochs=200, validation_data=(X_test_scaled, y_test), callbacks=[early_stopping])

# Evaluate the model on the test set
loss, mae = model.evaluate(X_test_scaled, y_test)
print(f"Test Set Mean Squared Error: {loss:.4f}")
print(f"Test Set Mean Absolute Error: {mae:.4f}")

# Save the trained model to a file
model.save("my_model.keras")