# Import necessary libraries
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import seaborn as sns

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

# Calculate and plot a correlation matrix using a heatmap
# This section calculates and visualizes a correlation matrix heatmap, including the dependent variable

correlation_matrix = X.corr()

# Create a mask to display only the lower half of the matrix
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(10, 6))
fig.set_facecolor('beige')
plt.gca().set_facecolor('beige')

# Create a heatmap
sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="YlOrBr",  # Change to your preferred color map
    mask=mask,
    square=False,
    cbar=True,
    annot_kws={"size": 8},
)

plt.title("Feature and WS_Win Correlation Heatmap")
plt.yticks(np.arange(len(correlation_matrix))+0.5, X.columns)
plt.tight_layout()
plt.show()
