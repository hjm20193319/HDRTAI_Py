from flask import Flask, render_template, request
import pymysql
import pandas as pd
# import numpy as np
# 💡 [추천] 현재 코드에서는 numpy를 사용하지 않고 있습니다. 사용하지 않는 모듈은 제거하여 가볍게 유지하는 것이 좋습니다.
from markupsafe import escape
# import sys
# 💡 [추천] sys 모듈 역시 현재 사용되지 않으므로 제거를 권장합니다.
import matplotlib.pyplot as plt
# 💡 [중요 추천] Flask 같은 웹 애플리케이션에서 matplotlib을 사용할 때는 백엔드를 'Agg'로 설정하는 것이 좋습니다.
# 예: matplotlib.use('Agg')
# 이렇게 하지 않으면 멀티 스레드 환경에서 GUI 관련 에러가 발생하거나 서버가 다운될 위험이 있습니다.
import koreanize_matplotlib
import seaborn as sns



app = Flask(__name__)

# 💡 [추천] 데이터베이스 접속 정보(비밀번호 등)는 코드에 직접 작성(Hardcoding)하기보다는,
# python-dotenv 모듈 등을 활용해 환경변수(.env) 파일로 분리하는 것이 보안상 매우 중요하고 안전합니다.
db_config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8mb4'
}

def get_connection():
    return pymysql.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.get('/listshow')
def listshow():

    sql = '''
        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, year(now())-year(jikwonibsail), busernum, jikwongen
        from jikwon left outer join buser
        on jikwon.busernum = buser.buserno
        order by busernum asc, jikwonname asc 
    '''

    with get_connection() as conn:

        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [c[0]for c in cur.description]       # 각 칼럼의 정보 얻기
            
            # 💡 [추천] pymysql로 직접 fetchall()을 하는 것도 좋지만, 
            # pandas의 `pd.read_sql(sql, conn)`을 사용하면 위 과정을 한 줄로 처리하고 바로 DataFrame을 만들 수 있어 훨씬 간편합니다.

    df = pd.DataFrame(rows, columns=cols)
    df.columns = ['사번', '이름', '부서', '직급', '연봉', '근무년수', '부서번호', '성별']
    df1=df[['사번', '이름', '부서', '직급', '연봉', '근무년수']].to_html(index=False)

    df_pay = (
        # 💡 [참고] 문제 2번에서 "부서명, 직급 자료를 이용하여"라고 명시되어 있습니다.
        # 따라서 df.groupby(['부서', '직급']) 으로 두 개를 묶어주는 것이 출제 의도에 더 정확히 부합할 수 있습니다.
        df.groupby(['부서', '직급'])['연봉']
        .agg(
            연봉합 = 'sum',
            연봉평균 = 'mean'            
        )
        .round(2)
        .reset_index()
    )
    paydata = df_pay.to_html(index=False)

    plt.figure()
    plt.subplot(1,2,1)
    plt.bar(df_pay['부서'], df_pay['연봉합'])
    plt.title('부서별 연봉합')
    plt.subplot(1,2,2)
    plt.bar(df_pay['부서'], df_pay['연봉평균'])
    plt.title('부서별 평균')
    plt.savefig('static/images/bar.png')
    plt.close()
    # 💡 [중요 추천 - 메모리 누수 방지] plt.savefig() 이후에는 반드시 `plt.close()`를 호출해야 합니다.
    # 닫지 않으면 사용자가 새로고침을 할 때마다 서버 메모리에 그래프가 누적되어 결국 메모리 부족(OOM) 오류가 발생할 수 있습니다.
    
    # 💡 [추천 - 동시성 문제] 여러 사용자가 동시에 웹페이지에 접속할 경우, 동일한 파일('bar.png')을 덮어쓰게 되어
    # 엉뚱한 사람의 차트가 보이거나 파일 락(Lock) 에러가 날 수 있습니다.
    # 파일명에 타임스탬프/uuid를 붙이거나, 파일을 저장하지 않고 BytesIO를 이용해 이미지를 메모리에서 바로 base64로 HTML에 넘겨주는 방식이 더 좋습니다.


    plt.figure()
    plt.subplot(1,2,1)
    # 💡 [참고] 문제 4번에서 요구한 "빈도표"는 일반적으로 표 형태(Crosstab이나 Frequency Table)를 의미합니다.
    # 히스토그램도 좋지만, `pd.crosstab(df['성별'], df['직급'])` 등을 사용해 구한 표를
    # `.to_html()`을 통해 넘겨주는 것이 출제 의도("빈도표 출력")에 더 맞을 가능성이 높습니다.
    plt.hist(df['성별'])
    plt.title('성별 분포')
    plt.subplot(1,2,2)
    plt.hist(df['직급'])
    plt.title('직급 분포')
    plt.savefig('static/images/hist.png')
    plt.close()
    # 💡 [중요 추천] 여기에도 역시 `plt.close()` 추가를 적극 권장합니다.

    ctab = pd.crosstab(df['성별'], df['직급'], margins=True).to_html()

    plt.figure()
    plt.subplot(1,2,1)
    sns.countplot(data=df, x='직급', hue='성별')
    plt.title('직급별 성별 분포')
    plt.subplot(1,2,2)
    sns.countplot(data=df, x='성별', hue='직급')
    plt.title('성별 직급 분포')
    plt.savefig('static/images/countplot.png')
    plt.close()

    # 부서별 최고 연봉자 1명씩 출력
    df_payking = df.groupby('부서')['연봉'].agg(['max']).reset_index().to_html(index=False)


    dept_count = df.groupby('부서명').size()
    total = len(df)
    dept_ratio = (dept_count / total * 100).round(2)
    ratio = pd.DataFrame({
        '부서명':dept_ratio.index, 
        '비율':dept_ratio.values
        })


    return render_template('listshow.html', data=df1, paydata=paydata, ctabdata=ctab, payking=df_payking, ratio=ratio.to_html())

if __name__ == '__main__':
    app.run(debug=True)