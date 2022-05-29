from flask import Flask, render_template, Response
import time
import cv2
import imutils
from imutils.video import VideoStream
import pyautogui
app = Flask(__name__)

def gen_frames():
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    tracker = None
    vs = VideoStream(src=0).start()
    scale = 2
    H = 480 // scale
    W = 640 // scale
    up = 160 // scale #Defined boundaries
    down = 320 // scale
    left = 200 // scale
    right = 440 // scale
    pyautogui.PAUSE = 0.0
    wait_time = 0.01
    start = end = 0  
    totalFrames = 0
    skip_frames = 50
   
    while True:
        frame = vs.read()
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=W)
        action = None
        # Run the face detector to find or update face position
        if tracker is None or totalFrames % skip_frames == 0:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect all faces
            faces = detector.detectMultiScale(gray, scaleFactor=1.05,
                                              minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            if len(faces) > 0:
                initBB = faces[0]
                tracker = cv2.legacy_TrackerKCF.create()
                tracker.init(frame, tuple(initBB))
            else:
                tracker = None

        # otherwise the tracker is tracking the face, update the position and grab the new bounding box coordinates of the face
        else:

            (success, box) = tracker.update(frame)

            # if tracking was successful, draw the center point
            if success:
                (x, y, w, h) = [int(v) for v in box]


                centerX = int(x + (w / 2.0))
                centerY = int(y + (h / 2.0))

                # draw a bounding box and the center
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.circle(frame, (centerX, centerY), 5, (0, 255, 0), -1)

                # determine the action
                if centerY < up:
                    action = "up"
                elif centerY > down:
                    action = "down"
                elif centerX < left:
                    action = "left"
                elif centerX > right:
                    action = "right"

            else:
                tracker = None

        end = time.time()

        if action is not None and end - start > wait_time:

            pyautogui.press(action)
            start = time.time()


        cv2.line(frame, (0, up), (W, up), (255, 255, 255), 2)  # UP
        cv2.line(frame, (0, down), (W, down), (255, 255, 255), 2)  # DOWN
        cv2.line(frame, (left, up), (left, down), (255, 255, 255), 2)  # LEFT
        cv2.line(frame, (right, up), (right, down), (255, 255, 255), 2)  # RIGHT

        # increment the totalFrames and draw the action on the frame
        totalFrames += 1
        text = "{}: {}".format("Action", action)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Generate a stream of frame bytes
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
