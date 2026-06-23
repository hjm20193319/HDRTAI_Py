# Tutle 사용해서 그래픽  처리 >> 외부 모듈

from turtle import *

p = Pen()
p.color('red', 'yellow')
p.begin_fill()

while True:
    p.forward(200)
    p.left(170)
    if abs(p.pos()) < 1:
        break

p.end_fill()
input()