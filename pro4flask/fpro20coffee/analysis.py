from pathlib import Path
import scipy.stats as stats # [문법] scipy.stats: 통계 분석을 위한 다양한 확률 분포 및 검정 함수 제공
import pandas as pd # [문법] pandas: 데이터 조작 및 분석을 위한 라이브러리 (DataFrame 사용)
import matplotlib.pyplot as plt # [문법] matplotlib.pyplot: 데이터 시각화를 위한 서브 모듈
import koreanize_matplotlib # [개념] 한글 폰트 설정 없이도 그래프 내 한글 깨짐을 자동 해결
import matplotlib # [문법] matplotlib: 파이썬의 대표적인 시각화 라이브러리
matplotlib.use('Agg') # [개념] GUI가 없는 환경(서버 등)에서 그래프를 파일로 저장하기 위해 Non-Interactive 백엔드 설정

# [추천] : 분석 대상이 되는 범주형 데이터의 순서를 미리 정의하여 시각화나 집계 시 일관성을 유지합니다.
BRAND_ORDER = ['스타벅스', '폴바셋', '이디야', '탐앤탐스']

def analysis_func(rdata:list[dict]):
    # [문법] pd.DataFrame(rdata): 리스트 내의 딕셔너리 객체들을 행(Row) 데이터로 변환하여 데이터프레임 생성
    df = pd.DataFrame(rdata)
    
    if df.empty:
        return pd.DataFrame(), '데이터가 없음', pd.DataFrame()
    
    # [문법] dropna(subset=[...]): 특정 컬럼에 결측치(NaN)가 있는 행만 선택적으로 제거
    df = df.dropna(subset=['gender', 'co_survey'])

    # 성별 커피브랜드별 선호 빈도수
    # [개념] 교차표(Contingency Table): 두 범주형 변수의 빈도를 행과 열로 교차하여 집계한 표
    croassTab = pd.crosstab(index=df['gender'], columns=df['co_survey'])

    # [개념] 카이제곱 검정 조건: 데이터의 크기가 너무 작으면 통계적 유의성을 확보하기 어려움
    if croassTab.size == 0 or croassTab.shape[0] < 2 or croassTab.shape[1] < 2:
        return croassTab, '표본 자료가 부족해, 카이제곱 검정 수행 불가', df
    
    # 유의 수준 : 0.05 (5%)
    # [개념] 유의수준(Alpha): 귀무가설이 참일 때 이를 기각할 확률의 최대 허용 한계
    alpha = 0.05

    # [문법] stats.chi2_contingency: 독립성 검정을 수행하여 통계량, p-value, 자유도, 기대빈도를 반환
    chi2, p, dof, expected = stats.chi2_contingency(croassTab)
    
    # [개념] 기대빈도(Expected Frequency): 두 변수가 서로 독립일 때 이론적으로 예상되는 빈도
    min_expected = expected.min()
    note = ''
    # [추천] : 카이제곱 검정은 모든 셀의 기대빈도가 5 이상일 때 신뢰도가 높으므로, 미달 시 경고 메시지를 포함하는 것이 좋습니다.
    if min_expected < 5:
        note = f'<br><small>* 주의 : 기대빈도 최소값 {min_expected:.2f} (5 미만)</small>'

    # [개념] p-value 판정
    # p-value >= alpha: 귀무가설 채택 (두 변수 간 연관성이 없음)
    # p-value < alpha: 귀무가설 기각, 대립가설 채택 (두 변수 간 연관성이 있음)
    
    # [추천] : f-string 내부에 HTML 태그(<b>)를 사용하여 웹 페이지 출력 시 가독성을 높일 수 있습니다.
    if p >= alpha:
        # 귀무가설 : 성별과 커피 브랜드 선호도는 관련이 없다.
        results = f'p값 {p:.5f} >= {alpha} : 성별에 따라 커피 선호 브랜드는 <b>차이가 없다(귀무 가설)</b> {note}'
    else:
        # 대립가설 : 성별과 커피 브랜드 선호도는 관련이 있다.
        results = f'p값 {p:.5f} < {alpha} : 성별에 따라 커피 선호 브랜드는 <b>차이가 있다(대립 가설)</b> {note}'

    return croassTab, results, df

def save_barchart_func(df:pd.DataFrame, out_path:Path) -> bool:
    if df is None or df.empty or 'co_survey' not in df.columns:
        return False
    
    # [문법] value_counts(): 범주형 데이터의 빈도 계산
    # [문법] reindex(fill_value=0): 지정된 BRAND_ORDER 순서로 재배치하고, 데이터가 없는 브랜드는 0으로 채움
    counts = df['co_survey'].value_counts().reindex(BRAND_ORDER, fill_value=0)
    
    # [문법] mkdir(parents=True, exist_ok=True): 저장 경로의 상위 디렉토리가 없으면 생성하고, 이미 있으면 무시
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure() # [개념] 새로운 Figure(도화지) 객체 생성
    # [문법] plot(kind='bar'): Pandas Series 객체에서 직접 막대 그래프 생성
    ax = counts.plot(kind='bar', width=0.6, edgecolor='black')
    ax.set_xlabel('커피 브랜드')
    ax.set_ylabel('선호 건수')
    ax.set_title('커피 브랜드별 선호 건수')
    ax.set_xticklabels(BRAND_ORDER, rotation=0) # [문법] x축 눈금 라벨 설정 및 회전 각도(0도) 지정
    fig.tight_layout() # [추천] : 그래프 요소들이 겹치지 않도록 여백을 자동으로 조정합니다.
    fig.savefig(str(out_path), dpi=120, bbox_inches='tight') # [문법] savefig: 그래프를 이미지 파일로 저장
    plt.close(fig) # [추천] : 메모리 누수 방지를 위해 사용이 끝난 Figure 객체를 명시적으로 닫습니다.

    return True
```