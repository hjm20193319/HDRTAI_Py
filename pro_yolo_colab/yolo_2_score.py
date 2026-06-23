# Preciscion, Recall, mAP 확인하기
!unzip aquarium_dataset.zip -d aquarium_dataset



#######################################################################################
!pip install ultralytics opencv-python



#######################################################################################
from ultralytics import YOLO

model = YOLO('yolo11n.pt')

metrics = model.val(
    data = r'aquarium_dataset/aquarium_dataset/data.yaml',
    imgsz = 640
)


print('Precision : ', metrics.box.mp)
print('Recall : ', metrics.box.mr)
print('mAP50 : ', metrics.box.map50)    # IOU 0.5 기준에서 계산한 AP
print('mAP50-95 : ', metrics.box.map)   # mAP50 보다 엄격한 기준
# Precision :  0.02657698596149982
# Recall :  0.0926869970987618
# mAP50 :  0.01988449241985285
# mAP50-95 :  0.011751987471109789

# 점수가 낮은 이유는 백본은 coco dataset(라벨 80개)
# aquarium dataset → 라벨 7개