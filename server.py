from flask import *
from camera import Camera
from movement import Movement
import os

htmlDir = os.path.abspath('HTML')
robot = Movement()
app = Flask(__name__,  template_folder=htmlDir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/video_stream')
def video_stream():
    return Response(stream(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/move', methods=['POST'])
def move_forward():
    param = request.form["param"]
    if param == "forward":
        robot.forward()
    if param == "backward":
        robot.backward()
    if param == "left":
        robot.left()
    if param == "right":
        robot.right()

@app.route('/stop', methods=['POST'])
def stop():
    robot.stop()


def stream(camera):
    while True:
        frame = camera.streaming()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
