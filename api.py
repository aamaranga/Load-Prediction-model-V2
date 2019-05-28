import flask
from flask import Flask, request, render_template,Response
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')

@app.route("/Download")
def getPlotCSV():
	with open("output_data.csv") as fp:
		csv = fp.read()
	return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=results.csv"})

	
@app.route('/predict', methods=['POST'])
def make_prediction():
	if request.method=='POST':
		
		test = pd.read_csv('test_loan.csv')
		# dropping the first column
		test.drop(labels='Loan_ID',axis=1,inplace=True)
		# imputing missing values
		for i in test.columns:    
			try:
				imputer = SimpleImputer(strategy='mean')
				test[i] = imputer.fit_transform(df2[i].values.reshape(-1,1))
			except:
				imputer = SimpleImputer(strategy='most_frequent')
				test[i] = imputer.fit_transform(test[i].values.reshape(-1,1))
				
		# Encoding non-numeric column
		le = LabelEncoder()
		for i in test.columns:
			if(test[i].dtype=='object'):
				test[i] = le.fit_transform(test[i])
				
		# make prediction 		
		test = test.values
		y_pred_proba = model.predict_proba(test)
		y_pred = model.predict(test)    
		
		# create the output
		output = pd.read_csv('test_loan.csv')
		output['Loan_Status'] =  pd.Series(y_pred)
		output.to_csv('output_data.csv')
		a = output.head()

		return render_template('index.html', label=a.to_html())


if __name__ == '__main__':
	# load ml model
	model = joblib.load('model.pkl')
	# start api
	app.run(debug=True)
