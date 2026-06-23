import sys

sys.stdout.reconfigure(encoding = 'utf-8')

import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8') 
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

ss = '파이썬 자료 출력'
ss2 = 123 + 5
# print(ss)     --> 개발자가 자신의 컴 표준 출력 장치로 값 확인용


# 변수를 외부로 출력하고 싶다면??
# 클라이언트 브라우저로 출력
print('Content-Type:text/html; charset=utf-8')
print()
print('<html><body>')
print('<b>안녕. 파이썬 모듈로 작성한 문서야</b><br/>')
print('파이썬 변수 값 : %s'%(ss, ))     # 튜플로 줘야 함
print('<br/>파이썬 변수 값2 : %d'%(ss2, ))
print('</body></html>')