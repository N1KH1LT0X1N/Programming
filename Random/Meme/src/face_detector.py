import cv2
import numpy as np
from pathlib import Path

class FaceDetector:
    """Detect faces in images using Haar Cascade classifier"""
    
    def __init__(self):
        # Load the pre-trained Haar Cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise ValueError("Failed to load Haar Cascade classifier")
    
    def detect_faces(self, frame):
        """
        Detect faces in the given frame
        
        Args:
            frame: OpenCV image frame
            
        Returns:
            List of face rectangles (x, y, w, h)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces
    
    def draw_rectangles(self, frame, faces):
        """Draw rectangles around detected faces for debugging"""
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return frame
