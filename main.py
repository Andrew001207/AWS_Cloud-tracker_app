# coding: utf-8

from flask import Flask, render_template, request, redirect
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import MQTT

app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBTfQk2e0_GziHCnrhHYcVituFAWEgBIuQ"

# you can also pass key here
GoogleMaps(
    app,
    #key="AIzaSyDP0GX-Wsui9TSDxtFNj2XuKrh7JBTPCnU"
)

# NOTE: this example is using a form to get the apikey

def makePin(lat, lon):
    return  {
                'icon': icons.dots.green,
                'lat': lat,
                'lng': lon,
                # 'infobox':  "<p><b>Місце:</b><br><b>Рейтинг:</b><br><b>Коментарі:</b><br></p>"
            }

def updateReviews():
    print(MQTT.location.items())
    return tuple([makePin(*item[1]) for item in MQTT.location.items()])

@app.route("/", methods=["GET", "POST"])
def mapview():
    print('called')
    markers = updateReviews()
    print(len(markers))
    twmap = Map(
        identifier="twmap",
        varname="twmap",
        style=(
            "height:100%;"
            "width:100%;"
            "left:0;"
            "position:absolute;"
            # "z-index:200;"            
        ),
        lat=46.44,
        lng=30.75,
        zoom = 12.5,
        markers=markers
    )

    return render_template(
        'main.html',
        twmap=twmap,
        GOOGLEMAPS_KEY=request.args.get('apikey')
    )

@app.route("/team", methods=["GET", "POST"])
def about_us():
    return render_template('about_us.html')


@app.route('/clickpost/', methods=['POST'])
def clickpost():
    # Now lat and lon can be accessed as:
    lat = request.form['lat']
    lng = request.form['lng']
    print(lat)
    print(lng)
    return "ok"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host= '0.0.0.0', port = 5001)
