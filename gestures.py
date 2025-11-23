"""
gestures.py — Angle-based detection + temporal smoothing/hysteresis

Returns stable gestures:
- "move"       -> index extended
- "left_click" -> thumb-index pinch
- "right_click"-> thumb-middle pinch
- "palm"       -> 3+ fingers extended
- "none"       -> idle

Use config to tune thresholds if needed.
"""

import math
from collections import deque

class Gesture:
    def __init__(self, config: dict):
        # thresholds (tweakable)
        self.pinch_threshold = float(config.get("pinch_threshold", 0.06))       # thumb-tip distance
        self.middle_pinch_threshold = float(config.get("right_pinch_extra", 0.07))
        self.extend_angle = float(config.get("extend_angle", 50.0))            # degrees
        # how many frames must a detection hold to flip state
        self.hysteresis_frames = int(config.get("hysteresis_frames", 3))

        # frame buffers / counters for smoothing
        self.buf_move = 0
        self.buf_left = 0
        self.buf_right = 0
        self.buf_palm = 0
        self.buf_none = 0

        # last stable gesture
        self.last_gesture = "none"

    # -------------------------
    # math helpers
    # -------------------------
    @staticmethod
    def dist(a, b):
        return math.hypot(a.x - b.x, a.y - b.y)

    @staticmethod
    def angle(a, b, c):
        bax = a.x - b.x
        bay = a.y - b.y
        bcx = c.x - b.x
        bcy = c.y - b.y
        dot = bax * bcx + bay * bcy
        mag1 = math.hypot(bax, bay)
        mag2 = math.hypot(bcx, bcy)
        if mag1 * mag2 == 0:
            return 180.0
        cos_val = max(-1.0, min(1.0, dot / (mag1 * mag2)))
        return math.degrees(math.acos(cos_val))

    # -------------------------
    # angle-based extension
    # -------------------------
    def is_extended(self, lm, base, mid, tip):
        ang = self.angle(lm[base], lm[mid], lm[tip])
        return ang < self.extend_angle

    def is_index_extended(self, lm):
        return self.is_extended(lm, 5, 6, 8)

    def is_middle_extended(self, lm):
        return self.is_extended(lm, 9, 10, 12)

    def is_ring_extended(self, lm):
        return self.is_extended(lm, 13, 14, 16)

    def is_pinky_extended(self, lm):
        return self.is_extended(lm, 17, 18, 20)

    def is_palm_open(self, lm):
        ext = 0
        if self.is_index_extended(lm): ext += 1
        if self.is_middle_extended(lm): ext += 1
        if self.is_ring_extended(lm): ext += 1
        if self.is_pinky_extended(lm): ext += 1
        return ext >= 3

    def pinch_left(self, lm):
        return self.dist(lm[4], lm[8]) < self.pinch_threshold

    def pinch_right(self, lm):
        return self.dist(lm[4], lm[12]) < self.middle_pinch_threshold

    # -------------------------
    # debugging metrics
    # -------------------------
    def metrics(self, lm):
        # returns a dict useful for overlay/debugging
        return {
            "angle_index": round(self.angle(lm[5], lm[6], lm[8]), 1),
            "angle_middle": round(self.angle(lm[9], lm[10], lm[12]), 1),
            "pinch_thumb_index": round(self.dist(lm[4], lm[8]), 3),
            "pinch_thumb_middle": round(self.dist(lm[4], lm[12]), 3),
            "index_ext": self.is_index_extended(lm),
            "middle_ext": self.is_middle_extended(lm),
            "palm_open": self.is_palm_open(lm)
        }

    # -------------------------
    # main classify with hysteresis
    # -------------------------
    def classify(self, lm):
        # compute booleans
        palm = self.is_palm_open(lm)
        left_pinch = self.pinch_left(lm)
        right_pinch = self.pinch_right(lm)
        index_ext = self.is_index_extended(lm)

        # increment counters
        if palm:
            self.buf_palm += 1
        else:
            self.buf_palm = 0

        if left_pinch:
            self.buf_left += 1
        else:
            self.buf_left = 0

        if right_pinch:
            self.buf_right += 1
        else:
            self.buf_right = 0

        if index_ext and not (left_pinch or right_pinch or palm):
            self.buf_move += 1
        else:
            self.buf_move = 0

        # none = when nothing else holds
        if not (palm or left_pinch or right_pinch or index_ext):
            self.buf_none += 1
        else:
            self.buf_none = 0

        # decide in priority order
        if self.buf_palm >= self.hysteresis_frames:
            g = "palm"
        elif self.buf_left >= self.hysteresis_frames:
            g = "left_click"
        elif self.buf_right >= self.hysteresis_frames:
            g = "right_click"
        elif self.buf_move >= self.hysteresis_frames:
            g = "move"
        elif self.buf_none >= self.hysteresis_frames:
            g = "none"
        else:
            # not stable yet — return last stable gesture (prevents flicker)
            g = self.last_gesture

        # update last stable if changed
        if g != self.last_gesture:
            self.last_gesture = g

        return g
