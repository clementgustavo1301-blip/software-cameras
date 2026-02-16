class TrackerManager:
    def __init__(self):
        self.tracks = {}

    def update(self, boxes, track_ids, zone_manager):
        # Update track positions and check zones
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            # Use bottom center point (feet) for better accuracy
            feet_point = (int(x), int(y + h / 2))
            
            if track_id not in self.tracks:
                self.tracks[track_id] = {
                    'positions': [],
                    'zones_visited': set(),
                    'current_zone': None,
                    'has_paid': False,
                    'status': 'Visitante'
                }
            
            # Update position history
            self.tracks[track_id]['positions'].append(feet_point)
            
            # Check current zone
            current_zone = zone_manager.check_zone(feet_point)
            if current_zone:
                self.tracks[track_id]['zones_visited'].add(current_zone)
                self.tracks[track_id]['current_zone'] = current_zone
                
                if current_zone == 'checkout':
                    self.tracks[track_id]['has_paid'] = True
                    self.tracks[track_id]['status'] = 'Comprador'
                
                elif current_zone == 'exit':
                    if self.tracks[track_id]['has_paid']:
                         self.tracks[track_id]['status'] = 'Comprador (Saindo)'
                    else:
                        self.tracks[track_id]['status'] = 'Nao Comprou'

        return self.tracks

    def set_name(self, track_id, name):
        if track_id in self.tracks:
            self.tracks[track_id]['name'] = name
