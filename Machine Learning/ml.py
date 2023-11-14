from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor

class Item(BaseModel):
	moisture: int
	irrigation: int
	weather_code: int


dataset1 = pd.read_csv('moisture_before_after.csv')
X=dataset1[['Moisture_Before', 'Weather_Code']]
y=dataset1['Moisture_After'] 
X=X.values
y=y.values
svr = DecisionTreeRegressor()
svr.fit(X,y)
app = FastAPI()

@app.post('/ml')
async def add_menu(item: Item):	
	item_dict=item.dict()
	y_pred=svr.predict([[item_dict.get("moisture"),item_dict.get("weather_code")]])
	moisture_after=y_pred.tolist()
	if item_dict.get('moisture') > 4000:
		moisture_after[0]=item_dict.get('moisture')/3.7
	if item_dict.get("moisture") < 45:
		moisture_after[0]=item_dict.get('moisture')/3
	dataset2 = pd.read_csv('durasi_pengairan.csv')
	X = dataset2[['Moisture', 'Irrigation']]
	y = dataset2['Duration']
	X=X.values
	y=y.values
	regressor = linear_model.LinearRegression()
	regressor.fit(X,y)
	
	if item_dict.get("irrigation") == 0:
		return [0]
	if item_dict.get("irrigation") == 1 and moisture_after[0]>=1360:
		return [0]
	y_pred = regressor.predict([[item_dict.get("moisture"),item_dict.get("irrigation")]])
	
	y_pred=y_pred.tolist()
	if y_pred[0]<0:
		y_pred[0]=0
	return y_pred[0]
	

