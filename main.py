# main.py - Modular Air Mouse Project

from joystick import JoystickMouse
from gestures import Gesture
from drawing import draw_skeleton
from tracker import create_hand_tracker
from ui_config import load_user_config

import cv2
import time
import mediapipe as mp

CONFIG = load_user_config()
MODEL_PATH = "hand_landmarker.task"
CAM_WIDTH = 1280
CAM_HEIGHT = 720

class AirMouse:
    def __init__(self):
        self.cam_id = 0
        self.use_gpu = False
        self.cap = self.open_cam(self.cam_id)
        self.tracker = create_hand_tracker(MODEL_PATH)
        self.mouse = JoystickMouse(CONFIG)
        self.gesture = Gesture(CONFIG)
        self.frame_i = 0
        self.last_click = 0
        self.current_gesture = "none"

    def open_cam(self, i):
        cap = cv2.VideoCapture(i)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        return cap

    def process(self, frame):
        self.frame_i += 1
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        res = self.tracker.detect_for_video(mp_img, self.frame_i)

        # --- Proper hand detection ---
        if res.hand_landmarks and len(res.hand_landmarks) > 0:
            lm = res.hand_landmarks[0]
            draw_skeleton(frame, lm)

            action = self.gesture.classify(lm)
            self.current_gesture = action

            # --- Display gesture text ---
            cv2.putText(frame, f"Gesture: {action}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            # --- New Gesture System ---
            if action == "palm":
                self.mouse.freeze()

            elif action == "left_click":
                self.mouse.freeze()
                now = time.time()
                if now - self.last_click > CONFIG.get("click_threshold", 0.3):
                    self.mouse.left_click()
                    self.last_click = now

            elif action == "right_click":
                self.mouse.freeze()
                now = time.time()
                if now - self.last_click > CONFIG.get("click_threshold", 0.3):
                    self.mouse.right_click()
                    self.last_click = now

            elif action == "move":
                self.mouse.unfreeze()
                x, y = lm[8].x, lm[8].y
                self.mouse.move(x, y)

            else:
                self.mouse.unfreeze()
        else:
            self.mouse.unfreeze()
            self.current_gesture = "none"

        return frame

    def run(self):
        prev = 0
        print("Air Mouse (Modular) Running… ESC to exit")

        while True:
            ok, frame = self.cap.read()
            if not ok: break

            out = self.process(frame)

            now = time.time()
            fps = 1 / (now - prev) if prev else 0
            prev = now

            cv2.putText(out, f"FPS: {int(fps)}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(out, f"Cam: {self.cam_id} | c: switch | g: GPU(sim)", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow("Air Mouse", out)

            k = cv2.waitKey(1) & 0xFF
            if k == 27: break
            if k == ord('c'):
                self.cam_id = 1 - self.cam_id
                self.cap.release()
                self.cap = self.open_cam(self.cam_id)
            if k == ord('g'):
                self.use_gpu = not self.use_gpu
                self.tracker.close()
                self.tracker = create_hand_tracker(MODEL_PATH)

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    AirMouse().run()
