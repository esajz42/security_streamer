#!/usr/bin/env python
from flask import Flask, render_template, Response, request
from camera_pi import Camera

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def gen(camera, alerts):
    print "gen: " + str(alerts)
    while True:
        frame = camera.get_frame(alerts)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video_feed", methods=["POST", "GET"])
def video_feed():
    alerts = False
    if request.method == "POST":
        if request.form["alerts"] == "Alerts":
            alerts = True
        else:
            alerts = False
    return Response(gen(Camera(), alerts),
            mimetype="multipart/x-mixed-replace; boundary=frame")

#@app.route("/control", methods=["POST"])
#def control():
#    if request.method == "POST":
#        button = request.form["alerts"]
#        session["alerts"] = button
#        return button

if __name__ == "__main__":
    app.run(host="192.168.0.16", port=8080, threaded=True, debug=True)
