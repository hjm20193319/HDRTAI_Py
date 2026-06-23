# image segmentation
# !pip install ultralytics opencv-python



import cv2, numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import os

IMG_PATH = 'animal.png'
OUT_DIR = 'seg_output'
os.makedirs(OUT_DIR, exist_ok=True)



#######################################################################################
model = YOLO('yolo11n-seg.pt')

img_bgr = cv2.imread(IMG_PATH)
assert img_bgr is not None, f'이미지 없음 : {IMG_PATH}'
print(img_bgr.shape)    # (1024, 1536, 3)

H, W = img_bgr.shape[:2]
print(H, W)



#######################################################################################
res = model(img_bgr, verbose=False)[0]

annotated = res.plot()
cv2.imwrite(os.path.join(OUT_DIR, 'yolo10seg_result.jpg'), annotated)

# 화면 시각화
plt.imshow(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()



#######################################################################################
# 텐서 → numpy 배열로 변환
has_masks = (res.masks is not None)

if has_masks:
    masks_np = res.masks.data.cpu().numpy()
    boxes_np = res.boxes.xyxy.cpu().numpy().astype(int)
    conf_np = res.boxes.conf.cpu().numpy()
    class_np = res.boxes.cls.cpu().numpy().astype(int)

else:
    masks_np = boxes_np = conf_np = class_np = None



#######################################################################################
# 마스크 오버레이
overlay = img_bgr.copy()

# 인스턴스 Segmentation
if has_masks:
    for m in masks_np:
        # 모델이 출력한 마스크 크기를 원본 크기로 리사이즈
        m_bin = cv2.resize(m, (W, H), interpolation=cv2.INTER_NEAREST) > 0.5   # 0.5 이상일때만 객체로 간주 → 이진화
        # interpolation=cv2.INTER_NEAREST → 경계를 매끈하게 하는 옵션
        color_mask = np.zeros_like(overlay)     # 원본 이미지와 동일 크기의 빈 배열(검은색) 생성
        color_mask[m_bin] = (0, 255, 0)     # 객체 마스크 픽셀만 초록색으로 채움
        overlay = cv2.addWeighted(overlay, 1.0, color_mask, 0.4, 0)   # 이미지 합성(블렌딩)
        # overlay = cv2.addWeighted(이미지1, 가중치1, 이미지2, 가중치2, 추가 밝기)   # 이미지 합성(블렌딩)

cv2.imwrite(os.path.join(OUT_DIR, 'yolo10seg_overlay.jpg'), overlay)



#######################################################################################
# 객체 별 배경 제거 후 PNG로 개별 저장
crops_dir = os.path.join(OUT_DIR, 'seg_crops')
os.makedirs(crops_dir, exist_ok=True)

# YOLO 출력 마스크를 원본 이미지 크기에 맞춰 변환 후 여러 객체 마스크 처리
if has_masks and len(masks_np) > 0:
    masks_full = np.stack(
        [cv2.resize(m, (W, H), interpolation=cv2.INTER_NEAREST) > 0.5 for m in masks_np], 
        axis=0
    )

    # 탐지된 객체의 배경을 제거해 PNG로 저장
    for i, (m_full, box, cls_id, conf) in enumerate(zip(masks_full, boxes_np, class_np, conf_np)):
        x1, y1, x2, y2 = map(int, box)
        x1, y1 = max(0, x1), max(0, y1) # 좌상단 좌표가 이미지 밖으로 나가면 0으로 보정
        x2, y2 = min(W, x2), min(H, y2) # 우하단 좌표가 이미지 밖으로 나가면 W, H 로 보정
        if x2 <= x1 or y2 <= y1:
            continue

        # opencv는 순서가 [h, w, chanel] 이므로 이미지 자를 때 주의
        crop_bgr = img_bgr[y1:y2, x1:x2]    # 원본 이미지에서 박스 영역만 자르기
        crop_mask = (m_full[y1:y2, x1:x2] * 255).astype(np.uint8)   # 같은 영역 마스크를 0/255 (불투명)로 변환

        crop_bgra = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2BGRA)  # 알파 채널 추가
        crop_bgra[..., 3] = crop_mask   # 앞 차원은 그대로 두고, 4번째(알파) 채널에 마스크 적용 ⇨ 배경은 투명, 객체는 불투명

        # 클래스 이름 얻기(dog, cat, ...)
        name = model.names[int(cls_id)] if hasattr(model, 'names') else str(cls_id)
        cv2.imwrite(os.path.join(crops_dir, f'crop_{i:02d}_{name}_{conf:.2f}.png'), crop_bgra)



#######################################################################################
# Semantic(의미론적) Segmentation → 결과가 단순한 클래스가 아니라 마스크 이미지로 출력
sem_canvas = np.zeros((H, W, 3), dtype=np.uint8)  # 색상 지도
conf_map = np.zeros((H, W), dtype=np.float32)   # 신뢰도 기록

def class_color(c:int):
    return ((37 * c) % 256, (17 * c) % 256, (91 * c) % 256)     # BGR 형태의 고유 색상 반환

if has_masks and len(masks_np) > 0:
    for m_full, cls_id, conf in zip(masks_full, class_np, conf_np):
        color = class_color(int(cls_id))    # 클래스별 고정 색상 생성
        update = m_full & (conf > conf_map) # 이번 인스턴스의 conf가 더 큰 픽셀만 갱신
        sem_canvas[update] = color
        conf_map[update] = conf

cv2.imwrite(os.path.join(OUT_DIR, 'yolo10seg_sem.png'), sem_canvas)