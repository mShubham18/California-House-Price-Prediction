from flask import Flask,request,jsonify,render_template,url_for
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
import pickle

elastic_model = pickle.load(open("models/ElasticNet.pkl","rb"))
scaler_model = pickle.load(open("models/scaler.pkl","rb"))
application = Flask(__name__)
app = application


@app.route("/",methods=["GET","POST"])
def predict_datapoint():
    if request.method=="POST":
        longitude = float(request.form.get("longitude"))
        latitude = float(request.form.get("latitude"))
        housing_median_age = int(request.form.get("housing_median_age"))
        total_rooms = int(request.form.get("total_rooms"))
        total_bedrooms = int(request.form.get("total_bedrooms"))
        population = int(request.form.get("population"))
        households = int(request.form.get("households"))
        median_income = float(request.form.get("median_income"))

        new_data_scaled = scaler_model.transform([[longitude,latitude,housing_median_age,total_rooms,total_bedrooms,population,households,median_income]])
        result = elastic_model.predict(new_data_scaled)[0]
        return render_template("form.html",result = f"{result:.2f}")
    else:
        return render_template("form.html")


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)