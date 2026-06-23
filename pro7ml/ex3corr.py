# "국적별 관광지 방문 데이터를 활용한 장소 간 연관성 분석 실습"

# 외국인(미국,일본,중국) 국내 관광지(5개) 방문 관련자료 사용
# 나라별 관광지 상관관계 확인하기

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 산점도 그리기
def setScatterGraph(tour_table, all_table, tourpoint):
    # print(tourpoint)
    # 계산할 관광지명에 해당하는 자료만 뽑아 tour에 저장하고 외국인 자료와 병합
    tour = tour_table[tour_table['resNm'] == tourpoint]
    merge_table = pd.merge(tour, all_table, left_index=True, right_index=True)
    # print('merge_table : \n', merge_table)
    
    # 시각화 - 상관계수
    fig = plt.figure()
    fig.suptitle(tourpoint + ' 상관관계 분석')

    # 중국인
    plt.subplot(1, 3, 1)
    plt.xlabel('중국인 방문수')
    plt.ylabel('외국인 입장객 수')
    
    lamb1 = lambda p:merge_table['중국인'].corr(merge_table['ForNum'])
    r1 = lamb1(merge_table)
    # print('r1 : ', r1)
    # r1 :  -0.05879110406006314
    # r1 :  0.44594488384450376
    # r1 :  0.5256734293511215
    # r1 :  0.4512325398089607
    # r1 :  -0.5834218986767473

    plt.title('r={:.5f}'.format(r1))
    plt.scatter(merge_table['중국인'], merge_table['ForNum'], alpha=0.7, s=6, c='red')
    
    # 일본인
    plt.subplot(1, 3, 2)
    plt.xlabel('일본인 방문수')
    plt.ylabel('외국인 입장객 수')
    
    lamb2 = lambda p:merge_table['일본인'].corr(merge_table['ForNum'])
    r2 = lamb2(merge_table)
    
    plt.title('r={:.5f}'.format(r2))
    plt.scatter(merge_table['일본인'], merge_table['ForNum'], alpha=0.7, s=6, c='green')
    
    # 미국인
    plt.subplot(1, 3, 3)
    plt.xlabel('미국인 방문수')
    plt.ylabel('외국인 입장객 수')
    
    lamb3 = lambda p:merge_table['미국인'].corr(merge_table['ForNum'])
    r3 = lamb3(merge_table)

    plt.title('r={:.5f}'.format(r3))
    plt.scatter(merge_table['미국인'], merge_table['ForNum'], alpha=0.7, s=6, c='blue')
    
    plt.tight_layout()
    plt.show()

    return [tourpoint, r1, r2, r3]

def processFunc():
    # 서울시 관광지 정보 파일
    fname = "서울특별시_관광지입장정보_2011_2016.json"
    jsonTP = json.loads(open(fname, 'r', encoding='utf-8').read())
    tour_table = pd.DataFrame(jsonTP, columns=('yyyymm', 'resNm', 'ForNum'))    # 년 월, 관광지 명, 입장객 수
    tour_table = tour_table.set_index('yyyymm')
    # print(tour_table)

    resNm = tour_table.resNm.unique()
    print('resNm : ', resNm[:5])
    # resNm :  ['창덕궁' '운현궁' '경복궁' '창경궁' '종묘']

    # 중국인 관광지 정보 파일 DataFrame에 저장
    cdf = "중국인방문객.json"
    jdata = json.loads(open(cdf, 'r', encoding='utf-8').read())
    china_table = pd.DataFrame(jdata, columns=('yyyymm', 'visit_cnt'))
    china_table = china_table.rename(columns={'visit_cnt':'중국인'})
    china_table = china_table.set_index('yyyymm')
    print(china_table[:2])


    # 일본인 관광지 정보 파일 DataFrame에 저장
    jdf = "일본인방문객.json"
    jdata = json.loads(open(jdf, 'r', encoding='utf-8').read())
    japan_table = pd.DataFrame(jdata, columns=('yyyymm', 'visit_cnt'))
    japan_table = japan_table.rename(columns={'visit_cnt':'일본인'})
    japan_table = japan_table.set_index('yyyymm')
    print(japan_table[:2])

    # 미국인 관광지 정보 파일 DataFrame에 저장
    udf = "미국인방문객.json"
    jdata = json.loads(open(udf, 'r', encoding='utf-8').read())
    usa_table = pd.DataFrame(jdata, columns=('yyyymm', 'visit_cnt'))
    usa_table = usa_table.rename(columns={'visit_cnt':'미국인'})
    usa_table = usa_table.set_index('yyyymm')
    print(usa_table[:2])

    all_table = pd. merge(china_table, japan_table, left_index=True, right_index=True)
    all_table = pd. merge(all_table, usa_table, left_index=True, right_index=True)
    print(all_table)    # [72 rows x 3 columns]

    # 상관계수
    r_list = []
    for tourpoint in resNm[:5]:
        r_list.append(setScatterGraph(tour_table, all_table, tourpoint))

    # print(r_list)
    r_df = pd.DataFrame(r_list, columns=('고궁명', '중국', '일본', '미국'))
    print(r_df)

    r_df.plot(kind='bar', rot=50)
    plt.show()

if __name__ == "__main__":
    processFunc()