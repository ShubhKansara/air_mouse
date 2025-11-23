"""
tracker.py

Handles loading MediaPipe Hand Landmark model and providing a reusable tracker instance.
main.py calls create_hand_tracker() to get the object.

MediaPipe Tasks format:
 HandLandmarker.create_from_options(options)
 RunningMode.VIDEO for per-frame tracking
"""

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def create_hand_tracker(model_path: str):
    """Create MediaPipe HandLandmarker.

    Args:
        model_path: path to .task file
    Returns:
        HandLandmarker object
    """
    base = python.BaseOptions(model_asset_path=model_path)

    opts = vision.HandLandmarkerOptions(
        base_options=base,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1
    )

    return vision.HandLandmarker.create_from_options(opts)
