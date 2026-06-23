# YOLO Segmentation : 이미지 분할 - 객체 모양 그대로 영역(mask)을 찾음
# !pip install ultralytics opencv-python

#######################################################################################
import os, cv2, numpy as np
from ultralytics import YOLO

IMG_PATH = 'image1.jpg'
OUT_DIR = 'seg_out'     # 출력 저장 폴더
os.makedirs(OUT_DIR, exist_ok=True)

im = cv2.imread(IMG_PATH)
assert im is not None, f'이미지 없음:{IMG_PATH}'

H, W = im.shape[:2]     # 원본 이미지 높이/너비 얻기 → Mask resize 에 필요

model = YOLO('yolo11n-seg.pt')  # segmentation 용 모델
res = model(im)[0]
imsi = res
print(imsi.boxes)   # 탐지 박스 정보
print(imsi.masks)   # Segmentation Mask information
# mask : 객체를 박스가 아니라 픽셀 단위로 표시한 영역을 말함
# masks.data → 개별 마스크 이미지 데이터
# masks.xy → 객체 윤곽선 좌표

cv2.imwrite(os.path.join(OUT_DIR, '00_annotated.jpg'), res.plot())
# 원본 이미지 위에 바운딩 박스 + 클래스 라벨 + 신뢰도를 마스크로 처리
# 현재는 sanity check(기본 검증) 를 함

if res.masks is None or len(res.masks.data) == 0:   # Seg 결과가 없을 때
    print('마스크 객체가 없음')
    raise SystemExit()

m_small = res.masks.data.cpu().numpy()  # (N, h, w) float tensor를 numpy 배열로 변환
# print(m_small)  0 ~ 1 사이 값

masks= np.stack([
    cv2.resize(m, (W, H), cv2.INTER_NEAREST) > 0.5 for m in m_small
    # cv2.INTER_NEAREST : 최근접 이웃 보간법 → 흐림 방지
], axis=0)  # mask를 모아 (N,H,W) 배열로 만듦, mask는 최종적으로 N개의 bool 스텍이 됨


# Seg 전 단계 : Mask preview
mask_union = (masks.any(axis=0).astype(np.uint8) * 225)     # opencv 에서 이미지 저장 범위가 0 ~ 225
cv2.imwrite(os.path.join(OUT_DIR, '01_mask_preview.png'), mask_union)   # 단일 마스크 흑백 이미지 저장




#######################################################################################
# 최종 Segmentation : 컬러 오버레이 + 외곽선

def color(i):
    return ((37 * i) % 256, (17 * i) % 256, (91 * i) % 256)
    # 색상을 tuple로 반환 - 고유 색상을 주기 위함 → 마스크 외과선을 위함


final = im.copy()   # 최종 합성용 캔버스
blend = np.zeros_like(im)   # im과 같은 크기의 빈 캔버스

for i. n in enumerate(masks):
    blend[m] = color(i)     # 마스크 영역에 고유색 채우기
    cnts, _ = cv2.findContours(     # 마스크 경계 추출
        (m.astype(np.uint8) * 255),
        cv2.RETR_EXTERNAL,          # 가장 바깥쪽 외곽선
        cv2.CHAIN_APPROX_SIMPLE     # 꼭지점 단순화
    )
    cv2.drawContours(final, cnts, -1, (255, 255, 255), 2, cv2.LINE_AA)  # 외곽선만 얹어 경계 시각화

# 반 투명 합성
final = cv2.addWeighted(final, 1.0, blend, 0.45, 0.0)
cv2.imwrite(os.path.join(OUT_DIR, '02_final_seg.png'), final)   # 최종 결과 저장

# local 용 코드
# cv2. imshow('final seg', final)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# colab(jupyter 방법)
from google.colab.patches import cv2_imshow
cv2_imshow(final)
