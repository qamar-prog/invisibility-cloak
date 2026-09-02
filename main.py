import cv2
from utils.camera import CameraHandler
from core.segmenter import HumanSegmenter
from core.gesture_tracker import GestureTracker
from core.blender import apply_invisibility

def main():
    cam = CameraHandler()
    segmenter = HumanSegmenter()
    tracker = GestureTracker()

    background = cam.capture_background()
    if background is None:
        cam.release()
        return

    while True:
        ret, frame = cam.read_frame()
        if not ret: break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 1. Get body segmentation mask
        mask = segmenter.get_mask(rgb_frame)

        # 2. Get 2-hand portal box coordinates & hand landmarks
        box, hand_landmarks_list = tracker.get_portal_box_and_landmarks(rgb_frame)

        # 3. Apply invisibility ONLY inside the 2-hand box
        if box is not None:
            output_frame = apply_invisibility(frame, background, mask, box=box)
        else:
            output_frame = frame

        # 4. Draw Portal rectangle & Hand Skeletons ON TOP of the frame
        tracker.draw_landmarks_and_box(output_frame, box, hand_landmarks_list)

        cv2.imshow("Invisibility Cloak - Portal Mode", output_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()

if __name__ == "__main__":
    main()