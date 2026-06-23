import re   # 정규표현식 지원 모듈 로딩

ss = "1234 abc가나다abcABC_123555집에가나요_6'Python is fun'"
print(ss)
print(re.findall(r'123', ss))     # 정규표현식에서는 r을 선행할 것
#  findall 의 return type은 list 형식이다
print(re.findall(r'가나', ss))
print(re.findall(r'[0-9]', ss))   # 숫자만 뽑고 싶을 때
print(re.findall(r'[0-9]+', ss))    #  1개 이상 붙여서 출력-------   *는 0개 이상 --------  {숫자}는 숫자만큼 붙여서
print(re.findall(r'[0-9]{2,3}', ss))
print(re.findall(r'[a-zA-Z]+', ss))
print(re.findall(r'[가-힣]+', ss))
print(re.findall(r'\d+', ss))
print(re.findall(r'\D+', ss))