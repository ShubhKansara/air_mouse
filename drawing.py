"""
drawing.py

Contains functions for drawing hand skeleton and landmarks.
Used by main.py to visualize tracking results.
"""

import cv2

# MediaPipe hand landmark connections
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]


def draw_skeleton(frame, lm):
    """Draw hand skeleton and keypoints.

    Args:
        frame (ndarray): Video frame (BGR)
        lm (list of landmarks): MediaPipe hand landmarks
    """
    h, w, _ = frame.shape

    # Draw connections (bones)
    for s, e in HAND_CONNECTIONS:
        x1, y1 = int(lm[s].x * w), int(lm[s].y * h)
        x2, y2 = int(lm[e].x * w), int(lm[e].y * h)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw keypoints
    for i, p in enumerate(lm):
        cx, cy = int(p.x * w), int(p.y * h)
        # Highlight fingertips
        col = (0, 200, 255) if i in (4, 8, 12, 16, 20) else (0, 255, 255)
        cv2.circle(frame, (cx, cy), 6, col, -1)
