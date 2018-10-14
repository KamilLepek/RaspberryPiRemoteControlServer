from flask import *
from camera import Camera
import os

htmlDir = os.path.abspath('HTML')

app = Flask(__name__,  template_folder=htmlDir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')


def stream(camera):
    while True:
        frame = camera.streaming()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_stream')
def video_stream():
    return Response(stream(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
