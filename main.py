import cv2
import pyautogui
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import os
import sys
from numba import njit

# --- PATH HANDLER FOR EXE ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- PHYSICS ENGINE ---
@njit(fastmath=True)
def calculate_physics(curr_x, curr_y, prev_raw_x, prev_raw_y, out_x, out_y, boost, thresh):
    dx = curr_x - prev_raw_x
    dy = curr_y - prev_raw_y
    dist = np.sqrt(dx*dx + dy*dy)
    if dist < 0.005: return out_x, out_y, False
    if dist > thresh:
        return out_x + (dx * boost), out_y + (dy * boost), True
    return out_x + dx * 1.1, out_y + dy * 1.1, False

use_inv = True

def power_preprocess(frame, sens_val):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    
    mode = cv2.THRESH_BINARY_INV if use_inv else cv2.THRESH_BINARY
    if sens_val <= 0:
        _, l_bin = cv2.threshold(l, 0, 255, mode + cv2.THRESH_OTSU)
    else:
        _, l_bin = cv2.threshold(l, sens_val, 255, mode)
        
    l_bin = cv2.GaussianBlur(l_bin, (5, 5), 0)
    return l_bin

# --- SETUP ---
MODEL_PATH = resource_path('hand_landmarker.task')

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

WIN_NAME = "NumbaCoreVision (NCV)"
cv2.namedWindow(WIN_NAME)
cv2.createTrackbar("Boost", WIN_NAME, 15, 50, lambda x: None)
cv2.createTrackbar("Box", WIN_NAME, 85, 100, lambda x: None)
cv2.createTrackbar("Sens", WIN_NAME, 0, 255, lambda x: None)

SCR_W, SCR_H = pyautogui.size()
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

modes = ["MOUSE", "SCROLL", "TURBO"]
current_mode_idx = 0
out_x, out_y = 0.5, 0.5
raw_px, raw_py = 0.5, 0.5
l_clicked = False
prev_time = 0
pose_start_time = 0
CHANGE_DELAY = 1.0

try:
    while cap.isOpened():
        success, raw_frame = cap.read()
        if not success: break
        raw_frame = cv2.flip(raw_frame, 1)
        h, w, _ = raw_frame.shape

        # SAFE TRACKBAR READING
        try:
            current_sens = cv2.getTrackbarPos("Sens", WIN_NAME)
            boost_val = cv2.getTrackbarPos("Boost", WIN_NAME)
            b_val = cv2.getTrackbarPos("Box", WIN_NAME) / 100.0
        except:
            break # Exit loop if window is closed

        active_sens = 0 if pose_start_time > 0 else current_sens
        mask = power_preprocess(raw_frame, active_sens)
        processed_frame = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # PIP VIEW
        small_res = (w//5, h//5)
        pip = cv2.resize(processed_frame, small_res)
        raw_frame[10:10+small_res[1], 10:10+small_res[0]] = pip
        cv2.rectangle(raw_frame, (10,10), (10+small_res[0], 10+small_res[1]), (255, 255, 0), 1)

        mw, mh = int(w * (1 - b_val) / 2), int(h * (1 - b_val) / 2)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=processed_frame)
        
        try:
            result = detector.detect_for_video(mp_image, int(time.time() * 1000))
        except: continue

        if result.hand_landmarks:
            hand = result.hand_landmarks[0]
            wrist = hand[0]
            t_t, i_t, m_t, r_t, p_t = hand[4], hand[8], hand[12], hand[16], hand[20]
            i_m, m_m, r_m, p_m = hand[5], hand[9], hand[13], hand[17]
            
            pinky_up = p_t.y < p_m.y - 0.02
            others_down = (i_t.y > i_m.y) and (m_t.y > m_m.y) and (r_t.y > r_m.y)
            
            if pinky_up and others_down:
                if pose_start_time == 0: pose_start_time = time.time()
                elapsed = time.time() - pose_start_time
                cv2.rectangle(raw_frame, (w//2-60, 20), (w//2+60, 35), (40, 40, 40), -1)
                cv2.rectangle(raw_frame, (w//2-60, 20), (w//2-60+int(min(elapsed/CHANGE_DELAY, 1)*120), 35), (0, 255, 0), -1)
                if elapsed >= CHANGE_DELAY:
                    current_mode_idx = (current_mode_idx + 1) % len(modes)
                    pose_start_time = 0
                    time.sleep(0.2)
            else:
                pose_start_time = 0

            cx = np.clip((wrist.x * w - mw) / (w - 2 * mw), 0, 1)
            cy = np.clip((wrist.y * h - mh) / (h - 2 * mh), 0, 1)
            mode = modes[current_mode_idx]
            
            active_boost = float(boost_val) if mode == "TURBO" else 2.0
            new_x, new_y, _ = calculate_physics(cx, cy, raw_px, raw_py, out_x, out_y, active_boost, 0.04)
            out_x, out_y = np.clip(new_x, 0, 1), np.clip(new_y, 0, 1)
            raw_px, raw_py = cx, cy
            
            if mode != "SCROLL":
                pyautogui.moveTo(int(out_x * SCR_W), int(out_y * SCR_H))
                if np.sqrt((t_t.x - i_t.x)**2 + (t_t.y - i_t.y)**2) < 0.04:
                    if not l_clicked: pyautogui.mouseDown(); l_clicked = True
                    cv2.circle(raw_frame, (int(i_t.x*w), int(i_t.y*h)), 10, (0, 0, 255), -1)
                else:
                    if l_clicked: pyautogui.mouseUp(); l_clicked = False
            elif mode == "SCROLL":
                if t_t.y < i_m.y - 0.06: pyautogui.scroll(80)
                elif i_t.y < i_m.y - 0.05 and m_t.y < m_m.y - 0.05: pyautogui.scroll(-80)

            for lm in hand: cv2.circle(raw_frame, (int(lm.x*w), int(lm.y*h)), 2, (0, 255, 0), -1)
            cv2.circle(raw_frame, (int(wrist.x*w), int(wrist.y*h)), 12, (255, 0, 0), 3)

        cv2.rectangle(raw_frame, (mw, mh), (w-mw, h-mh), (0, 255, 255), 1)
        cv2.putText(raw_frame, f"MODE: {modes[current_mode_idx]}", (20, h-20), 1, 2, (255, 255, 0), 2)
        
        cv2.imshow(WIN_NAME, raw_frame)
        if cv2.waitKey(1) & 0xFF == 27: break
        if cv2.waitKey(1) & 0xFF == ord('i'): use_inv = not use_inv

finally:
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0) # Clean exit for EXE
