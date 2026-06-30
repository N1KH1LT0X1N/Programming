import cv2
import numpy as np
from pathlib import Path
from face_detector import FaceDetector
from meme_overlay import MemeOverlay

def create_placeholder_memes():
    """Create placeholder meme images for testing"""
    memes_dir = Path('memes')
    memes_dir.mkdir(exist_ok=True)
    
    # Only create if empty
    if list(memes_dir.glob('*.png')):
        return
    
    # Create 5 simple placeholder meme images
    meme_types = [
        ('surprised', (0, 0, 255)),      # Red
        ('angry', (0, 255, 255)),         # Yellow
        ('cool', (255, 0, 0)),            # Blue
        ('heart_eyes', (255, 0, 255)),    # Magenta
        ('sunglasses', (255, 165, 0))     # Orange
    ]
    
    for name, color in meme_types:
        # Create a simple image with text
        img = np.ones((200, 200, 4), dtype=np.uint8) * 255
        img[:, :, :3] = color
        img[:, :, 3] = 200  # Semi-transparent
        
        # Add text
        cv2.putText(img, name.replace('_', ' ').upper(), 
                   (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (255, 255, 255), 2)
        
        # Save as PNG to preserve alpha channel
        cv2.imwrite(str(memes_dir / f'{name}.png'), img)
        print(f"Created placeholder: {name}.png")

def main():
    """Main application loop"""
    print("=== Viral Meme Face Filter ===")
    print("Loading resources...")
    
    # Create placeholder memes for testing
    create_placeholder_memes()
    
    # Initialize components
    try:
        detector = FaceDetector()
        overlay = MemeOverlay('memes')
    except Exception as e:
        print(f"Error initializing: {e}")
        return
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return
    
    print("\nControls:")
    print("  1-5: Switch meme")
    print("  SPACE: Toggle meme overlay")
    print("  s: Save screenshot")
    print("  q or ESC: Quit\n")
    
    overlay_enabled = True
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame")
                break
            
            frame_count += 1
            
            # Detect faces
            faces = detector.detect_faces(frame)
            
            # Apply meme overlay or debug rectangles
            if overlay_enabled and overlay.meme_names:
                for face_rect in faces:
                    frame = overlay.overlay_meme(frame, face_rect)
            else:
                frame = detector.draw_rectangles(frame, faces)
            
            # Add UI information
            meme_status = overlay.get_current_meme_name() if overlay_enabled else "OFF"
            ui_text = f"Meme: {meme_status} | Faces: {len(faces)}"
            cv2.putText(frame, ui_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Viral Meme Face Filter', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == 27:  # q or ESC
                print("Exiting...")
                break
            elif key == ord('1'):
                overlay.current_meme = 0
                print(f"Switched to: {overlay.meme_names[0]}")
            elif key == ord('2') and len(overlay.meme_names) > 1:
                overlay.current_meme = 1
                print(f"Switched to: {overlay.meme_names[1]}")
            elif key == ord('3') and len(overlay.meme_names) > 2:
                overlay.current_meme = 2
                print(f"Switched to: {overlay.meme_names[2]}")
            elif key == ord('4') and len(overlay.meme_names) > 3:
                overlay.current_meme = 3
                print(f"Switched to: {overlay.meme_names[3]}")
            elif key == ord('5') and len(overlay.meme_names) > 4:
                overlay.current_meme = 4
                print(f"Switched to: {overlay.meme_names[4]}")
            elif key == ord(' '):
                overlay_enabled = not overlay_enabled
                status = "ON" if overlay_enabled else "OFF"
                print(f"Overlay: {status}")
            elif key == ord('s'):
                filename = f'screenshot_{frame_count}.png'
                cv2.imwrite(filename, frame)
                print(f"Screenshot saved: {filename}")
    
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Done!")

if __name__ == '__main__':
    main()
