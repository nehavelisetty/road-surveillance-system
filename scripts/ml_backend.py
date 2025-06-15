import cv2
import numpy as np
import json
import os
from datetime import datetime
import base64

class LaneMarkingDetector:
    def __init__(self):
        self.kernel = np.ones((5,5), np.uint8)
        
    def detect_lane_markings(self, image):
        """Detect lane markings using computer vision techniques"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection using Canny
        edges = cv2.Canny(blur, 50, 150)
        
        # Define region of interest (lower half of image)
        height, width = edges.shape
        mask = np.zeros_like(edges)
        polygon = np.array([[
            (0, height),
            (0, height//2),
            (width, height//2),
            (width, height)
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_edges = cv2.bitwise_and(edges, mask)
        
        # Hough line detection
        lines = cv2.HoughLinesP(
            masked_edges, 
            rho=1, 
            theta=np.pi/180, 
            threshold=50,
            minLineLength=100,
            maxLineGap=50
        )
        
        detections = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Calculate confidence based on line length and angle
                length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                angle = np.arctan2(y2-y1, x2-x1) * 180 / np.pi
                
                # Filter for lane-like lines
                if length > 50 and abs(angle) < 45:
                    confidence = min(length / 200, 1.0)
                    detections.append({
                        'type': 'lane_marking',
                        'confidence': confidence,
                        'coordinates': [x1, y1, x2, y2],
                        'length': length,
                        'angle': angle
                    })
        
        return detections

class RoadDamageDetector:
    def __init__(self):
        self.min_contour_area = 100
        
    def detect_road_damage(self, image):
        """Detect road damage using texture analysis and contour detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply morphological operations to enhance damage features
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
        
        # Combine tophat and blackhat
        enhanced = cv2.add(tophat, blackhat)
        
        # Threshold to get binary image
        _, binary = cv2.threshold(enhanced, 30, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate features for severity assessment
                aspect_ratio = w / h
                extent = area / (w * h)
                
                # Determine severity based on size and shape
                if area > 1000:
                    severity = 'high'
                elif area > 500:
                    severity = 'medium'
                else:
                    severity = 'low'
                
                confidence = min(area / 2000, 1.0)
                
                detections.append({
                    'type': 'road_damage',
                    'confidence': confidence,
                    'bbox': [x, y, w, h],
                    'area': area,
                    'severity': severity,
                    'aspect_ratio': aspect_ratio,
                    'extent': extent
                })
        
        return detections

class RoadSurveillanceProcessor:
    def __init__(self):
        self.lane_detector = LaneMarkingDetector()
        self.damage_detector = RoadDamageDetector()
        
    def process_frame(self, image):
        """Process a single frame and return all detections"""
        # Detect lane markings
        lane_detections = self.lane_detector.detect_lane_markings(image)
        
        # Detect road damage
        damage_detections = self.damage_detector.detect_road_damage(image)
        
        # Combine all detections
        all_detections = lane_detections + damage_detections
        
        # Add timestamp and unique IDs
        timestamp = datetime.now().isoformat()
        for i, detection in enumerate(all_detections):
            detection['id'] = f"{timestamp}_{i}"
            detection['timestamp'] = timestamp
        
        return all_detections
    
    def process_video(self, video_path):
        """Process entire video file"""
        cap = cv2.VideoCapture(video_path)
        all_detections = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process every 10th frame to reduce computation
            if frame_count % 10 == 0:
                detections = self.process_frame(frame)
                for detection in detections:
                    detection['frame_number'] = frame_count
                all_detections.extend(detections)
            
            frame_count += 1
        
        cap.release()
        return all_detections
    
    def process_image(self, image_path):
        """Process single image"""
        image = cv2.imread(image_path)
        if image is None:
            return []
        
        return self.process_frame(image)

# Example usage and testing
def main():
    processor = RoadSurveillanceProcessor()
    
    # Create a sample image for testing
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some lane-like lines
    cv2.line(test_image, (100, 400), (200, 300), (255, 255, 255), 3)
    cv2.line(test_image, (400, 400), (500, 300), (255, 255, 255), 3)
    
    # Add some damage-like spots
    cv2.circle(test_image, (300, 350), 20, (50, 50, 50), -1)
    cv2.ellipse(test_image, (450, 380), (30, 15), 0, 0, 360, (40, 40, 40), -1)
    
    # Process the test image
    detections = processor.process_frame(test_image)
    
    print("Detection Results:")
    print(json.dumps(detections, indent=2))
    
    print(f"\nTotal detections: {len(detections)}")
    lane_count = sum(1 for d in detections if d['type'] == 'lane_marking')
    damage_count = sum(1 for d in detections if d['type'] == 'road_damage')
    print(f"Lane markings: {lane_count}")
    print(f"Road damage: {damage_count}")

if __name__ == "__main__":
    main()
