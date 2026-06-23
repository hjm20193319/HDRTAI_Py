# 선형 리스트(Linear List)
# : 데이터를 연속적인 메모리 공간에 순서대로 저장하는 자료구조

# 놀이공원, 공연장 줄서기 등등

################################
# 연습 1 - python 함수 사용
line = ['철수', '영희', '민수']
print('현재 줄 상태 : ', line)
print('\n')

# 데이터 접근 - 인덱스를 사용 (빠름)
print('맨 앞 사람 : ', line[0])     # [문법] 리스트[인덱스]: 특정 위치의 요소에 접근 (O(1))
print('두번째 사람 : ', line[1])
print('맨 뒤 사람 : ', line[-1])
print('\n')

# 새치기 (삽입)
line.insert(2, '지수')      # [문법] insert(index, value): 특정 인덱스에 데이터를 삽입하며 이후 요소들은 뒤로 밀려남
print('새치기 후 현재 줄 상태 : ', line)
print('\n')

# 줄에서 빠지기 (삭제)
line.remove('영희')     # [문법] remove(value): 리스트에서 특정 값을 찾아 삭제하며 이후 요소들은 앞으로 당겨짐
print('줄에서 빠진 후 현재 줄 상태 : ', line)
print('\n')

# 앞사람 부터 놀이기구 타기 - 첫번째 자료부터 빠져나감. 이후 자료는 앞으로 이동
first_person = line.pop(0)  # pop(0) : 왼쪽 값 추출, pop() : 오른쪽 값 추출
print('첫번째 사람 : ', first_person)
print('줄에서 빠진 후 현재 줄 상태 : ', line)
print('\n')

# 현재 남은 사람 번호와 함께 출력
for i, p in enumerate(line):    # [문법] enumerate(iterable): 인덱스와 요소를 동시에 반환함
    print(i, '번째 사람 : ', p)
print('**' * 10)

##################################
# 연습 2 - python 코드를 사용
line = ['철수', '영희', '민수']
print('현재 줄 상태 : ', line)
print('\n')

# 데이터 접근 - 인덱스를 사용 (빠름)
print('맨 앞 사람 : ', line[0])
print('두번째 사람 : ', line[1])
print('맨 뒤 사람 : ', line[-1])
print('\n')

# 새치기 (삽입)
# '지수'를 '민수' 앞에 끼워 넣기
# → index 2 위치에 지수를 삽입 (공간 확보) ⇨ index 2 이후 뒤로 한 칸씩 이동 ⇨ 값 대입 
line.append(None) # [문법] append(value): 리스트의 맨 끝에 새로운 공간을 추가함
for i in range(len(line)-1, 2, -1):
    line[i] = line[i-1]     # 민수를 맨 뒤에 하나 더 만듦
    line[i-1] = None        # 기존 민수 자리 빈 자리로 만듦
line[2] = '지수'            # 빈 자리에 '지수' 삽입
print('새치기 후 현재 줄 상태 : ', line)
print('\n')

# 줄에서 빠지기 (삭제)
# 대기하던 '영희' 줄 서기 포기
# ↪ 영희의 위치를 찾고 그 뒤 요소들을 앞으로 이동
remove_index = None
for i in range(len(line)):
    if line[i] == '영희':
        remove_index = i    # 영희 index 검색
        break
# 앞으로 한 칸씩 이동
for i in range(remove_index, len(line)-1):
    line[i] = line[i+1]
    line[i+1] = None    # 빈 자리로 만듦 → 굳이 안해도 되긴 함(어차피 삭제할 예정) 
line.pop()
print('줄에서 빠진 후 현재 줄 상태 : ', line)
print('\n')

# 앞 사람 한명 놀이기구 탑승
# ↪ 앞에서 부터 한 칸씩 좌측으로 이동
first_person = line[0]
for i in range(len(line) - 1):
    line[i] = line[i+1]     # 앞 자리 사람을 뒷 자리 사람으로 대체 → 맨 앞은 없어짐
    line[i+1] = None
line.pop()
print('첫번째 사람 : ', first_person)
print('줄에서 빠진 후 현재 줄 상태 : ', line)
print('\n')

# 선형 리스트는 index로 즉시 접근 가능 (검색 빠름)
# 삽입/삭제 시 데이터 이동 발생(비용 발생, 속도 ⇊) ⇨ 비효율적
# [추천] 데이터의 삽입과 삭제가 빈번한 경우에는 연결 리스트(Linked List) 사용을 권장함