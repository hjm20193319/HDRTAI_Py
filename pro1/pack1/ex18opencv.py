# Computer vision / opencv / Image
# pip install opencv-pythonc

import cv2
print(cv2.__version__)

img1 = cv2.imread('ani.jpg')
print(type(img1))       # <class 'numpy.ndarray'> 숫자를 읽음 

cv2.imshow('image test', img1)      # 읽은 것을 이미지로 보여주는 // 별도의 창을 지원
cv2.waitKey()       #  세워 두는 것 //// 무한 루프에 빠짐
cv2.destroyAllWindows()  # 닫는 것 (X버튼 눌러주면)

print('=============\n')

# 다른 이름으로 저장 
cv2. imwrite('ani2.jpg', img1)
cv2. imwrite('ani3.jpg', img1, [cv2.IMWRITE_JPEG_QUALITY, 10])

img2 = cv2.resize(img1, (300, 100), interpolation=cv2.INTER_AREA)       # 크기 조정
cv2.imwrite('ani4.jpg', img2)

# 이미지 크기 조정
# 이미지 밝기 조정
# 이미지 상하좌우 회전
# 특정 영역 자르기
# ...

'''
 C:\work\projects\pro1\pack1 디렉터리

2026-02-04  오후 03:00           143,408 ani.jpg
2026-02-04  오후 03:11           200,665 ani2.jpg
2026-02-04  오후 03:11            19,254 ani3.jpg    >>> 퀄리티는 떨어지지만 메모리를 절약할 수 있다
               3개 파일             363,327 바이트
               0개 디렉터리  362,278,236,160 바이트 남음
'''