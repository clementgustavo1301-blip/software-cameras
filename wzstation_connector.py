import cv2

class WZStationConnector:
    def __init__(self, rtsp_url=None):
        self.rtsp_url = rtsp_url
        self.cap = None

    def connect(self):
        """
        Connects to the RTSP stream or default camera.
        """
        source = self.rtsp_url if self.rtsp_url else 0
        print(f"Connecting to video source: {source}")
        self.cap = cv2.VideoCapture(source)
        
        if not self.cap.isOpened():
            print("Error: Could not open video source.")
            return False
        return True

    def get_frame(self):
        """
        Reads a frame from the connected source.
        """
        if self.cap and self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                return True, frame
        return False, None

    def release(self):
        """
        Releases the video capture resource.
        """
        if self.cap:
            self.cap.release()
