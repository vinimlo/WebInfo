import json
import requests as req

from flask import Flask, request, make_response, jsonify, render_template, redirect, url_for, session

url = 'https://eonet.sci.gsfc.nasa.gov/api/v2.1/events'

app = Flask(__name__)
app.secret_key = "MINHA_CHAVE_CRIPTOGRAFADA"

resp = req.get(url)

data = json.loads(resp.text)

userInput = 8

events = {}
imgUrl = {}

def gets_events():
    count = 0
    for key, val in data.items():
        if(key == "events"):
            for event in val:
                for title, value in event.items():
                    if title == "id":
                        event_id = value
                    if title == "categories":
                        for a in value:
                            for b,c in a.items():
                                if(b == "id"):
                                    id = c
                                    if(id == int(userInput)):
                                        # print(event)
                                        events[event_id] = event
    return events

def gets_images(events):
    # print(events)

    for event, event_value in events.items():
        for title, value in event_value.items():
            if title == "geometries":
                for geometries in value:
                    for geometry, geometry_value in geometries.items():
                        if geometry == "coordinates":
                            apiUrl = 'https://api.nasa.gov/planetary/earth/imagery/?lon={}&lat={}&date=2017-02-01&cloud_score=True&api_key=ZsN3etuq4qjAUe9TEPWte1R4agCptOmlOrNtzW6a'.format(geometry_value[0], geometry_value[1])
                            # print(apiUrl)
                            imgResp = req.get(apiUrl)
                            imgData = json.loads(imgResp.text)
                            for imgKey, imgVal in imgData.items():
                                if imgKey == "url":
                                    imgUrl[geometry_value[0],geometry_value[1]] = imgVal
                                    # print(imgUrl)
    return imgUrl


events = gets_events()
imgUrl = gets_images(events)

@app.route('/')
def hello():
    return render_template('index.html'), 200

@app.route('/events')
def return_events():
    return render_template('events.html', events=events, imgUrl=imgUrl), 200

# @app.route('/events', methods=['POST'])
# def return_events():
#     if request.method == "POST":
#         session['event'] = request.form["events"]
#         return render_template('events.html', events=events, imgUrl=imgUrl), 200
#     return redirect(url_for("index.html"))

if __name__ == '__main__':
    app.run(debug=True)
