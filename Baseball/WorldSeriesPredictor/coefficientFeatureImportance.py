# Import necessary libraries
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load and preprocess the training data
train_data = pd.read_csv('Fangraphs Master.csv')
X = train_data.drop(['Team', 'Season'], axis=1)
X_train = train_data.drop(['Team', 'Season', 'WS_Win'], axis=1)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
y_train = train_data['WS_Win']

# Train a logistic regression classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Calculate and plot the feature importance using absolute values of the coefficients
# This section calculates and visualizes feature importance based on absolute coefficients in the logistic regression model

# Get feature coefficients (weights) and their absolute values
coefficients = model.coef_[0]
abs_coefficients = np.abs(coefficients)

# Sort features by absolute importance
sorted_indices = np.argsort(abs_coefficients)[::-1]
sorted_coefficients = abs_coefficients[sorted_indices]
sorted_feature_names = X_train.columns[sorted_indices]

# Plot feature importances
fig, ax = plt.subplots(figsize=(10, 6))
fig.set_facecolor('beige')
plt.gca().set_facecolor('beige')
bars = ax.barh(range(len(sorted_coefficients)), sorted_coefficients[::-1])
ax.set_ylabel('Feature')
ax.set_xlabel('Absolute Coefficient Value')
ax.set_title('Feature Importance in Logistic Regression Model')
ax.yaxis.tick_left()
plt.yticks(range(len(sorted_coefficients)), reversed(sorted_feature_names))

# Custom colors for the bars
colors = plt.cm.copper(np.linspace(0, 1, len(sorted_coefficients)))

# Set custom colors for feature labels
for bar, feature_name, color in zip(bars, sorted_feature_names, colors):
    bar.set_label(feature_name)
    bar.set_color(color)
plt.tight_layout()
plt.show()
