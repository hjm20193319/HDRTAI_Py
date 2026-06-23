# 이미지 탐지 결과를 DataFrame에 저장해서 csv 저장한 후 이를 읽어 → 요약 통계 처리

# !pip install ultralytics opencv-python


#######################################################################################
import os
import pandas as pd
from ultralytics import YOLO

model = YOLO('yolo11n.pt')
img_dir = 'images'
imag_paths = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
print('img_paths : ', imag_paths)

records = []

for path in imag_paths:
    results = model(path, conf=0.25, verbose=False)[0]      # 단일 이미지 추론
    boxes = results.boxes
    names = results.names

    if len(boxes) == 0:
        records.append({
            'image':os.path.basename(path),
            'object_count':0,
            'classes':'',
            'avg_confidence':0.0
        })
        continue

    # cpu() : pytorch 텐서로 반환된 값을 cpu 메모리로 옮겨 numpy 배열로 변환 → float 형태
    cls_id = boxes.cls.cpu().numpy().astype(int)    # 탐지된 객체들의 클래스 id(정수 라벨 번호)
    print('cls_id : ', cls_id)
    # [0 0 3 0 0 2] → 이미지 6개 감지
    confs = boxes.conf.cpu().numpy()
    print('confs : ', confs)

    classes = [names[i] for i in cls_id]
    print('classes : ', classes)
    print('\n')
    avg_conf = float(confs.mean())

    records.append({
        'image':os.path.basename(path),
        'object_count':len(cls_id),
        'classes':','.join(sorted(set(classes))),
        'avg_confidence':round(avg_conf, 3)
    })




#######################################################################################
# records로 DataFrame에 저장
df = pd.DataFrame(records)
print(df)

df.to_csv('yolo6report.csv', index=False, encoding='utf-8-sig')
print('csv 저장 완료')




#######################################################################################
# csv 로딩
mydf = pd.read_csv('yolo6report.csv')
print(mydf)
print('\n')

num_images = len(mydf)
total_objects = mydf['object_count'].sum()    # 탐지 객체 총 개수

# 전체 confidence 평균
avg_confidence = mydf.loc[mydf['avg_confidence'] > 0, 'avg_confidence'].mean() if total_objects > 0 else 0.0

print(f'총 이미지 수 : {num_images}')
print(f'총 탐지 객체 수 : {total_objects}')
print(f'전체 confidence 평균 : {avg_confidence:.2f}')
print('\n')

class_counts = {}
for cls_str in mydf['classes']:
    if cls_str:
        for cls in cls_str.split(','):
            class_counts[cls] = class_counts.get(cls, 0) + 1    # 나눠진 리스트를 하나씩 반복

print('<클래스 별 등장 이미지 수>')

for k, v in class_counts.items():
    print(f'   - {k} : {v}개')
print('\n')

print(mydf.describe())
print('\n')

max_row = mydf.loc[mydf['object_count'].idxmax()]
print('가장 많이 감지된 객체는 ', max_row['image'], '에', max_row['object_count'], '개 입니다.')
print('\n')


# 평균 신뢰도막대 그래프
import matplotlib.pyplot as plt

plt.figure(figsize=(5, 3))
plt.bar(mydf['image'], mydf['avg_confidence'], color='skyblue')
plt.xlabel('Image')
plt.ylabel('Average Confidence')
plt.title('Average Confidence by Image')
plt.xticks(rotation=45, ha='center')
plt.ylim(0, 1)
plt.tight_layout()
plt.show()