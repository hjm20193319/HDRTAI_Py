# YOLO Tracking
# 이미지 내의 객체를 단순히 감지(Detection)하는 것을 넘어, 
# 비디오 스트림이나 연속된 프레임에서 동일한 객체에 고유 ID를 부여하고 추적하는 기술

# 1. 주요 특징:
# - 객체 감지(Detection) + 데이터 연관(Data Association)
# - 이전 프레임의 객체 위치와 현재 프레임의 감지 결과를 매칭
# - 객체가 일시적으로 가려지거나(Occlusion) 화면 밖으로 나갔다 들어와도 동일 ID 유지 시도
# - Detection → Tracking(같은 객체에 동일 id 부여)

# 2. YOLO에서 제공하는 주요 트래커(내부 알고리즘):
# - BoT-SORT: 기본 트래커, 높은 정확도와 견고함 제공
# - ByteTrack: 낮은 신뢰도의 감지 결과도 활용하여 추적 성능 향상

# 3. 주요 파라미터:
# - tracker: 사용할 트래커 설정 (botsort.yaml 또는 bytetrack.yaml)
# - persist: 비디오 프레임 간 추적 상태를 유지할지 여부 (True 권장)

# !pip install ultralytics opencv-python 

#######################################################################################
import cv2
from ultralytics import YOLO

model = YOLO('yolo11n.pt')

video_path = 'road_car.mp4'

cap = cv2.VideoCapture(video_path)  # 지정한 동영상 파일을 프레임 단위 읽기

if not cap.isOpened():
    print("동영상 파일을 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read() # ret : 읽기 성공 여부 , frame : 실제 이미지 데이터

    if not ret:
        break

    results = model.track(
        source = frame,     # 분석할 입력 이미지(현재 읽은 1장의 프레임)
        persist = True,     # 추적 정보 유지
        tracker='bytetrack.yaml',   # 객체 추적 알고리즘 중 하나 : 현재 프레임과 이전 프레임을 비교해 id 를 부여
        verbose = False,
        show = False
    )

    result = results[0]

    if result.boxes is not None and result.boxes.id is not None:
        boxes = result.boxes.xyxy.cpu().numpy()
        ids = result.boxes.id.cpu().numpy().astype(int)
        class_ids = result.boxes.cls.cpu().numpy().astype(int)  # ex) car = 2

        # 박스 좌표, 추적 id, 클래스 번호를 묶어 반복 처리
        for box, track_id, class_id in zip(boxes, ids, class_ids):
            x1, y1, x2, y2 = map(int, box)

            class_name = result.names[class_id]     # ex) 2 → car
            print(f'id : {track_id}, class : {class_name}, box : {box}')
    
    annotated_frame = result.plot()     # 욜로가 탐지한 이미지 자동으로 그리기 (각종 정보 표시)

    display_frame = cv2.resize(annotated_frame, (960, 540))

    cv2.imshow('YOLO Tracking', display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()