# Import necessary libraries
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.inspection import permutation_importance

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

# Calculate and plot permutation feature importance
# This section calculates and visualizes feature importance using permutation importance

# Calculate permutation importance
perm_importance = permutation_importance(model, X_train_scaled, y_train, n_repeats=30, random_state=42)

# Get feature importances
importances = perm_importance.importances_mean

# Sort feature importances in descending order
sorted_indices = importances.argsort()[::-1]
sorted_importances = importances[sorted_indices]
sorted_feature_names = X_train.columns[sorted_indices]

# Plot feature importances
fig, ax = plt.subplots(figsize=(10, 6))
fig.set_facecolor('beige')
plt.gca().set_facecolor('beige')
bars = plt.barh(range(len(sorted_importances)), sorted_importances[::-1])
plt.ylabel('Feature')
plt.xlabel('Permutation Importance')
plt.title('Permutation Feature Importance')
plt.yticks(range(len(sorted_importances)), reversed(sorted_feature_names))

# Custom colors for the bars
colors = plt.cm.copper(np.linspace(0, 1, len(sorted_importances)))

# Set custom colors for feature labels
for bar, feature_name, color in zip(bars, sorted_feature_names, colors):
    bar.set_label(feature_name)
    bar.set_color(color)
plt.tight_layout()
plt.show()
