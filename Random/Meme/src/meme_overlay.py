import cv2
import numpy as np
from PIL import Image
from pathlib import Path

class MemeOverlay:
    """Handle meme overlay functionality"""
    
    def __init__(self, memes_dir='memes'):
        self.memes_dir = Path(memes_dir)
        self.memes = {}
        self.current_meme = 0
        self.meme_names = []
        self.load_memes()
    
    def load_memes(self):
        """Load all meme images from the memes directory"""
        if not self.memes_dir.exists():
            print(f"Warning: {self.memes_dir} directory not found")
            return
        
        # Load PNG meme images
        for meme_file in sorted(self.memes_dir.glob('*.png')):
            try:
                img = cv2.imread(str(meme_file), cv2.IMREAD_UNCHANGED)
                if img is not None:
                    meme_name = meme_file.stem
                    self.memes[meme_name] = img
                    self.meme_names.append(meme_name)
                    print(f"Loaded meme: {meme_name}")
            except Exception as e:
                print(f"Error loading {meme_file}: {e}")
        
        if not self.memes:
            print("No memes loaded. Using default solid color overlay.")
    
    def overlay_meme(self, frame, face_rect, meme_name=None):
        """
        Overlay a meme image on a detected face
        
        Args:
            frame: OpenCV image frame
            face_rect: Tuple (x, y, w, h) for face location
            meme_name: Name of meme to overlay (uses current if None)
            
        Returns:
            Modified frame with meme overlay
        """
        x, y, w, h = face_rect
        
        # If no memes loaded, use a colored rectangle
        if not self.memes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
            cv2.putText(frame, "Meme", (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            return frame
        
        # Get the meme image
        meme_name = meme_name or self.meme_names[self.current_meme % len(self.meme_names)]
        meme_img = self.memes.get(meme_name)
        
        if meme_img is None:
            return frame
        
        # Resize meme to match face size
        resized_meme = cv2.resize(meme_img, (w, h), interpolation=cv2.INTER_LINEAR)
        
        # Handle alpha channel for transparency
        if resized_meme.shape[2] == 4:  # Has alpha channel
            alpha = resized_meme[:, :, 3] / 255.0
            meme_rgb = resized_meme[:, :, :3]
            
            # Blend the meme with the background
            for c in range(3):
                frame[y:y+h, x:x+w, c] = (
                    meme_rgb[:, :, c] * alpha +
                    frame[y:y+h, x:x+w, c] * (1 - alpha)
                ).astype(np.uint8)
        else:
            # No alpha channel, direct overlay
            frame[y:y+h, x:x+w] = resized_meme[:, :, :3]
        
        return frame
    
    def next_meme(self):
        """Switch to next meme"""
        if self.meme_names:
            self.current_meme = (self.current_meme + 1) % len(self.meme_names)
            print(f"Switched to: {self.meme_names[self.current_meme]}")
    
    def get_current_meme_name(self):
        """Get name of current meme"""
        if self.meme_names:
            return self.meme_names[self.current_meme]
        return "None"
