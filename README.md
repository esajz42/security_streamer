# Security Streamer

Security Streamer is an app designed to make a Rasberry Pi with a camera module into a remotely viewable security camera, which can also send email alerts. 

## Table of Contents

* [Dependencies](#dependencies)
* [Getting Started](#getting-started)
* [Acknowledgements](#acknowledgements)

## Dependencies

1. Python 2.7
2. OpenCV

## Getting Started

Getting python, the raspberry pi camera, and OpenCV working are required for this app. There are plenty of great resources
describing these processes. My [Acknowledgments](#acknowledgements) have some good ones. Also Google.

First things first, acquire a domain name to use as your security camera's homepage. Free dynamic DNS service is offered from
[noip](https://www.noip.com/login), but needs to be renewed monthly. Take note of the IP connected to your new domain name. 

Next, clone the security streamer repository onto your Raspberry Pi. Make sure that `app.py` and `autorun_app.py` have permission to
execute with `chmod +x`. Edit app.py to point to the IP address of your website (last line).

Now create a pickle file with python that contains the username and password you will use to log onto your website and view the 
stream. Edit `flask_auth.py` to point to this pickle, using absolute paths. 

Create another pickle that contains the email address and password for the Gmail account you will use to send images containing
motion to other email addresses. This pickle should also have the email address(es) you want to send these images to and the 
message body for the emails. You can infer the structure of the pickle from what I have in `app.py`, though I will eventually
improve this documentation to spell it out. Finally, update app.py to point to your new pickle with an absolute path. 

From this point, you can run `python app.py` and check out your video stream! Use the buttons on your webpage to turn email alerts on 
or off. 

If your restart your Raspberry Pi frequently or are worried about power outages, you can add the line `bash /path/to/autorun_app.py`
to your `/etc/rc.local file`. This will make the server run when your Pi reboots. A word of warning, I `pkill apache` in that script
because of the unique and special (read: bad) way I have things running on my own Pi. If you use apache for other things on your
pi, then remove this line. 

I'd like to create a config script in the future to streamline this, but probably won't. Maybe if people actually start using this
code!

## Acknowledgements

1. Miguel Grinberg's [Video Streaming with Flask](http://blog.miguelgrinberg.com/post/video-streaming-with-flask) blog post and camera_pi.py code, which I've used with only minor modifications.
2. pyimagesearch.com's [Install OpenCV and Python on your Raspberry Pi 2 and B+](http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/)
3. stackoverflow answer from dirn demonstrating [restricting access to endpoints](http://stackoverflow.com/questions/29725217/password-protect-one-webpage-in-flask-app) in flask.
