import time
import io
import threading
import picamera
import cv2
import copy
import numpy as np


class Camera(object):
    motion_frame = None
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.motion_frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = False

            # let camera warm up
            camera.start_preview()
            time.sleep(2)
            
            def detect_motion(frame):
                # make frame steams into image arrays
                ref = cv2.imdecode(np.fromstring(frame, dtype=np.uint8), 1)
                new = cv2.imdecode(np.fromstring(cls.frame, dtype=np.uint8), 1)

                ref_gray = cv2.cvtColor(ref.copy(), cv2.COLOR_BGR2GRAY)
                new_gray = cv2.cvtColor(new.copy(), cv2.COLOR_BGR2GRAY)
                
                # blur images
                ref_blur = cv2.GaussianBlur(ref_gray, (7, 7), 0)
                new_blur = cv2.GaussianBlur(new_gray, (7, 7), 0)
               
               # difference images and find change countours
                delta = cv2.absdiff(ref_blur, new_blur)
                thresh = cv2.dilate(cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
                (cnts, _) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # draw bounding boxes about large contours
                for c in cnts:
                    if cv2.contourArea(c) < 500:
                        continue
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    cv2.putText(new, "occupied", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # reencode image to memory buffer
                new_buff = cv2.imencode(".jpeg", new, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tostring()

                try:
                    return new_buff
                except NameError:
                    return cls.frame      

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
 
                cls.frame = stream.read()
                
                # return camera image with detected motion bounding boxes
                try:
                    cls.motion_frame = detect_motion(old_stream)
                except NameError:
                    cls.motion_frame = detect_motion(cls.frame)

                old_stream = copy.deepcopy(cls.frame)

                # reset streams for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
