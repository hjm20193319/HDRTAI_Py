from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# 테스트용 이미지 경로
image_path = "my.jpg"

# YOLO 모델 로드
det_model = YOLO("yolov8n.pt")           # detection 전용
seg_model = YOLO("yolov8n-seg.pt")   # segmentation 전용

img = cv2.imread(image_path)
assert img is not None, "이미지 로드 실패!"

# 1) Object Detection
det_results = det_model(img)[0]
det_img = det_results.plot()

# 2) Image Segmentation
seg_results = seg_model(img)[0]
seg_img = seg_results.plot()

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.imshow(cv2.cvtColor(det_img, cv2.COLOR_BGR2RGB))
plt.title("Object Detection (Bounding Boxes)")
plt.axis("off")
plt.subplot(1,2,2)
plt.imshow(cv2.cvtColor(seg_img, cv2.COLOR_BGR2RGB))
plt.title("Image Segmentation (Pixel Masks)")
plt.axis("off")

plt.tight_layout()
plt.show()