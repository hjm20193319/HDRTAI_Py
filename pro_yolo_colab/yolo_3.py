# 이미지 감지 후 결과 출력
# !pip install ultralytics opencv-python



################################################################################
import cv2
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt
import os
import koreanize_matplotlib

model = YOLO('yolo11n.pt')




#######################################################################################
image_path = 'image1.jpg'
image = cv2.imread(image_path)
if image is None:
    print('이미지 로딩 실패')
    exit()

# 이미지 감지 시작
results = model(image)
print(results)
# image at shape (1, 3, 416, 640)




#######################################################################################
# 원본 이미지 별도 기억 → 나중에 쓰기 위해서
original = image.copy()

person_count = 0    # 감지된 사람 수를 기억하기 위해서

for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])      # 바운딩 박스 좌표
        label = result.names[int(box.cls[0])]       # 감지된 객체 클래스 이름
        confidence = box.conf[0].item()             # 신뢰도

        if label.lower() == 'person' and confidence > 0.4:
            person_count += 1

        cv2.rectangle(image, (x1, y1), (x2, y2), (225, 255, 0), 2)
        cv2.putText(image, f'{label} : {confidence:.2f}', (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

print(f'감지된 사람 수는 {person_count}명 입니다.')



#######################################################################################
# !pip install koreanize_matplotlib
import koreanize_matplotlib





#######################################################################################
# 시각화
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title(f'감지된 사람 수는 {person_count}명 입니다.')
plt.show()





#######################################################################################
# 바운딩 박스 결과를 이미지로 저장
output_path = 'yolo3.jpg'
cv2.imwrite(output_path, image)
print('저장 성공')




#######################################################################################
# 바운딩 박스 좌표 출력
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])      # 바운딩 박스 좌표

        label = result.names[int(box.cls[0])]       # 감지된 객체 클래스

        confidence = box.conf[0].item()             # 신뢰도
        
        print(f'{label} → 신뢰도:{confidence}, 좌표=({x1},{y1}),({x2},{y2})')




#######################################################################################
# 신뢰도 높은 객체만 필터링 (예 : 70% 이상)
for idx, result in enumerate(results):
    print(f'이미지 {idx}번째 결과 : ')
    found = False

    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = result.names[int(box.cls[0])]
        confidence = box.conf[0].item()

        if confidence >= 0.7:
            print(f'   - {label} → 신뢰도:{confidence:.2f}')
            found = True

    if not found:
        print('   - 없음')



#######################################################################################
# 바운딩 박스 내부 객체 저장
for idx, result in enumerate(results):
    for j, box in enumerate(result.boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = result.names[int(box.cls[0])]
        confidence = box.conf[0].item()

        # 이미지에서 ROI (Region Of Interest : 관심 영역) 추출
        cropped = image[y1:y2, x1:x2]   # 배열 슬라이싱 (행 방향, 열 방향으로 자르기)
        
        # 저장 파일 만들기
        crop_path = f'crop_{idx}_{j}_{label}_{confidence:.2f}.jpg'
        cv2.imwrite(crop_path, cropped)
        print(f' → 객체 {label} ⇨ {crop_path} 저장 완료')
        


#######################################################################################
# 바운딩 박스 내부 객체 저장 - 2    (바운딩 박스 없이)
os.makedirs('crops', exist_ok=True)

for idx, result in enumerate(results):
    for j, box in enumerate(result.boxes):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = result.names[int(box.cls[0])]
        confidence = box.conf[0].item()

        # 이미지에서 ROI (Region Of Interest : 관심 영역) 추출
        cropped = original[y1:y2, x1:x2]   # 배열 슬라이싱 (행 방향, 열 방향으로 자르기)
        
        # 저장 파일 만들기
        crop_path = os.path.join('crops', f'crop_{idx}_{j}_{label}_{confidence:.2f}.jpg')
        cv2.imwrite(crop_path, cropped)
        print(f' → 객체 {label} ⇨ {crop_path} 저장 완료')




#######################################################################################
# 감지된 객체에 중심 좌표 출력 + 시각화
person_count = 0

for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])      # 바운딩 박스 좌표
        label = result.names[int(box.cls[0])]       # 감지된 객체 클래스
        confidence = box.conf[0].item()             # 신뢰도

        # 중심 좌표
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        if label.lower() == 'person':
            person_count += 1
            print(f'person ⇨ {person_count} : 중심 좌표 = ({center_x}, {center_y}), 신뢰도 : {confidence:.2f}')

            # 중심점을 원으로 그리기
            cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)

            # 텍스트 표시
            coord_text = f'({center_x}, {center_y})'
            cv2.putText(image, coord_text, (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

        # 바운딩 박스 출력
        cv2.rectangle(image, (x1, y1), (x2, y2), (225, 255, 0), 2)
        cv2.putText(image, f'{label} : {confidence:.2f}', (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

plt.figure(figsize=(6, 5))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title(f'감지된 사람 수는 {person_count}명 입니다.')
plt.show()




#######################################################################################
# 복수 이미지 처리
image_paths = ['image1.jpg', 'image2.jpg']
results = model(image_paths)

# 시각화
fig, axes = plt.subplots(1, len(image_paths), figsize=(12, 6))

for idx, (result, image_path) in enumerate(zip(results, image_paths)):
    print(f'\n이미지 {idx}번째 ({image_path}) 결과 : ')
    found = False

    # 원본 이미지 읽기
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for box in result.boxes:
        label = model.names[int(box.cls[0])]
        confidence = box.conf[0].item()

        if confidence >= 0.4:
            print(f'   - {label} → 신뢰도:{confidence:.2f}')
            found = True

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 225), 2)
            cv2.putText(image, f'{label} : {confidence:.2f}', (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if not found:
        print('   - 없음')

    axes[idx].imshow(image)
    axes[idx].axis('off')
    axes[idx].set_title(f'이미지 {idx}')

plt.tight_layout()
plt.show()