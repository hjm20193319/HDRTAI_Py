# 내가 그린 숫자 이미지 분류

# 손글씨 이미지 읽기
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib


#######################################################################################
im = Image.open('num.png')
img = np.array(im.resize((28, 28), Image.Resampling.LANCZOS).convert('L'))
# L 모드 : 흑백 이미지 픽셀값이 0~255 범위(0:검정, 255:흰색)
print(img)

plt.imshow(img, cmap='Greys')   # 색 반전
plt.show()

data = img.reshape([1, 784]).astype('float32')
data = data / 255.0


#######################################################################################
import tensorflow as tf

mymodel = tf.keras.models.load_model('tf23model.keras')
print('모델 로드 완료')
print('\n')

new_pred = mymodel.predict(data, verbose=0)
print('분류 결과 : ', new_pred)
print('예측값 : ', np.argmax(new_pred, 1)[0])