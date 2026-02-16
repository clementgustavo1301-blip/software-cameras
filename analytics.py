import cv2

class Analytics:
    def __init__(self):
        self.total_entries = 0
        self.total_checkouts = 0
        self.conversions = 0.0

    def increment_entry(self):
        self.total_entries += 1
        self.calculate_conversion()

    def update_counts(self, tracks):
        # Calculate stats based on current tracks
        # Note: In a real system, we'd need to persist this history even after tracks disappear
        visitors = len(tracks)
        buyers = sum(1 for t in tracks.values() if t['has_paid'] or 'Comprador' in t['status'])
        
        self.total_entries = visitors
        self.total_checkouts = buyers
        self.calculate_conversion()

    def calculate_conversion(self):
        if self.total_entries > 0:
            self.conversions = (self.total_checkouts / self.total_entries) * 100
        else:
            self.conversions = 0.0

    def draw_overlay(self, frame):
        # Draw a stats box
        cv2.rectangle(frame, (10, 10), (300, 120), (0, 0, 0), -1)
        
        cv2.putText(frame, f"Visitantes: {self.total_entries}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(frame, f"Compradores: {self.total_checkouts}", (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Conversao: {self.conversions:.1f}%", (20, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
