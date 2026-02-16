import cv2
from ultralytics import YOLO
import numpy as np
from tracker_manager import TrackerManager
from zones import ZoneManager
from analytics import Analytics
from wzstation_connector import WZStationConnector
from face_manager import FaceManager

def main():
    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt') 

    # Initialize WZStation Connector
    # For now, it uses default camera (0). User can change this to an RTSP URL.
    # Example: connector = WZStationConnector("rtsp://admin:password@192.168.1.10:554/stream1")
    # Use test video if available
    import os
    source = "test_video.mp4" if os.path.exists("test_video.mp4") else 0
    connector = WZStationConnector(source) 
    if not connector.connect():
        return

    tracker_manager = TrackerManager()
    zone_manager = ZoneManager()
    analytics = Analytics()
    face_manager = FaceManager() # Initialize FaceManager

    while True:
        success, frame = connector.get_frame()
        if not success:
            break

        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        # Filter for class 0 (person)
        results = model.track(frame, persist=True, classes=[0])

        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist() if results[0].boxes.id is not None else []

        # Customize visualization (cleaner look)
        annotated_frame = frame.copy()
        
        # Draw zones first (background)
        annotated_frame = zone_manager.draw_zones(annotated_frame)

        # Update tracker and zones logic
        current_tracks = tracker_manager.update(boxes, track_ids, zone_manager)
        
        # Process logic for each track
        for track_id, data in current_tracks.items():
            # Face Recognition Integration
            # Only try to recognize if we haven't identified this track yet, or periodically
            if data.get('name', 'Unknown') == 'Unknown':
                # Find the box for this track
                # This is a bit inefficient (O(N)), but N is small
                try:
                    idx = track_ids.index(track_id)
                    box = boxes[idx]
                    
                    # Recognize face
                    name = face_manager.recognize_face(frame, box)
                    if name != "Unknown":
                        tracker_manager.set_name(track_id, name)
                except ValueError:
                    pass # Track ID might have been lost in this specific frame but kept in history

        # Draw minimalist track info
        for track_id, data in current_tracks.items():
            # Find the box for this track
            try:
                idx = track_ids.index(track_id)
                x, y, w, h = boxes[idx]
                x, y, w, h = int(x - w/2), int(y - h/2), int(w), int(h) # Convert xywh center to top-left
                
                # Determine color based on status
                status = data.get('status', 'Visitante')
                color = (255, 255, 255) # White
                if 'Comprador' in status: color = (0, 255, 0) # Green
                elif 'Nao Comprou' in status: color = (0, 0, 255) # Red

                # Draw simple box
                cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), color, 2)
                
                # Draw minimal label
                label = f"{status}"
                cv2.putText(annotated_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            except ValueError:
                pass

        # Update analytics display
        # We need a way to count completed paths, not just current state
        # For simplicity, let's count persistent distinct IDs in 'entry' as entries
        # And distinct IDs that visited 'checkout' as conversions.
        
        # Update analytics with current tracks
        analytics.update_counts(current_tracks)

        # Draw analytics overlay
        analytics.draw_overlay(annotated_frame)

        # Display the annotated frame
        cv2.imshow("Retail Analytics", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    connector.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
