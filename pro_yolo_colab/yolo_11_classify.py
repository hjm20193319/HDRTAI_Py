# YOLO 이미지 분류 모델
# 이미지 속 특정 객체의 위치를 찾는 대신 입력된 전체 이미지가
# 어떤 클래스(카테고리)에 속하는지 판별하고 해당 확률을 출력

# flower dataset 사용

# !pip install ultralytics opencv-python


#######################################################################################
import random
import shutil
from pathlib import Path
import tensorflow as tf
from ultralytics import YOLO
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

dataset_path = tf.keras.utils.get_file(
    fname = 'flower_photos',
    origin = 'http://download.tensorflow.org/example_images/flower_photos.tgz'
)

SOURCE_DIR = Path(dataset_path)
print('SOURCE_DIR : ', SOURCE_DIR)

classes = [p.name for p in SOURCE_DIR.iterdir() if p.is_dir()]
print('classes : ', classes)



#######################################################################################
# YOLO 학습용 dataset 폴더 생성
DATASET_DIR = Path('flower_dataset')

if DATASET_DIR.exists():
    shutil.rmtree(DATASET_DIR)

# train / val / test 폴더 생성
TRAIN_DIR = DATASET_DIR / 'train'
VAL_DIR = DATASET_DIR / 'val'
TEST_DIR = DATASET_DIR / 'test'

for class_dir in SOURCE_DIR.iterdir():
    if not class_dir.is_dir():  # 폴더가 아니면 skip
        continue

    class_name = class_dir.name # 클래스 이름 저장
    images = list(class_dir.glob('*.*'))    # 모든 이미지 파일 가져오기

    if len(images) == 0:
        continue

    random.shuffle(images)  # 학습 편향 방지를 목적으로 데이터 섞기

    total = len(images)
    print('total : ', total)
    train_end = int(total * 0.7)
    val_end = int(total * 0.9)

    # 데이터 분할 (7:2:1)
    splits = {
        'train':images[:train_end],
        'val':images[train_end:val_end],
        'test':images[val_end:]
    }

    print(len(splits['train']), len(splits['val']), len(splits['test']))

    # 분할된 이미지를 각 폴더에 복사
    for split_name, split_images in splits.items():
        target_dir = DATASET_DIR / split_name / class_name  # 저장 경로 생성
        target_dir.mkdir(parents=True, exist_ok=True)

        for img in split_images:
            shutil.copy2(img, target_dir/img.name)    # 파일 복사

# dataset 확인 (정상 생성 여부 확인)
for split in ['train', 'val', 'test']:
    print(f'[{split}]')
    for class_dir in (DATASET_DIR / split).iterdir():   # 클래스별 폴더 탐색
        count = len(list(class_dir.glob('*.*')))
        print(f'{class_dir.name} : {count}')
    print('\n')



#######################################################################################
# YOLO11 분류 모델을 학습 (train + val 사용)
model = YOLO('yolo11n-cls.pt')     # 사전 학습된 YOLO11 classification 모델(80개의 클래스로 분류)을 로딩

model.train(
    data = str(DATASET_DIR.resolve()),     # 경로는 절대 경로 사용
    epochs = 5,
    imgsz = 224,
    batch = 16,
    device = 'cpu'
)
print('학습 완료')




#######################################################################################
# 모델 성능 측정 - 가장 좋은 모델 로딩
best_model = YOLO('runs/classify/train/weights/best.pt')

y_true = [] # 실제 정답
y_pred = [] # 예측값

for class_dir in TEST_DIR.iterdir():
    true_label = class_dir.name # 폴더 이름이 클래스 이름
    
    for img_path in class_dir.glob('*.*'):
        results = best_model.predict(       # 예측 수행
            source = str(img_path),
            imgsz=224,
            verbose=False
        )

        r = results[0]      # 결과 1개 추출
        pred_idx = r.probs.top1     # 가장 높은 확률 클래스의 인덱스
        pred_label = r.names[pred_idx]    # 가장 높은 확률 클래스의 이름

        y_true.append(true_label)
        y_pred.append(pred_label)

# 성능 출력
acc = accuracy_score(y_true, y_pred)
print(f'Test Accuracy : {acc * 100:.2f}%')

report = classification_report(y_true, y_pred, target_names=classes)
print(report)

# confusion matrix → heatmap으로 혼동행렬 시각화
cm = confusion_matrix(y_true, y_pred, labels=classes)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix(test data)')
plt.tight_layout()
plt.savefig('yolo11cm.png')
plt.show()



#######################################################################################
# 새로운 이미지로 예측
sample_path = Path('myflower.jpg')

if sample_path.exists():
    results = best_model.predict(
        source = str(sample_path),
        imgsz = 224,
        verbose = False
    )
    r = results[0]
    pred_idx = r.probs.top1
    pred_label = r.names[pred_idx]
    confidence = float(r.probs.top1conf)    # 확신도

    print(sample_path)
    print('Predicted class : ', pred_label)
    print('Confidence : ', round(confidence, 3))


else:
    print('파일 없음')