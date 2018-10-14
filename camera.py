import io
import time
import threading
import picamera


class Camera(object):
    curr_frame = None
    
    res_width = 1280
    res_height = 720
    
    streaming_started = False
    
    def streaming(self):
        if self.streaming_started is False:
            threading.Thread(target=self.streaming_thread).start()
            self.streaming_started = True
            while self.curr_frame is None:
                time.sleep(0)
        return self.curr_frame

    @classmethod
    def streaming_thread(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (cls.res_width, cls.res_height)
            io_stream = io.BytesIO()
            for frame in camera.capture_continuous(io_stream, 'jpeg', use_video_port=True):
                io_stream.seek(0)
                cls.curr_frame = io_stream.read()
                io_stream.seek(0)
                io_stream.truncate()
