from flask import Flask, render_template, request # Flask: 웹 프레임워크, render_template: HTML 템플릿 렌더링, request: HTTP 요청 데이터 처리
import pandas as pd # 데이터 조작 및 분석을 위한 라이브러리 (DataFrame 사용)
import numpy as np # 수치 계산 및 다차원 배열 처리를 위한 라이브러리
import seaborn as sns # Matplotlib 기반의 시각화 라이브러리 (Iris 데이터셋 로드용)
import matplotlib # 파이토 시각화 라이브러리의 기본 패키지
matplotlib.use('Agg') # GUI 없이 백엔드에서 이미지 파일 생성을 위해 'Agg' 모드 설정
# Agg (Anti Grain Geometry) : matplotlib 렌더링 엔진 중 하나
# 이미지 저장시 오류 방지 : 차트 출력 없이 저장할 때 사용
import matplotlib.pyplot as plt # 그래프 작성을 위한 서브 모듈
import koreanize_matplotlib # Matplotlib 그래프 내 한글 깨짐 방지를 위한 라이브러리
from pathlib import Path # 객체 지향적 파일 시스템 경로 처리를 위한 모듈


app = Flask(__name__) # Flask 애플리케이션 인스턴스 생성

# Path(__file__).resolve(): 현재 실행 중인 스크립트의 절대 경로 확보
BASE_DIR = Path(__file__).resolve().parent      # 현재 파일의 디렉토리 경로 (프로젝트 루트)
STATIC_DIR = BASE_DIR / 'static' / 'images'               # static 디렉토리 경로 (이미지 저장소)
TEMPLATE_DIR = BASE_DIR / 'templates'            # templates 디렉토리 경로 (HTML 파일 저장소)

# mkdir(parents=True, exist_ok=True): 상위 디렉토리가 없으면 생성하고, 이미 존재해도 오류를 발생시키지 않음
STATIC_DIR.mkdir(parents=True, exist_ok=True) 
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/') # 기본 경로 접속 시 실행
def index():
    return render_template('main.html') # main.html 페이지 반환

@app.route('/showdata') # 데이터 시각화 및 테이블 표시를 위한 경로
def showdata():
    # sns.load_dataset('iris'): 내장된 붓꽃(Iris) 데이터셋(붓꽃 종류별 꽃잎/꽃받침 길이와 너비) 로드
    df = sns.load_dataset('iris') 
    print(df.head()) # 데이터 프레임의 상위 5개 행 콘솔 출력

    # pie chart 생성 및 저장(서버에서 자체 출력은 안함)
    # value_counts(): 범주형 데이터의 빈도수 계산, sort_index(): 인덱스(종 이름) 순으로 정렬
    counts = df['species'].value_counts().sort_index()
    plt.figure() # 새로운 그래프 도화지 생성
    # autopct: 비율 표시 형식, startangle: 시작 각도, ylabel: y축 라벨(여기서는 제거)
    counts.plot.pie(autopct='%1.1f%%', startangle=90, ylabel = ' ')
    plt.tight_layout() # 그래프 요소들이 겹치지 않도록 레이아웃 자동 조정
    img_path = STATIC_DIR / 'fpro19.png' # 저장할 이미지의 전체 경로 설정
    plt.savefig(img_path, dpi=130) # 지정된 경로에 이미지 저장 (dpi는 해상도 설정)
    plt.close() # 메모리 해제를 위해 생성된 그래프 닫기

    # to_html(): DataFrame을 HTML <table> 태그로 변환
    irishtml = df.to_html(
        classes='table table-striped table-sm', index=False # 부트스트랩 클래스 적용 및 인덱스 제외
    )

    return render_template( # 템플릿에 데이터와 이미지 경로 전달
        'show.html',
        table = irishtml,
        img_path='images/fpro19.png'
        
    )


if __name__ == '__main__': # 스크립트 직접 실행 시 서버 구동
    app.run(debug=True)
