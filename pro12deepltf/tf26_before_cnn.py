# 합성곱의 원리 이해 - 컵의 특징 추출

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from scipy.ndimage import correlate
from skimage import data
from skimage.color import rgb2gray
from skimage.transform import resize


#######################################################################################
# 컵 이미지를 읽어와 (64, 64)로 리사이즈
im = rgb2gray(data.coffee())
im = resize(im, (64, 64))
print(im.shape)
print('\n')


plt.axis('off')
plt.imshow(im, cmap='gray')
plt.show()



# 합성곱 필터 (3x3)
# filter = np.array([
#     [1,1,1],
#     [0,0,0],
#     [-1,-1,-1]
# ])

# 어떤 필터를 사용하는지에 따라 달라짐
filter = np.array([
    [-1,0,1],
    [-1,0,0],
    [-1,0,1]
    ])



# Padding : 상하좌우에 1픽셀씩 0으로 채우기
new_image = np.zeros(im.shape)
im_pad = np.pad(im, pad_width=1, mode='constant', constant_values=0)



# 합성곱(원소별 곱의 합) 연산 수행 : Convolution
# ↪ 원래 이미지 im의 크기에 대해 모든 픽셀 좌표 (i, j)를 탐색
for i in range(im.shape[0]):    # 0 ~ 63 (세로 방향)
    for j in range(im.shape[1]):     # 0 ~ 63 (가로 방향)
        try:
            new_image[i, j] = im_pad[i - 1, j - 1] * filter[0, 0] + im_pad[i - 1, j] * filter[0, 1] + \
            im_pad[i - 1, j + 1] * filter[0, 2] + im_pad[i, j - 1] * filter[1, 0] + im_pad[i, j] * filter[1, 1] + \
            im_pad[i, j + 1] * filter[1, 2] + im_pad[i + 1, j - 1] * filter[2, 0] + im_pad[i + 1, j] * filter[2, 1] + \
            im_pad[i + 1, j + 1] * filter[2, 2]
        except:
            pass

print(new_image)
print('\n')



# 시각화
plt.axis('off')
plt.imshow(new_image, cmap='gray')
plt.show()