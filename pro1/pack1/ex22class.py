# 클래스는 새로운 타입을 만들어 자원을 공유 가능
'''
class Singer:
    title_song = '빛나라 대한민국'

    def sing(self):
        msg = '노래는 '
        print(msg, self.title_song)
'''     

# import ex22singer     별도의 모듈을 import  >> ex22singer.Singer 해줘야 해서 귀찮음
from ex22singer import Singer           # 이게 더 간단할수도 모듈의 Singer 클래스 바로 import

bts = Singer()      # 생성자 호출 / 객체 생성 후 주소 치환 / 생성자는 안줌, 초기화 할거 없었음 
bts.sing()
print(type(bts))        # Singer type 임

bts.title_song = 'Permission to Dance'          # bts의 title_song 이 바뀐 것이다!!!
bts.sing()
bts.co = 'Big Hit Ent'              # bts 저장공간에 co 멤버 추가 / co 는 bts만 갖고 있는 것
print('소속사 : ', bts.co)
print()

ive = Singer()
ive.sing()
print(type(ive))            # Singer type 이다, ive 에게는 co 가 없다

Singer.title_song = '아 대한민국'       # 원형 클래스를 바꿈
bts.sing()
ive.sing()                          # ive 는 title_song이 없기 때문에 원형을 참고한다

print('\n-----------')

niceGroup = ive         # 주소를 치환해줌 / 이제부터 둘은 같은 것
niceGroup.sing()


