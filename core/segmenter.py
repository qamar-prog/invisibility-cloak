import mediapipe as mp

class HumanSegmenter:
    def __init__(self, model_selection=1):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmenter = self.mp_selfie_segmentation.SelfieSegmentation(
            model_selection=model_selection)

    def get_mask(self, rgb_frame):
        results = self.segmenter.process(rgb_frame)
        return results.segmentation_mask