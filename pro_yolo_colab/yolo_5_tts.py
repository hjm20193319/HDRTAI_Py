# 감지된 이미지 관련 음성으로 들려 주기
# TTS - Text To Speech
# STT - Speech To Text

# 유기 동물 탐지 후 보호소 안내 메세지 음성으로 출력

# !pip install ultralytics opencv-python playsound==1.2.2
# !pip install gtts



#######################################################################################
# TTS 연습
from gtts import gTTS
from IPython.display import Audio   # jupyter notebook 용
from playsound import playsound     # local 편집기용(vsc...)

def speakFunc(message):
    tts = gTTS(text=message, lang='ko')
    tts.save('yolo5test.mp3')   # 음성 파일로 저장
    return Audio('yolo5test.mp3', autoplay=True)    # 바로 재생 → jupyter
    # playsound('yolo5test.mp3')  # 재생 → 로컬


message = '19일 화요일은 영남을 중심으로 낮 기온이 올라 더울 전망이다. 전국 내륙을 중심으로 낮밤의 기온차가 클 것으로 보인다.이날 기상청은 오늘 경상권을 중심으로 낮 기온이 30도 이상으로 올라 덥겠고, 전국 내륙을 중심으로 낮과 밤의 기온차가 15도 안팎으로 크겠다고 예보했다. 건조특보가 발효된 서울 동북권과 서남권, 경기 일부 내륙을 중심으로 대기가 매우 건조할 것으로 보인다.'
speakFunc(message=message)




#######################################################################################
import cv2
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 보호소 정보 안내(텍스트 + 음성 재생)
def show_shelter_info_func(region, shelters, detected_info):
    shelter_info = shelters.get(region, shelters['기본'])
    pet_summary = f"{detected_info['count']}마리 ({', '.join(detected_info['labels'])})"

    message = (
        f'유기 동물 탐지 결과\n'
        f'  - 탐지된 동물 수 : {detected_info['count']}\n'
        f'  - 종류 : {detected_info['labels']}\n\n'
        f'<{region} 지역 보호소 정보> \n → {shelter_info}'
    )
    print('보호소 정보 : \n', message)

    # 음성 안내
    try:
        tts = gTTS(text=f'{region} 지역에 유기된 {pet_summary}가 감지 되었습니다. 가까운 보호소는 {shelter_info}입니다', lang='ko')
        tts.save('yolo5shelter.mp3')
        # display(Audio('yolo5shelter.mp3', autoplay=True))
    
    except Exception as err:
        print(f'음성안내 실패 : {err}')


def handle_stray_pet_func(region, shelters, detected_info):
    print('유기 동물로 추정됨')
    show_shelter_info_func(region, shelters, detected_info)

region = '테헤란로 사거리 삼원빌딩 앞'
shelters = {
    '서울':'서울 반려동물 보호센터:02-1234-5678',
    '기본':'전국 유기동물 보호연합:1577-8888'
}
detected_info = {
    'count':3,
    'labels':['호랑이', '사자', '코끼리']
}

handle_stray_pet_func(region, shelters, detected_info)




#######################################################################################
# 본격적으로 이미지 내 객체 감지 후 함수 호출

# 탐지 정보 로그 저장
def save_detection_log_func(image_path, detection_data):
    log_file = 'yolo5log.txt'
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, mode='a', encoding='utf-8') as log:
        log.write(f'\n[{now} 이미지] - {image_path}\n')
        log.write(f'탐지된 객체 수 : {len(detection_data)}\n')
        for d in detection_data:
            log.write(f'  - {d['label']} : box={d['box']}, confidence={d['confidence']:.2f}\n')
        log.write('-' * 40 + '\n')
    print(f'탐지 결과가 {log_file} 파일에 저장되었습니다.')



# 유기동물 감지 함수
def detect_pets_func(image_path):
    pet_desc = {
        'dog':'강아지',
        'cat':'고양이',
        'bird':'새',
        'fish':'물고기',
        'horse':'말',
        'sheep':'양',
        'cow':'소',
        'elephant':'코끼리',
        'bear':'곰',
        'zebra':'얼룩말'
    }

    shelters = {
    '서울':'서울 반려동물 보호센터:02-1234-5678',
    '기본':'전국 유기동물 보호연합:1577-8888',
    '부산':'부산 유기동물 보호소:051-123-4567'
    }

    stray_keywords = ['street', 'road', 'outside', 'stray'] 

    model = YOLO('yolo11n.pt')
    image = cv2.imread(image_path)

    if image is None:
        print('이미지 로딩 실패')
        return
    
    results = model(image)
    detected_pets = []      # 감지된 객체 레이블 저장
    detection_data = []     # 감지된 객체 정보 저장

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[int(box.cls[0])]
            confidence = box.conf[0].item()

            if label in pet_desc:
                detected_pets.append(label)
                detection_data.append({
                    'label':pet_desc[label],
                    'confidence':confidence,
                    'box':(x1, y1, x2, y2)
                })
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(image, f'{label} : {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과 이미지 저장
    output_path = 'yolo5out.jpg'
    cv2.imwrite(output_path, image)

    # 시각화
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    if detected_pets:   # 감지된 동물이 있는 경우
        print('유기 동물 탐지 결과 : ')
        for pet in set(detected_pets):
            print(f' - {pet_desc.get(pet, pet)}')       # 라벨에 대한 한글 변환

    # 감지 정보 파일로 저장
    save_detection_log_func(image_path=image_path, detection_data=detection_data)

    # 유기동물 조건 확인
    # 감지 동물이 dog, cat이고 이미지 경로에 street, stray 등의 키워드가 포함되면 유기동물로 판단
    if any(pet in ['dog', 'cat'] for pet in detected_pets) and any(keyword in image_path.lower() for keyword in stray_keywords):
        detected_info = {
            'count':len(detection_data),
            'labels':sorted(set([d['label'] for d in detection_data]))
        }
    
        # 유기 동물로 판단되었으므로 보호소 정보를 음성 + 텍스트로 안내
        handle_stray_pet_func(region='서울', shelters=shelters, detected_info=detected_info)
    else:
        print('유기동물이 감지되지 않았습니다')


detect_pets_func('street_ani.png')