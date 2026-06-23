# YOLO 웹캠 객체 감지 프로그램 ------------------------
import cv2
import time
import os
from ultralytics import YOLO

# 설정값
MODEL_PATH = "yolo11n.pt"
WINDOW_NAME = "YOLO Webcam Detection"
SAVE_DIR = "saved"

# 감지할 객체
TARGET_LABELS = {
    "cell phone", "laptop", "keyboard", "mouse", "cup", "book", "backpack",
    "handbag", "keyboard", "umbrella", "toothbrush"
}

CONFIDENCE_THRESHOLD = 0.55   # 최소 신뢰도
SAVE_COOLDOWN = 5  # 저장 간격(초)
FRAME_DELAY = 0.03  # 프레임 처리 간격

# 웹캠 해상도
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# 저장 폴더 준비
os.makedirs(SAVE_DIR, exist_ok=True)

print("YOLO 모델 로드 중...")
model = YOLO(MODEL_PATH)
print("모델 로드 완료")

# 웹캠 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
print("웹캠 연결 성공")

# 창 생성
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, 900, 700)

# 객체 저장 시간 기록
last_saved = {}

# 색상 정의
BOX_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)

# FPS 계산용
prev_time = time.time()

# 메인 루프
while True:
    success, frame = cap.read()

    if not success:
        print("프레임 읽기 실패")
        break

    # 좌우 반전
    frame = cv2.flip(frame, 1)

    # YOLO 추론
    results = model(
        frame,
        verbose=False
    )

    # 객체 처리
    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            confidence = float(box.conf[0])
            # 신뢰도 필터
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            # 원하는 객체만
            if label not in TARGET_LABELS:
                continue

            # 좌표
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # 박스 그리기
            cv2.rectangle(
                frame, (x1, y1), (x2, y2), BOX_COLOR, 2
            )

            text = f"{label} {confidence:.2f}"

            cv2.putText(
                frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, TEXT_COLOR, 2
            )

            # 저장 처리
            current_time = time.time()
            last_time = last_saved.get(label, 0)

            if current_time - last_time > SAVE_COOLDOWN:
                filename = (
                    f"{label}_{int(current_time)}.jpg"
                )

                filepath = os.path.join(SAVE_DIR, filename)
                cv2.imwrite(filepath, frame)
                print(f"[저장 완료] {filepath}")
                last_saved[label] = current_time

    # FPS 계산
    current = time.time()
    fps = 1 / (current - prev_time)
    prev_time = current

    cv2.putText(
        frame, f"FPS: {fps:.1f}", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2
    )

    # 화면 출력
    cv2.imshow(WINDOW_NAME, frame)

    # 종료 키
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

    # CPU 사용량 감소
    time.sleep(FRAME_DELAY)

# 종료 처리
cap.release()
cv2.destroyAllWindows()
print("프로그램 종료")