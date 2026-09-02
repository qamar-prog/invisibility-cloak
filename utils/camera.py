import cv2
import time
import numpy as np

class CameraHandler:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        time.sleep(2) # Allow sensor to adjust
        self.bg_float = None # Store the 32-bit background

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False, None
        return True, cv2.flip(frame, 1)

    def capture_background(self):
        print("Step OUT of the frame and press 'c' to capture the clean background.")
        
        while True:
            ret, frame = self.read_frame()
            if not ret: continue
            
            display_frame = frame.copy()
            cv2.putText(display_frame, "Step out and press 'C'", (10, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.imshow("Invisibility Cloak", display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                # Store the background as a 32-bit float for running average
                self.bg_float = np.float32(frame)
                print("Background captured!")
                break
            elif key == ord('q'):
                break
                
        return self.get_background()

    def update_background(self, current_frame, human_mask, learning_rate=0.01):
        """Updates ONLY the background pixels to adjust to new lighting."""
        if self.bg_float is None:
            return
            
        # Invert mask: Human becomes 0, Background becomes 255
        bg_mask = np.where(human_mask > 0.5, 0, 255).astype(np.uint8)
        
        # Slowly blend new frame into background only where bg_mask is 255
        cv2.accumulateWeighted(current_frame, self.bg_float, learning_rate, mask=bg_mask)

    def get_background(self):
        """Returns the standard 8-bit background for blending."""
        if self.bg_float is None:
            return None
        return cv2.convertScaleAbs(self.bg_float)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()