#!/usr/bin/env python
from flask import Flask, render_template, Response, request
from flask_auth import requires_auth
from camera_pi import Camera

alerts = False

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
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/control", methods=["POST"])
@requires_auth
def control():
    global alerts
    alerts = request.form["alerts"] == "Alerts"
    return str(alerts)

if __name__ == "__main__":
    app.run(host="192.168.0.16", port=8080, threaded=True, debug=True)
