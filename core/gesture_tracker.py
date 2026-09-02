import cv2
import numpy as np
import mediapipe as mp

class GestureTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7, 
            max_num_hands=2  # Track BOTH hands
        )

    def get_portal_box_and_landmarks(self, rgb_frame):
        h, w, _ = rgb_frame.shape
        results = self.hands.process(rgb_frame)
        
        box = None
        hand_landmarks_list = []

        if results.multi_hand_landmarks:
            hand_landmarks_list = results.multi_hand_landmarks
            
            # When BOTH hands are visible, use their index fingertips (Landmark 8) to form the Portal Box
            if len(hand_landmarks_list) == 2:
                hand1_index = hand_landmarks_list[0].landmark[8]
                hand2_index = hand_landmarks_list[1].landmark[8]

                x1, y1 = int(hand1_index.x * w), int(hand1_index.y * h)
                x2, y2 = int(hand2_index.x * w), int(hand2_index.y * h)

                box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        return box, hand_landmarks_list

    def draw_landmarks_and_box(self, frame, box, hand_landmarks_list):
        # 1. Draw the yellow Portal Box if active
        if box is not None:
            bx1, by1, bx2, by2 = box
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 255), 2)
            cv2.putText(frame, "ALGEASY PORTAL", (bx1, max(by1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # 2. Draw white Hand Skeleton ON TOP so hands stay visible
        for hand_landmarks in hand_landmarks_list:
            self.mp_draw.draw_landmarks(
                frame, 
                hand_landmarks, 
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=3),
                self.mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2)
            )