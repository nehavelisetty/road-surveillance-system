from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import numpy as np
import json
import os
import base64
from datetime import datetime
import threading
import time
from ml_backend import RoadSurveillanceProcessor

app = Flask(__name__)
CORS(app)

# Global variables
processor = RoadSurveillanceProcessor()
processing_active = False
current_detections = []

class VideoProcessor:
    def __init__(self):
        self.cap = None
        self.processing = False
        
    def start_camera_processing(self, camera_id=0):
        """Start processing from camera feed"""
        global processing_active, current_detections
        
        self.cap = cv2.VideoCapture(camera_id)
        processing_active = True
        
        def process_loop():
            global current_detections
            while processing_active and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    detections = processor.process_frame(frame)
                    current_detections = detections
                    time.sleep(0.1)  # Process at 10 FPS
                else:
                    break
            
            if self.cap:
                self.cap.release()
        
        thread = threading.Thread(target=process_loop)
        thread.daemon = True
        thread.start()
        
    def stop_processing(self):
        """Stop camera processing"""
        global processing_active
        processing_active = False
        if self.cap:
            self.cap.release()

video_processor = VideoProcessor()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'processing_active': processing_active
    })

@app.route('/api/start_detection', methods=['POST'])
def start_detection():
    """Start real-time detection"""
    try:
        data = request.get_json() or {}
        camera_id = data.get('camera_id', 0)
        
        video_processor.start_camera_processing(camera_id)
        
        return jsonify({
            'success': True,
            'message': 'Detection started',
            'camera_id': camera_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stop_detection', methods=['POST'])
def stop_detection():
    """Stop real-time detection"""
    try:
        video_processor.stop_processing()
        
        return jsonify({
            'success': True,
            'message': 'Detection stopped'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get_detections', methods=['GET'])
def get_detections():
    """Get current detection results"""
    global current_detections
    
    return jsonify({
        'success': True,
        'detections': current_detections,
        'count': len(current_detections),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    """Upload and process file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save uploaded file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Process the file
        if filename.lower().endswith(('.mp4', '.avi', '.mov')):
            # Video processing
            detections = processor.process_video(filepath)
        else:
            # Image processing
            detections = processor.process_image(filepath)
        
        # Save results
        results_file = os.path.join('processed', f"{filename}_results.json")
        with open(results_file, 'w') as f:
            json.dump(detections, f, indent=2)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'detections': detections,
            'count': len(detections)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get_statistics', methods=['GET'])
def get_statistics():
    """Get detection statistics"""
    try:
        # Read all result files
        processed_dir = 'processed'
        all_detections = []
        
        if os.path.exists(processed_dir):
            for filename in os.listdir(processed_dir):
                if filename.endswith('_results.json'):
                    filepath = os.path.join(processed_dir, filename)
                    with open(filepath, 'r') as f:
                        detections = json.load(f)
                        all_detections.extend(detections)
        
        # Calculate statistics
        total_detections = len(all_detections)
        lane_markings = sum(1 for d in all_detections if d.get('type') == 'lane_marking')
        road_damage = sum(1 for d in all_detections if d.get('type') == 'road_damage')
        high_severity = sum(1 for d in all_detections if d.get('severity') == 'high')
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_detections': total_detections,
                'lane_markings': lane_markings,
                'road_damage': road_damage,
                'high_severity': high_severity,
                'average_confidence': np.mean([d.get('confidence', 0) for d in all_detections]) if all_detections else 0
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Road Surveillance API Server...")
    print("Make sure to run setup_environment.py first!")
    
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
