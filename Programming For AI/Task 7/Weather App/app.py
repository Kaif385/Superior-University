from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "722da275ed9b2835e7736988acdbfe36"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        city = request.form["city"]  
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"  
        }
        response = requests.get(BASE_URL, params=params)
        weather_data = response.json()  

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)

