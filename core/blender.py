import cv2
import numpy as np

def apply_invisibility(live_frame, background, mask, box=None):
    # Feather the mask edges
    blurred_mask = cv2.GaussianBlur(mask, (15, 15), 0)
    
    # Base condition: human pixels
    condition = np.stack((blurred_mask,) * 3, axis=-1) > 0.5
    
    # If portal box exists, restrict invisibility strictly INSIDE the box coordinates
    if box is not None:
        bx1, by1, bx2, by2 = box
        roi_condition = np.zeros_like(condition, dtype=bool)
        roi_condition[by1:by2, bx1:bx2, :] = True
        
        # Combine: pixel must be human AND inside the portal box
        condition = np.logical_and(condition, roi_condition)

    # Replace pixels inside the box with the static background
    return np.where(condition, background, live_frame)