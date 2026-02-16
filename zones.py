import cv2
import numpy as np

class ZoneManager:
    def __init__(self):
        # Define default zones (can be updated later)
        self.zones = {}
        self.load_zones()

    def load_zones(self):
        import json
        import os
        
        json_path = 'zones.json'
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
                for name, coords in data.items():
                    self.zones[name] = np.array(coords, np.int32)
        else:
            # Default zones if file doesn't exist
            self.zones = {
                "entry": np.array([[100, 100], [200, 100], [200, 200], [100, 200]], np.int32),
                "checkout": np.array([[300, 100], [400, 100], [400, 200], [300, 200]], np.int32),
                "exit": np.array([[500, 100], [600, 100], [600, 200], [500, 200]], np.int32)
            }

    def check_zone(self, point):
        # Check which zone the point is in
        for zone_name, polygon in self.zones.items():
            result = cv2.pointPolygonTest(polygon, point, False)
            if result >= 0:
                return zone_name
        return None

    def draw_zones(self, frame):
        # Zones are hidden as per user request
        # overlay = frame.copy()
        # for name, polygon in self.zones.items():
        #     color = (0, 255, 0) # Green default
        #     if name == 'checkout': color = (0, 255, 255) # Yellow
        #     elif name == 'exit': color = (0, 0, 255) # Red
        #     
        #     cv2.polylines(frame, [polygon], True, color, 2)
        #     cv2.fillPoly(overlay, [polygon], color)
            
        # # Add transparency (subtle)
        # alpha = 0.1
        # cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        return frame
