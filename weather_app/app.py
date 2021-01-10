import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

class weather(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)

@app.route('/', methods=['POST', 'GET'])
def weather_data():
    # cities = weather.query_all()
    # url = "https://community-open-weather-map.p.rapidapi.com/weather"
    # querystring = {"q":"London,uk","lat":"0","lon":"0","callback":"test","id":"2172797","lang":"null","units":"\"metric\" or \"imperial\"","mode":"xml, html"}
    # headers = {
    #     'x-rapidapi-key': "0ecda68496msh92f92a6bc393ec8p1e58f7jsn47de6a52c22c",
    #     'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    #     }
    # response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)
    if request.method == 'POST':
        city_name = request.form['city']
        if city_name:
            new_city = weather(name = city_name)
            db.session.add(new_city)
            db.session.commit()
    
    cities = weather.query.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=b85543cb128aa2dcb4e7917658e0616e'
    weather_data_list = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather_data = {
            'city': city.name,
            'description':r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'temperature':r['main']['temp']
        }
        weather_data_list.append(weather_data)
    return render_template('weather.html', weather_data_list = weather_data_list)

if __name__ == '__main__':
    app.run(debug=True)