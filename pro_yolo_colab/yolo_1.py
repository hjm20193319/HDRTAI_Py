#######################################################################################
# COLAB 환경에는 YOLO가 설치 되어 있지 않음
# 프로그램 적인 설치 방법
# import subprocess
# import sys
# try:
#     from ultralytics import YOLO


# except ModuleNotFoundError as err:
#     print('ultralytics가 설치되지 않음 : ', err)
#     try:
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ultralytics', 'opencv-python'])
    
#     except subprocess.CalledProcessError as e:
#         raise SystemExit(f'ultralytics 설치 실패 : {e}')

#     from ultralytics import YOLO

#######################################################################################
# 실습 시 설치 방법
!pip install ultralytics opencv-python



#######################################################################################
# 정보 확인
import ultralytics
ultralytics.checks()
# Ultralytics 8.4.51 🚀 Python-3.12.13 torch-2.10.0+cpu CPU (Intel Xeon CPU @ 2.20GHz)
# Setup complete ✅ (2 CPUs, 12.7 GB RAM, 20.5/107.7 GB disk)



#######################################################################################
# YOLO 11 모델로 이미지 감지 실습
from ultralytics import YOLO
import ultralytics

print(ultralytics.__version__)      # 8.4.51

model = YOLO('yolo11n.pt')  # → nano version (s, m l, xl version also exists)
print(model.names, len(model.names))
# {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train' ........}
# ↪ COCO dataset 으로 학습된 모델이므로 라벨 80개가 있다




#######################################################################################
# 이미지 로딩 후 감지
from PIL import Image
import matplotlib.pyplot as plt
import sys

# image_path = 'dog.jpg'
image_path = 'images.jpg'

try:
    image = Image.open(image_path)
    plt.imshow(image)
    plt.axis('off')
    plt.show()

except Exception as err:
    print('load error : ', err)
    sys.exit()



#######################################################################################
# 객체 감지
import cv2
import numpy as np

try:
    # results = model(image)
    results = model(image, conf = 0.25)
    print(results[0].orig_shape)

except Exception as err:
    print('imference error : ', err)
    sys.exit()


image = np.array(image)     # Pillow image → image.open() → np.array() 하면, (H, W, 3) 형태의 numpy 배열
print('image.shape : ', image.shape)
# print('image[:5, :5] : ', image[:5, :5])
print('image[0, 0] : ', image[0, 0])



# 이미지 영역 자르기
cropped = image[:100, :100]
plt.imshow(cropped)
plt.axis('off')
plt.show()




#######################################################################################
# dog 이미지에 박스 채우기
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

dog_detected = False    # dog 감지 여부 판단용 함수

for result in results:
    try:
        for box in result.boxes:    # 감지된 객체들의 바운딩 박스 리스트
            x1, y1, x2, y2 = map(int, box.xyxy[0])      # 바운딩 박스 좌표 반환
            print(x1, y1, x2, y2)
            label = result.names[int(box.cls[0])]   # 감지된 객체 클래스 이름 얻기
            print(label)

            #  YOLO의 confidence = Objectness × Class probability로 계산
            print('box.conf[0] : ', box.conf[0])    # box.conf[0] :  tensor(0.7494)
            confidence = box.conf[0].item()     # 신뢰도(바운딩 박스 안에 해당 클래스가 실제로 있을 확률 값)
            print('confidence : ', confidence)      # 0.75 정도 신뢰도

            if label == 'dog' and confidence > 0.4:
                dog_detected = True


            # 바운딩 박스 그리기
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f'{label} : {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #          대상 이미지      텍스트                       위치                글꼴 종류     크기    글씨색   두께         


    except Exception as err:
        print('process error : ', err)

print('dog_detected : ', dog_detected)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()


# 결과 출력
print('\n')
if label == 'dog' and confidence > 0.4:
    print('개가 보입니다')


# 감지 결과를 파일로 저장
cv2.imwrite('yolo1out.jpg', image)


# colab에서 저장한 이미지 다운로드할 경우
from google.colab import files
files.download('yolo1out.jpg')