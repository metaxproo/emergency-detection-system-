import cv2  # type: ignore
import time
import requests
import geocoder
from ultralytics import YOLO

# ================= MODELS =================
fire_model = YOLO("models/fire.pt")
weapon_model = YOLO("models/weapon.pt")
fall_model = YOLO("models/fall.pt")

# ================= CAMERA =================
cap = cv2.VideoCapture("testall1.mp4")

# ================= ALERT CONTROL =================
last_fire_alert = 0
last_weapon_alert = 0
last_fall_alert = 0

# ================= STABILITY COUNTERS =================
fall_counter = 0
weapon_counter = 0
fire_counter = 0
# ================= THRESHOLDS =================
FALL_THRESHOLD_FRAMES = 15
WEAPON_THRESHOLD_FRAMES = 8
FIRE_THRESHOLD_FRAMES = 10

# ================= SERVER =================
SERVER_URL = "https://mutular-julianna-coronally.ngrok-free.dev/new-incident"

# ================= LOCATION =================
def get_location():
    return [30.0444, 31.2357]

# ================= ALERT FUNCTION =================

def send_alert(alert_type, confidence):

    lat, lng = get_location()

    payload = {
        "id": time.time(),                 # unique alert id
        "type": alert_type,                # fire / weapon / fall
        "lat": lat,
        "lng": lng,
        "source": "AI_Camera_01",          # camera name
        "confidence": float(confidence)
    }

    try:
        response = requests.post(
            SERVER_URL,
            json=payload,
            timeout=5
        )

        print(f"🚨 ALERT SENT: {alert_type}")
        print("Server Response:", response.status_code)

    except Exception as e:
        print("❌ Alert failed")
        print(e)

# ================= MAIN LOOP =================
while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ================= RESIZE =================
    frame = cv2.resize(frame, (640, 480))

    # ======================================================
    # ================= FIRE DETECTION =====================
    # ======================================================

    fire_results = fire_model(
        frame,
        imgsz=640,
        verbose=False
    )

    for r in fire_results:

        for box in r.boxes:

            conf = float(box.conf[0])

            if conf > 0.5:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"FIRE {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

                cv2.putText(
                    frame,
                    "FIRE ALERT!",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                # send alert every 10 sec
                if time.time() - last_fire_alert > 10:

                    send_alert("fire", conf)

                    last_fire_alert = time.time()

    # ======================================================
    # ================= WEAPON DETECTION ===================
    # ======================================================

    weapon_detected = False

    weapon_results = weapon_model(
        frame,
        imgsz=640,
        verbose=False
    )

    for r in weapon_results:

        for box in r.boxes:

            conf = float(box.conf[0])

            # balanced confidence
            if conf > 0.55:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                width = x2 - x1
                height = y2 - y1

                # ignore very small detections
                if width < 40 or height < 40:
                    continue

                weapon_detected = True

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 105, 180),
                    2
                )

                cv2.putText(
                    frame,
                    f"WEAPON {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 105, 180),
                    2
                )

    # ================= WEAPON STABILITY =================

    if weapon_detected:
        weapon_counter += 1

    else:
        weapon_counter = 0

    if weapon_counter > WEAPON_THRESHOLD_FRAMES:

        cv2.putText(
            frame,
            "WEAPON ALERT!",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 105, 180),
            3
        )

        if time.time() - last_weapon_alert > 10:

            send_alert("weapon", 0.9)

            last_weapon_alert = time.time()

        weapon_counter = 0

    # ======================================================
    # ================= FALL DETECTION =====================
    # ======================================================

    fall_results = fall_model(
        frame,
        imgsz=640,
        verbose=False
    )

    fall_detected = False

    frame_height = frame.shape[0]

    for r in fall_results:

        for box in r.boxes:

            conf = float(box.conf[0])

            if conf > 0.55:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                width = x2 - x1
                height = y2 - y1

                if height == 0:
                    continue

                ratio = width / height

                # horizontal body check
                is_horizontal = ratio > 1.4

                # body lower in frame
                near_ground = y2 > frame_height * 0.65

                if is_horizontal and near_ground:

                    fall_detected = True

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (255, 0, 0),
                        3
                    )

                    cv2.putText(
                        frame,
                        f"FALL {conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 0, 0),
                        2
                    )

    # ================= FALL STABILITY =================

    if fall_detected:
        fall_counter += 1

    else:
        fall_counter = 0

    if fall_counter > FALL_THRESHOLD_FRAMES:

        cv2.putText(
            frame,
            "FALL ALERT!",
            (50, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            3
        )

        if time.time() - last_fall_alert > 10:

            send_alert("fall", 0.9)

            last_fall_alert = time.time()

        fall_counter = 0

    # ======================================================
    # ================= DISPLAY ============================
    # ======================================================

    cv2.imshow("Smart Emergency Detection System", frame)

    # press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================= RELEASE =================
cap.release()
cv2.destroyAllWindows()
