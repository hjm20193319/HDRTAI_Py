from hmac import new

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import param
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.model_selection import StratifiedKFold, GridSearchCV

# 데이터
df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/patient.csv')
pdata = df.head(3)
df_x = df.drop(['ID', 'STA'], axis=1)
df_y = df['STA']
print(df_x.info())
print(df_y.info())
print('\n')
print(df.isnull().sum())
print('\n')

# 테스트 데이터 분리
train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, test_size=0.3, random_state=12)

# 모델
pipe = Pipeline([
    ('model', RandomForestClassifier(random_state=12))
])

# 하이퍼 파라미터
param_grid = {
    'model__n_estimators': [100, 500],
    'model__max_depth': [5, 10, None],
    'model__class_weight': [None, 'balanced']
}

# 교차검증
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)

grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    cv=cv,
    scoring='roc_auc',
    n_jobs=-1
)
grid.fit(train_x, train_y)

print('최적의 파라미터 : ', grid.best_params_)
print('최적의 점수 : ', grid.best_score_)
# 최적의 파라미터 :  {'model__class_weight': None, 'model__max_depth': 5, 'model__n_estimators': 100}
# 최적의 점수 :  0.9702891156462584
print('\n')

# 예측
pred = grid.predict(test_x)
proba = grid.predict_proba(test_x)[:, 1]

# 평가
print('정확도 : ', accuracy_score(test_y, pred))
print('roc_auc score : ', roc_auc_score(test_y, proba))
# 정확도 :  0.8666666666666667
# roc_auc score :  0.9346590909090909
print('\n')
print('classification report : \n', classification_report(test_y, pred))
# classification report :
#                precision    recall  f1-score   support

#            0       0.89      0.93      0.91        44
#            1       0.79      0.69      0.73        16

#     accuracy                           0.87        60
#    macro avg       0.84      0.81      0.82        60
# weighted avg       0.86      0.87      0.86        60
print('\n')

bestmodel = grid.best_estimator_

# 변수 중요도
importances = grid.best_estimator_.named_steps['model'].feature_importances_
indices = np.argsort(importances)[::-1]

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib

plt.figure(figsize=(10, 5))
plt.barh(range(df_x.shape[1]), importances[indices], align='center')
plt.xticks(range(df_x.shape[1]), df_x.columns[indices])
plt.xlabel('변수')
plt.ylabel('중요도')
plt.title('변수 중요도')
plt.tight_layout()
plt.ylim(-1, df_x.shape[1])
plt.savefig('static/images/importance.png')
plt.close()
print('\n')


# Flask
app = Flask(__name__)

@app.route('/')
def main():
    acc = np.round(accuracy_score(test_y, pred), 4)
    p_data = pdata.to_dict(orient='records')
    return render_template('main.html', p_data=p_data, acc=acc)


@app.route('/show')
def show():
    return render_template('show.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.post('/predict')
def predict():
    new_data = {
            'AGE': int(request.form.get('age')),
            'SEX': int(request.form.get('sex')),
            'RACE': int(request.form.get('race')),
            'SER': int(request.form.get('ser')),
            'CAN': int(request.form.get('can')),
            'CRN': int(request.form.get('crn')),
            'INF': int(request.form.get('inf')),
            'CPR': int(request.form.get('cpr')),
            'HRA': int(request.form.get('hra'))
        }
    
    new_df = pd.DataFrame(new_data, index=[0])
    print(new_df.head())

    # 예측
    pred = bestmodel.predict(new_df)
    result = '사망..' if pred[0] == 1 else '생존!'
    
    return render_template('list.html', result=result)












if __name__ == '__main__':
    app.run(debug=True)