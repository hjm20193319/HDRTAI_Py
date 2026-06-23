# YOLO 가 기본 제공하는 80가지 클래스 대신 
# 수족관에 살고 있는 동물 7가지 분류 모델로 Fine Tunning 하기
# Roboflow 사이트에서 aquarium dataset을 다운 받아 작업

# !wget -O Aquarium_Data.zip https://public.roboflow.com/ds/lh43HXLtGX?key=EwWAf7C2T7
# !pip install ultralytics opencv-python
# !pip install PyYAML


import zipfile

with zipfile.ZipFile('/content/Aquarium_Data.zip') as tfile:
    tfile.extractall('/content/Aquarium_Data')



#######################################################################################
# 커스텀 데이터에 맞는 yaml 만들기 - 환경 설정 파일
import yaml

data = {
    'train':'/content/Aquarium_Data/train/images/',
    'val':'/content/Aquarium_Data/valid/images/',
    'test':'/content/Aquarium_Data/test/images/',
    'names':['fish', 'jellyfish', 'penguin', 'puffin', 'shark', 'starfish', 'stingray'],
    'nc':7
}

# 데이터를 yaml 파일로 저장
with open('/content/Aquarium_Data/Aquarium_Data.yaml', 'w') as f:
    yaml.dump(data, f)

# yaml 파일 내용 확인 1
with open('/content/Aquarium_Data/Aquarium_Data.yaml', 'r') as f:
    aquarium_yaml = yaml.safe_load(f)
    display(aquarium_yaml)

# yaml 파일 내용 확인 2
# !cat /content/Aquarium_Data/Aquarium_Data.yaml




#######################################################################################
# YOLO 모델 호출
import ultralytics
ultralytics.checks()

from ultralytics import YOLO

model = YOLO('yolov11n.pt')
print(type(model.names), len(model.names))
print(model.names)
# → coco dataset에 맞는 YOLO 모델

# Fine Tunning (학습)
model.train(data='/content/Aquarium_Data/Aquarium_Data.yaml', epochs=100, imgsz=416, patience=30, batch=32)     # YOLO 계열은 416, 512, 640 크기 권장





#######################################################################################
# 전이 학습 및 Fine Tunning 후 모델 확인
print(type(model.names), len(model.names))
print(model.names)
# ⇨ 모델이 아쿠아리움 데이터에 맞게 바뀜


#######################################################################################
# test 이미지 데이터 생성 및 확인
from glob import  glob  # 폴더나 파일을 찾을 때 사용하는 라이브러리

test_image_list = glob('/content/Aquarium_Data/test/images/*')
print(len(test_image_list))
test_image_list.sort()  # 파일명 순 정렬

for i in range(len(test_image_list)):
    print(' i = ', i, test_image_list[i])



#######################################################################################
# predict : test 이미지 전체를 추론하고 결과 반환
results = model.predict(source='/content/Aquarium_Data/test/images/', save=True)
print(type(results))
# <class 'list'>, 63개



#######################################################################################
# 예측된 이미지 클래스 별 검출 결과 집계
import numpy as np

# YOLO 추론 결과에서 클래스 별 등장 횟수 카운팅, 각 클래스 번호와 이름 출력
for result in results:
    uniq, cnt = np.unique(result.boxes.cls.cpu().numpy().astype(int), return_counts=True)
    uniq_cnt_dict = dict(zip(uniq, cnt))    # 두 배열을 묶어서 dict 타입 생성
    # print(f'uniq_cnt_dict : {uniq_cnt_dict}')

    for c in result.boxes.cls:
        print('class num = ', int(c), ', class_name = ', model.names[int(c)])



#######################################################################################
# 예측된 이미지 파일 목록
detected_image_list = glob('/content/runs/detect/predict/*')
detected_image_nums = len(detected_image_list)
print('detected_image_nums : ', detected_image_nums)
print('\n')

print(detected_image_list)
print('\n')



#######################################################################################
# test data 기준 모델 성능 평가 점수 확인
metrics = model.val(
    data = '/content/Aquarium_Data/Aquarium_Data.yaml',
    split = 'test'
)
print('Precision : ', metrics.box.mp)
print('Recall : ', metrics.box.mr)
print('mAP50 : ', metrics.box.map50)    # IOU 0.5 기준에서 계산한 AP
print('mAP50-95 : ', metrics.box.map)   # mAP50 보다 엄격한 기준 



#######################################################################################
#######################################################################################
# Fine Tunning 된 새로운 모델로 감지를 원하는 이미지에 대해 검출 시도
from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

model = YOLO('/content/runs/detect/train/weights/best.pt')

# 사용자가 업로드한 이미지
image_path = '/content/newimg.png'

results_pred = model.predict(source=image_path, save=True, imgsz=416)

from pathlib import Path
result_img_path = Path(results_pred[0].save_dir) / Path(image_path).name
print(result_img_path)

img = Image.open()(result_img_path)
plt.imshow(img)
plt.axis('off')
plt.show()



#######################################################################################
# 탐지된 클래스 정보
import numpy as np
from collections import defaultdict

detected_classes = []
conf_dict = defaultdict(list)

for box in results_pred[0].boxes:
    cls_id = int(box.cls)
    cls_name = model.names[cls_id]
    conf = float(box.conf)
    detected_classes.append(cls_name)
    conf_dict[cls_name].append(conf)

print('탐지된 클래스 전체 : ', detected_classes)
print('\n')
print('고유 클래스 : ', sorted(set(detected_classes)))

# class 별 요약
for cls_name, confs in conf_dict.items():
    print(f' - {cls_name} : {len(confs):.2f}개, 평균 신뢰도={np.mean(confs):.3f}')