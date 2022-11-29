import os
import datetime
from re import L, split
from typing import Type
from flask.scaffold import F
import pytz
from cs50 import SQL
from flask import Flask, jsonify, flash, redirect, render_template, request, session, url_for
from PIL import Image
from flask_session import Session
from tempfile import mkdtemp
import requests
from sqlalchemy.sql.operators import op
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Configure application
application = Flask(__name__)

# Ensure templates are auto-reloaded
application.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Debug setting
application.config['ENV'] = 'development'
application.config['DEBUG'] = True
application.config['TESTING'] = True

# Configure session to use filesystem (instead of signed cookies)
application.config["SESSION_FILE_DIR"] = mkdtemp()
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(application)

# home page


@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        city_name = request.form.get('city_name')

        # take a variable to show the json data
        r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' +
                         city_name+'&units=metric&appid=c2092d5bcfca757e5cab335af5de9958')

        if r:
            # read the json object
            json_object = r.json()

            # take some attributes like temperature,humidity,pressure of this
            # this temparetuure in kelvin
            temperature = int(json_object['main']['temp'])
            feels = int(json_object['main']['feels_like'])
            maxTemp = int(json_object['main']['temp_max'])
            minTemp = int(json_object['main']['temp_min'])
            humidity = int(json_object['main']['humidity'])
            pressure = int(json_object['main']['pressure'])
            wind = int(json_object['wind']['speed'])
            country = json_object['sys']['country']

            # atlast just pass the variables
            condition = json_object['weather'][0]['main']
            desc = json_object['weather'][0]['description']
            icon = json_object['weather'][0]['icon']

            return jsonify(temperature=temperature, pressure=pressure, humidity=humidity, city_name=city_name, condition=condition, wind=wind,
                           desc=desc, feels=feels, minTemp=minTemp, maxTemp=maxTemp, icon=icon, country=country)
        else:
            print('NNOOOOOOO DAAATTAA')
            suck = 'noData'
            return jsonify(suck=suck)

    # Weather reports for 20 pre-selected cities
    cities = ['Tianjin', 'New York', 'London', 'Shanghai', 'San Fransisco', 'Zurich', 'Tokyo', 'Sydney', 'Dubai',
              'Munich', 'Delhi', 'Seoul', 'Paris', 'Los Angeles', 'Hong Kong', 'Mumbai', 'Singapore', 'Berlin', 'Beijing', 'Chicago']
    reportsCards = []

    for i in cities:
        city = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' +
                            i+'&units=metric&appid=c2092d5bcfca757e5cab335af5de9958')
        json_object = city.json()

        temperature = int(json_object['main']['temp'])
        feels = int(json_object['main']['feels_like'])
        pressure = int(json_object['main']['pressure'])
        wind = int(json_object['wind']['speed'])
        condition = json_object['weather'][0]['main']
        desc = json_object['weather'][0]['description']

        report = {'cityName': i, 'temp': temperature,
                  'desc': desc, 'wnd': wind, 'cond': condition, 'fls': feels}

        reportsCards.append(report.copy())

    return render_template('index.html', reportsC=reportsCards)


@application.route("/aboutme", methods=["GET", "POST"])
def aboutme():
    return render_template('about_me.html')


@application.route("/aboutproject", methods=["GET", "POST"])
def aboutproject():
    return render_template('about_project.html')


@application.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    application.run(debug=False, use_debugger=True, use_reloader=True)
