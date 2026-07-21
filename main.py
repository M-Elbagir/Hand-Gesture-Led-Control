import cv2
import mediapipe as mp
import serial

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def count_fingers(hand_landmarks, handedness):
    lm = hand_landmarks.landmark
    count = 0

    def distance(a, b):
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

    wrist = lm[0]
    thumb_tip = lm[4]
    thumb_ip = lm[3]

    if handedness == "Right":
        thumb_open = distance(thumb_tip, wrist) > distance(thumb_ip, wrist) + 0.02 and thumb_tip.x < thumb_ip.x
    else:
        thumb_open = distance(thumb_tip, wrist) > distance(thumb_ip, wrist) + 0.02 and thumb_tip.x > thumb_ip.x

    if thumb_open:
        count += 1

    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        if distance(lm[tip], wrist) > distance(lm[pip], wrist) + 0.05:
            count += 1

    return count


try:
    arduino = serial.Serial('COM4', 115200, timeout=1)
except Exception as e:
    print(f"Unable to connect to Arduino on COM4: {e}")
    arduino = None

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Unable to open camera")
    raise SystemExit(1)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            handedness = "Right"
            if results.multi_handedness and results.multi_handedness[0].classification:
                handedness = results.multi_handedness[0].classification[0].label

            finger_count = count_fingers(hand_landmarks, handedness)
            if arduino is not None:
                arduino.write(f"{finger_count}\n".encode())
            cv2.putText(
                frame,
                f"Fingers: {finger_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                2,
                cv2.LINE_AA,
            )

        cv2.imshow("Fingers Counter", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

if arduino is not None:
    arduino.close()

cap.release()
cv2.destroyAllWindows()
