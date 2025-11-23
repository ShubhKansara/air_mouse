"""
ui_config.py

Tkinter Calibration UI for Air Mouse.
Allows user to adjust:
 - sensitivity
 - acceleration
 - deadzone
 - click_threshold
 - freeze_delay
 - smoothing
 - use_kalman

Config is stored in config.json
"""

import json
import os
import tkinter as tk
from tkinter import ttk

CONFIG_FILE = "config.json"

# --------------------------
# Load / Save Config
# --------------------------

def load_user_config():
    if not os.path.exists(CONFIG_FILE):
        default = {
            "sensitivity": 3.0,
            "accel": 2.0,
            "deadzone": 0.03,
            "pinch_threshold": 0.04,
            "two_pinch_threshold": 0.03,
            "right_pinch_extra": 0.045,
            "click_threshold": 0.3,
            "freeze_delay": 0.05,
            "smooth": 0.6,
            "use_kalman": False
        }
        save_user_config(default)
        return default

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_user_config(cfg: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)


# --------------------------
# Tkinter UI
# --------------------------

def open_config_window():
    cfg = load_user_config()

    win = tk.Tk()
    win.title("Air Mouse Calibration")
    win.geometry("400x500")

    sliders = {}

    def add_slider(label, key, from_, to_, step=0.01):
        tk.Label(win, text=label).pack()
        var = tk.DoubleVar(value=cfg[key])
        slider = ttk.Scale(win, from_=from_, to=to_, orient="horizontal", variable=var)
        slider.pack(fill="x", padx=10, pady=5)
        sliders[key] = var

    # Add sliders
    add_slider("Sensitivity", "sensitivity", 0.1, 10.0)
    add_slider("Acceleration", "accel", 0.1, 5.0)
    add_slider("Deadzone", "deadzone", 0.0, 0.2)
    add_slider("Pinch Threshold", "pinch_threshold", 0.01, 0.1)
    add_slider("Two Pinch Threshold", "two_pinch_threshold", 0.01, 0.1)
    add_slider("Right Pinch Extra", "right_pinch_extra", 0.01, 0.1)
    add_slider("Click Threshold", "click_threshold", 0.1, 1.0)
    add_slider("Freeze Delay", "freeze_delay", 0.0, 0.3)
    add_slider("Smoothing", "smooth", 0.0, 1.0)

    # Kalman checkbox
    kalman_var = tk.BooleanVar(value=cfg.get("use_kalman", False))
    tk.Checkbutton(win, text="Enable Kalman Filter", variable=kalman_var).pack(pady=10)

    # Save button
    def save_and_close():
        new_cfg = {k: v.get() for k, v in sliders.items()}
        new_cfg["use_kalman"] = kalman_var.get()
        save_user_config(new_cfg)
        win.destroy()

    tk.Button(win, text="Save", command=save_and_close).pack(pady=20)

    win.mainloop()


if __name__ == "__main__":
    open_config_window()
