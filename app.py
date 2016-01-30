#!/usr/bin/env python
import pickle
from flask import Flask, render_template, Response, request
from flask_auth import requires_auth
from camera_pi import Camera
from emailer import Email

alerts = False

messager_info = pickle.load(open("../rpi_security_tests/messager_info.pickle", "rb"))
messagers = [Email(messager_info[0], messager_info[1], messager_info[2][0], messager_info[3]),
        Email(messager_info[0], messager_info[1], messager_info[2][1], messager_info[3])]

app = Flask(__name__)

@app.route("/")
@requires_auth
def index():
    return render_template("index.html")

def gen(camera):
    global alerts
    while True:
        frame = camera.get_frame(alerts)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera(messagers=messagers)),
            mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/control", methods=["POST"])
@requires_auth
def control():
    global alerts
    alerts = request.form["alerts"] == "Alerts"
    return str(alerts)

if __name__ == "__main__":
    app.run(host="192.168.0.16", port=8080, threaded=True, debug=True)
