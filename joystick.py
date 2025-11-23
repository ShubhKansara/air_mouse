"""
joystick.py — Enhanced Joystick System

Includes ALL requested improvements:
✅ Downward movement fix
✅ Better camera → joystick mapping
✅ Auto-center drift correction
✅ Cubic response curve (gaming feel)
✅ Exponential smoothing
✅ Optional Kalman filter
✅ Multi-monitor boundary detection
"""

from screeninfo import get_monitors
from pynput.mouse import Controller, Button
import math


class JoystickMouse:
    def __init__(self, config: dict):
        # Load config
        self.sensitivity = float(config.get("sensitivity", 3.0))
        self.accel = float(config.get("accel", 2.0))
        self.deadzone = float(config.get("deadzone", 0.03))
        self.smooth = float(config.get("smooth", 0.6))
        self.use_kalman = bool(config.get("use_kalman", False))

        # Cursor control
        self.mouse = Controller()
        self.center_x = None
        self.center_y = None
        self.frozen = False

        # Smoothing
        self.prev_vx = 0.0
        self.prev_vy = 0.0

        # Auto-center drift correction
        self.center_stability = 0.995

        # Kalman filter state
        self.kalman_px = 0.0
        self.kalman_py = 0.0
        self.kalman_P = 1.0    # estimated covariance
        self.kalman_Q = 0.01   # process noise
        self.kalman_R = 0.3    # measurement noise

        # Monitor resolution
        mon = get_monitors()[0]
        self.sw = mon.width
        self.sh = mon.height

    # ------------------------------------------------------------
    # Utility functions
    # ------------------------------------------------------------
    def update_center(self, x, y):
        """Set joystick center to current hand position."""
        self.center_x = x
        self.center_y = y

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    # ------------------------------------------------------------
    # Kalman filter
    # ------------------------------------------------------------
    def kalman_filter(self, vx, vy):
        P_pred = self.kalman_P + self.kalman_Q
        K = P_pred / (P_pred + self.kalman_R)

        self.kalman_px += K * (vx - self.kalman_px)
        self.kalman_py += K * (vy - self.kalman_py)
        self.kalman_P = (1 - K) * P_pred

        return self.kalman_px, self.kalman_py

    # ------------------------------------------------------------
    # Main movement logic
    # ------------------------------------------------------------
    def move(self, x, y):
        if self.frozen:
            return

        # Detect active monitor
        try:
            mx, my = self.mouse.position
            for m in get_monitors():
                if m.x <= mx < m.x + m.width and m.y <= my < m.y + m.height:
                    self.sw, self.sh = m.width, m.height
                    break
        except:
            pass

        # Initialize center
        if self.center_x is None:
            self.update_center(x, y)
            return

        # ------------------------------------------------------------
        # Auto-center drift correction (slow center adaptation)
        # ------------------------------------------------------------
        self.center_x = self.center_x * self.center_stability + x * (1 - self.center_stability)
        self.center_y = self.center_y * self.center_stability + y * (1 - self.center_stability)

        # ------------------------------------------------------------
        # Compute joystick delta
        # ------------------------------------------------------------
        dx = x - self.center_x
        dy = -(y - self.center_y)   # invert vertical axis (fix downward issue)

        # Apply deadzone
        if abs(dx) < self.deadzone:
            dx = 0.0
        if abs(dy) < self.deadzone:
            dy = 0.0

        # ------------------------------------------------------------
        # Apply cubic response curve (gaming feel)
        # ------------------------------------------------------------
        dx_c = dx ** 3
        dy_c = dy ** 3

        # Raw velocity
        raw_vx = dx_c * self.sensitivity * (abs(dx) * self.accel + 1)
        raw_vy = dy_c * self.sensitivity * (abs(dy) * self.accel + 1)

        # ------------------------------------------------------------
        # Apply exponential smoothing
        # ------------------------------------------------------------
        vx = self.prev_vx * self.smooth + raw_vx * (1 - self.smooth)
        vy = self.prev_vy * self.smooth + raw_vy * (1 - self.smooth)

        self.prev_vx = vx
        self.prev_vy = vy

        # ------------------------------------------------------------
        # Optional Kalman filter
        # ------------------------------------------------------------
        if self.use_kalman:
            vx, vy = self.kalman_filter(vx, vy)

        # ------------------------------------------------------------
        # Apply movement to cursor
        # ------------------------------------------------------------
        cx, cy = self.mouse.position
        new_x = cx + vx * 40
        new_y = cy + vy * 40

        # Clamp to monitor boundaries
        new_x = max(0, min(self.sw - 1, new_x))
        new_y = max(0, min(self.sh - 1, new_y))

        try:
            self.mouse.position = (int(new_x), int(new_y))
        except:
            pass

    # ------------------------------------------------------------
    # Click events
    # ------------------------------------------------------------
    def left_click(self):
        try:
            self.mouse.click(Button.left)
        except:
            pass

    def right_click(self):
        try:
            self.mouse.click(Button.right)
        except:
            pass
