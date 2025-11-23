# 🖐️ AI Air-Mouse (Hand Tracking + Gesture Control)

A Python-based virtual mouse that uses **MediaPipe hand tracking**, **gesture recognition**,  
and a **joystick-style cursor controller** to replace your physical mouse.

Control your computer using:
- Index finger → move cursor  
- Thumb + index pinch → left click  
- Thumb + middle pinch → right click  
- Open palm → freeze cursor  

Built using:
- MediaPipe Tasks (Hand Landmarker)
- OpenCV
- Python
- Pynput (mouse control)
- Tkinter UI for calibration

---

## 🚀 Features

### 🎯 Cursor Control (Joystick Mode)
- Smooth & natural movement  
- Deadzone control  
- Sensitivity curves  
- Acceleration curve  
- Kalman-filter–ready architecture  

### ✋ Robust Gesture Detection
Uses **angle-based finger analysis + hysteresis** for stability.

Gestures supported:
- `move` — index finger extended  
- `left_click` — thumb + index pinch  
- `right_click` — thumb + middle pinch  
- `palm` — freeze cursor  
- `none` — idle  

### 🛠 Calibration UI (Tkinter)
Change parameters LIVE:
- Sensitivity  
- Acceleration  
- Deadzone  
- Pinch threshold  
- Hysteresis frames  
- Freeze delay  

### 🖥 Multi-Camera + GPU/CPU Switch
- Press `c` → cycle cameras  
- Press `g` → toggle simulated GPU mode  

### 🧪 Debug Overlay
Shows:
- Gesture name  
- FPS  
- Finger angles  
- Pinch distances  
- Index-extended state  
- Palm-open state  

Perfect for debugging and training gestures.

---

## 📦 Installation

### 1) Create a Virtual Environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

### 2) Install Requirements

```bash
pip install -r requirements.txt
```

### 3) Download MediaPipe Hand Model
Place the MediaPipe model file here:

```
./hand_landmarker.task
```

Download from:
https://developers.google.com/mediapipe/solutions/vision/hand_landmarker

---

## ▶️ Running the App

```bash
py main.py
```

---

## 🎮 Controls

| Action | How |
|--------|------|
| Move cursor | Extend index finger |
| Left click | Pinch thumb + index |
| Right click | Pinch thumb + middle |
| Freeze cursor | Open palm (3+ fingers extended) |
| Camera switch | Press `c` |
| GPU/CPU toggle | Press `g` |
| Exit | Press `ESC` |

---

## 📁 Project Structure

```
air_mouse/
│
├── main.py
├── joystick.py
├── gestures.py
├── config.py
├── ui.py             # calibration window
├── hand_landmarker.task
│
├── requirements.txt
└── README.md
```

---

## 🔧 Configuration

All adjustable parameters are stored in:

```
config.json
```

Example:

```json
{
  "sensitivity": 3.0,
  "acceleration": 2.0,
  "deadzone": 0.03,
  "pinch_threshold": 0.055,
  "right_pinch_extra": 0.065,
  "extend_angle": 50.0,
  "hysteresis_frames": 3,
  "freeze_delay": 0.3
}
```

---

## 🧠 How Gesture Detection Works

### 1. Finger Extension = Angle < 50°
Finger is extended if:

```
angle(base → mid → tip) < extend_angle
```

This avoids false detection when fingers are bent.

### 2. Pinch Detection = Thumb distance < threshold

### 3. Hysteresis = Stable gesture over N frames
Prevents flickering between states.

---

## 🛡 Troubleshooting

### Finger not recognized?
Increase:
```
extend_angle: 55–65
```

### Click triggers too easily?
Increase:
```
pinch_threshold
right_pinch_extra
hysteresis_frames
```

### Cursor moves too fast/slow?
Adjust in UI or config:
```
sensitivity
acceleration
```

---

## 📜 License
MIT License — free to modify and share.

---

## ⭐ Want More Features?
Available extensions:
- Drag gesture (hold pinch)
- Scroll gesture
- Zoom gesture
- Two-hand mode
- AI-based gesture classifier

Just ask: **“add scroll gesture”** or **“add drag gesture”**.

