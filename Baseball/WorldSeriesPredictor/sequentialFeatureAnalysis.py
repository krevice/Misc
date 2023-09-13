# Import necessary libraries
from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.metrics import accuracy_score

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

# Sequential Feature Analysis
# This section performs sequential feature selection and evaluates the model on a test set

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create a logistic regression model
model = LogisticRegression(max_iter=1000)

# Perform Sequential Feature Selection
sfs = SequentialFeatureSelector(model, n_features_to_select=5, direction='forward', cv=5)
sfs.fit(X_train_scaled, y_train)

# Get the selected feature indices
selected_feature_indices = sfs.get_support(indices=True)

# Use selected_feature_indices to subset your features
selected_features = X.columns[selected_feature_indices]

# Train the model with the selected features
model.fit(X_train_scaled[:, selected_feature_indices], y_train)

# Make predictions and evaluate the model on the test set
y_pred = model.predict(X_test_scaled[:, selected_feature_indices])
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy on the test set with selected features: {accuracy:.2f}")

# Print the selected feature names
print("Selected Features:")
for feature in selected_features:
    print(feature)
