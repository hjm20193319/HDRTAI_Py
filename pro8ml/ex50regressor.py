# [문법] sklearn 제공 Resgressor 성능 비교
# [문법] pipeline + GridSearchCV + 교차검증 + 성능확인 + 시각화

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.datasets import load_diabetes  # 당뇨병 데이터
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline   #  중요! 잘쓰면 좋음
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score    # Regression 평가
# [추천] 회귀 모델 평가 시 MAE(Mean Absolute Error)를 추가하여 오차의 실제 규모를 직관적으로 파악하는 것을 권장함.

# 데이터
data = load_diabetes() # [문법] load_diabetes(): 사이킷런에서 제공하는 당뇨병 진행도 예측용 회귀 데이터셋 로드.
print(data.DESCR) # [문법] DESCR: 데이터셋의 각 특성(age, bmi, bp 등)과 타겟에 대한 상세 설명 출력.
#     - age     age in years
#     - sex
#     - bmi     body mass index
#     - bp      average blood pressure
#     - s1      tc, total serum cholesterol
#     - s2      ldl, low-density lipoproteins
#     - s3      hdl, high-density lipoproteins
#     - s4      tch, total cholesterol / HDL
#     - s5      ltg, possibly log of serum triglycerides level
#     - s6      glu, blood sugar level
print('\n')

x = data.data # [문법] data: 독립변수(Feature) 행렬.
y = data.target # [문법] target: 종속변수(Target), 1년 뒤 당뇨병 진행도를 나타내는 수치.
print(x[:2])
print(y[:2])
print('\n')
# [문법] 타겟 데이터가 연속형 수치이므로 회귀(Regression) 분석을 수행함.

# train/test 분리
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42) # [문법] 데이터를 학습용(80%)과 테스트용(20%)으로 분리.

# Pipeline + GridSearchCV
models = { # [문법] 여러 모델의 파이프라인과 하이퍼파라미터 후보군을 딕셔너리 형태로 정의.
    "LinearRegression":{
        "pipeline":Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        "params":{
            "model__fit_intercept":[True, False]
        }
    },
    "RandomForest":{
        "pipeline":Pipeline([
            ("model", RandomForestRegressor(random_state=42)) # [문법] RandomForestRegressor: 여러 결정 트리의 평균으로 예측하는 앙상블 모델.
        ]),
        "params":{
            "model__n_estimators":[100, 200],
            "model__max_depth":[None, 5, 10],
            "model__min_samples_split":[2, 5]       
        }    
    },
    "XGBoost":{
        "pipeline":Pipeline([
            ("model", XGBRegressor(random_state=42, verbosity=0)) # [문법] XGBRegressor: Gradient Boosting 기반의 고성능 회귀 모델.
        ]),
        "params":{
            "model__n_estimators":[100, 200],
            "model__learning_rate":[0.01, 0.05],
            "model__max_depth":[3, 5]
        }
    },
    "SVR":{
        "pipeline":Pipeline([
            ("scaler", StandardScaler()),
            ("model", SVR()) # [문법] SVR: Support Vector Machine의 회귀 버전. 거리 기반이므로 스케일링 필수.
        ]),
        "params":{
            "model__C":[0.1, 1, 10], # [문법] C: 오차에 대한 규제 강도.
            "model__kernel":["rbf"],
            "model__gamma":["scale", "auto"]
        }
    },
    "KNN":{
        "pipeline":Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsRegressor()) # [문법] KNeighborsRegressor: 가장 가까운 K개 이웃의 평균값으로 예측.
        ]),
        "params":{
            "model__n_neighbors":[3, 5, 7],
            "model__weights":["uniform", "distance"]
        }
    }
}

# GridSearchCV 실행
results = []
best_models = {}

# 각 모델을 순서대로 반복 처리 : best 모델 추출, 성능 저장
for name, config in models.items():
    print(f'{name} 튜닝 중 ...')
    grid = GridSearchCV( # [문법] GridSearchCV: 교차 검증을 통해 최적의 하이퍼파라미터 조합을 탐색.
        config["pipeline"],
        config["params"],
        cv=5, # [문법] 5-Fold 교차 검증 수행.
        scoring="r2", # [문법] 평가 지표로 결정 계수(R2) 사용.
        n_jobs=-1, # [문법] 모든 CPU 코어를 사용하여 병렬 처리.
    )
    grid.fit(x_train, y_train) # [문법] fit(): 전처리 및 파라미터 튜닝 학습 수행.

    pred = grid.predict(x_test) # [문법] predict(): 테스트 데이터에 대한 예측값 생성.

    rmse = np.sqrt(mean_squared_error(y_test, pred)) # [문법] mean_squared_error: 평균 제곱 오차의 제곱근(낮을수록 우수).
    r2 = r2_score(y_test, pred) # [문법] r2_score: 모델의 설명력을 나타내는 결정 계수(1에 가까울수록 우수).

    results.append([name, rmse, r2])
    best_models[name] = grid.best_estimator_ # [문법] best_estimator_: 최적 파라미터로 학습된 모델 객체 저장.

    print('best params : ', grid.best_params_) # [문법] best_params_: 탐색된 최적의 파라미터 조합 출력.
    print('best score : ', grid.best_score_) # [문법] best_score_: 검증 데이터셋에서의 최고 평균 점수.
    print('R2 : ', r2)  # [문법] 테스트 데이터셋에 대한 최종 설명력 확인.
    print('\n')

# 최종 결과 DataFrame 에 저장
df_results = pd.DataFrame(results, columns=["modelname", "rmse", "r2"])
df_results = df_results.sort_values(by="r2", ascending=False)
print('최종 성능 비교')
print(df_results)
print('\n')

# 최종 성능 비교
#           modelname       rmse        r2
# 3               SVR  51.791775  0.493713
# 2           XGBoost  53.293563  0.463926
# 1      RandomForest  53.482640  0.460115
# 0  LinearRegression  53.853446  0.452603
# 4               KNN  54.244609  0.444622

# 성능 비교를 위한 시각화
plt.figure(figsize=(12, 5)) # [문법] subplots를 활용하여 R2와 RMSE를 동시에 비교 시각화.
# R2
plt.subplot(1, 2, 1)
sns.barplot(x="modelname", y="r2", data=df_results) # [문법] sns.barplot: 모델별 결정 계수 비교.
plt.title("튜닝 모델의 결정계수 R2")
plt.xticks(rotation=30)
plt.ylim(0.4, 0.5) # [문법] 차이를 명확히 보기 위해 y축 범위 제한.
# RMSE
plt.subplot(1, 2, 2)
sns.barplot(x="modelname", y="rmse", data=df_results) # [문법] sns.barplot: 모델별 오차(RMSE) 비교.
plt.title("RMSE")
plt.ylim(50, 55)
plt.xticks(rotation=30)
plt.tight_layout() # [문법] 그래프 간 겹침 방지를 위한 레이아웃 조정.
plt.show()

# best model 예측 시각화
# 최고 모델 선택
best_modelname = df_results.iloc[0]["modelname"]
best_model = best_models[best_modelname]

# [문법] 최적 모델을 사용한 최종 예측.
pred = best_model.predict(x_test) 

# 시각화
plt.figure(figsize=(6, 6))
plt.scatter(y_test, pred) # [문법] 실제값과 예측값의 상관관계를 산점도로 표현.
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--') # [문법] 완벽한 예측을 의미하는 대각선(y=x) 추가.
plt.xlabel('실제값')
plt.ylabel('예측값')
plt.title(f'최고 모델 {best_modelname}')
plt.tight_layout()
plt.show()