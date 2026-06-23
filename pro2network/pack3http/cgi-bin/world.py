import sys

sys.stdout.reconfigure(encoding = 'utf-8')          # 한글 파일이 깨질때 입력하는 방법

s1 = '자료1'
s2 = '두번째 자료'

print('Content-Type:text/html; charset=utf-8')

# 아래와 같이 작성할 수도 있다

print("""
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>world</title>
</head>
<body>
    <h1>world 페이지</h1>
    자료 출력 : {0}, {1}
    <br/>
    <img src = "../images/supra.jpg" />
    <br/>
    <a href = "../index.html">메인으로</a>
</body>
</html>
""".format(s1, s2))