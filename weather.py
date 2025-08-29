from flask import Flask, render_template, request
import requests
import mysql.connector
from datetime import datetime

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="weather_data"
)
cursor = db.cursor()

API_KEY = "dcc8cceff1883c04d6dd7552b6354ea8"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return "Welcome to my weather forecast page"

@app.route("/weather", methods=["GET", "POST"])
def weather():
    data = []
    city = ""

    if request.method == "POST":
        city = request.form.get("city")

        if city:
           
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            response = requests.get(API_URL, params=params)

            if response.status_code == 200:
                res = response.json()
                city_name = res['name']
                record_date = datetime.fromtimestamp(res['dt'])
                temp = res['main']['temp']
                humidity = res['main']['humidity']
                weather_desc = res['weather'][0]['description']

                cursor.execute(
                    "INSERT INTO weather_data (city, record_date, temperature, humidity, weather) VALUES (%s, %s, %s, %s, %s)",
                    (city_name, record_date, temp, humidity, weather_desc)
                )
                db.commit()

                city = city_name 

            cursor.execute("SELECT * FROM weather_data WHERE city = %s ORDER BY record_date DESC", (city,))
            data = cursor.fetchall()

    return render_template("frontend/weather.html", city=city, data=data)

if __name__ == "__main__":
    app.run(debug=True)
