import cv2
import numpy as np

class FaceManager:
    def __init__(self, db_path='faces_db'):
        self.db_path = db_path
        print("WARNING: Face recognition is DISABLED due to missing dependencies (dlib).")
        print("To enable, please install 'dlib' and 'face_recognition'.")

    def load_known_faces(self):
        pass

    def recognize_face(self, frame, box):
        return "Unknown"
