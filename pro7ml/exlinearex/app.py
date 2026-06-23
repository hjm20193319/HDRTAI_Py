import pickle
import re
import pymysql

with open('mydb.dat', mode = 'rb') as obj:         
    config = pickle.load(obj)

conn = pymysql.connect(**config)

from sklearn.linear_model import LinearRegression
import statsmodels.api
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import r2_score, mean_squared_error

import flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

sql = '''
    select jikwonjik, jikwonpay, YEAR(curdate())-YEAR(jikwonibsail) as year
    from jikwon
'''

data = pd.read_sql(sql, conn)
print(data)

jikpay = data.groupby('jikwonjik')['jikwonpay'].mean().astype(int)



@app.route('/')
def index():
    jikpay = data.groupby('jikwonjik')['jikwonpay'].mean().astype(int)
    jikpay = jikpay.to_dict()
    return render_template('index.html', jikpay = jikpay)


@app.get('/predict')
def predict():
    year = request.args.get('year', type=int)
    x = data[['year']]
    y = data['jikwonpay']
    model = LinearRegression()
    model.fit(x, y)

    coef = round(model.coef_[0], 4)
    intercept = round(model.intercept_, 4)
    r2_score = round(model.score(x, y), 2)
    r2_score = r2_score * 100
    
    pred = model.predict([[year]])
    predpay = int(pred[0])

    predresult = {'coef':coef, 'intercept':intercept, 'r2_score':r2_score, 'predpay':predpay}

    return jsonify(predresult)

if __name__ == '__main__':
    app.run(debug=True)