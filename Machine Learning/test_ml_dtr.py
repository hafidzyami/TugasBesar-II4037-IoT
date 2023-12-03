import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
dataset1 = pd.read_csv('moisture_before_after.csv')

# Extract features and target variable
X = dataset1[['Moisture_Before', 'Weather_Code']]
y = dataset1['Moisture_After']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Decision Tree Regressor
svr = DecisionTreeRegressor()

# Fit the model on the training set
svr.fit(X_train, y_train)

# Predict the target variable on the testing set
y_pred = svr.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error: {}".format(mse))
print("R-squared: {}".format(r2))
