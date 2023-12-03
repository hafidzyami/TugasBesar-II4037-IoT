import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
dataset2 = pd.read_csv('durasi_pengairan.csv')

# Extract features and target variable
X = dataset2[['Moisture', 'Irrigation']]
y = dataset2['Duration']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Linear Regression model
regressor = LinearRegression()

# Fit the model on the training set
regressor.fit(X_train, y_train)

# Predict the target variable on the testing set
y_pred = regressor.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error: {}".format(mse))
print("R-squared: {}".format(r2))
