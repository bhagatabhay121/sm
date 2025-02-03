import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Cooldown variables
last_action_time = 0  # Stores last action timestamp
cooldown_period = 1.0  # Cooldown in seconds (1 second)

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Camera error!")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get hand landmark positions
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]

            # Get screen dimensions
            screen_width, screen_height = pyautogui.size()
            x, y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)

            current_time = time.time()

            # Gesture 1: Thumbs Up → Play/Pause (with cooldown)
            if thumb_tip.y < thumb_ip.y and (current_time - last_action_time > cooldown_period):
                print("Gesture detected: Thumbs Up (Play/Pause)")
                pyautogui.press("space")  # Toggle play/pause
                last_action_time = current_time

            # Gesture 2: Swipe Down (Scroll Down)
            elif index_tip.y > index_dip.y and index_tip.y > thumb_tip.y and (current_time - last_action_time > cooldown_period):
                print("Gesture detected: Swipe Down (Scroll Down)")
                pyautogui.scroll(-500)  # Scroll down
                last_action_time = current_time

            # Gesture 3: Swipe Up (Scroll Up)
            elif index_tip.y < index_dip.y and index_tip.y < thumb_tip.y and (current_time - last_action_time > cooldown_period):
                print("Gesture detected: Swipe Up (Scroll Up)")
                pyautogui.scroll(500)  # Scroll up
                last_action_time = current_time


    # Show the camera feed
    cv2.imshow("Hand Gesture Control", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
