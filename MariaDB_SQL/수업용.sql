CREATE TABLE dept(NO INT PRIMARY KEY, NAME VARCHAR(10), tel VARCHAR(15), inwon INT, addr TEXT) CHARSET=UTF8;  -- 테이블 생성

-- 자료 추가

# insert into 테이블 명 (칼럼명....) values(입력자료,....)
INSERT INTO dept(NO, NAME, tel, inwon, addr) VALUES(1, '인사과', '111-1111', 3, '삼성동12');
INSERT INTO dept VALUES(2, '영업과', '111-2222', 5, '서초동12');
INSERT INTO dept(NO, NAME) VALUES (3, '자재과');
INSERT INTO dept(NO, addr, tel, NAME) VALUES (4, '역삼2동 33', '111-5555', '자재2과');

INSERT INTO dept VALUES(5, '판매과');  -- err : 입력자료와 칼럼 개수 불일치
INSERT INTO dept(NAME, tel) VALUES('판매과2', '111-6666');  -- err : NO 는 P. k 생략 불가
INSERT INTO dept(NO, NAME) VALUES(5, '판매과부서는 사람들이 좋아 일하기 좋은 우수한 부서임'); -- 10자리로 최대값 설정해서 에러 : 자리수 넘침

SELECT * FROM dept;


-- 자료 수정
-- update 테이블명 set 수정칼럼명 = 수정값, .... where 조건 <-- 수정 대신 칼럼을 지정
-- where 조건이 정말 중요
-- 조건을 지정 안하면 모두가 다 수정 됨
SELECT * FROM dept WHERE NO = 1;
UPDATE dept SET tel = '123-4567' WHERE NO = 2;  -- P.K 칼럼의 자료는 수정대상에서 제외
UPDATE dept SET addr = '압구정동33', inwon = 7, tel = '777-8888' WHERE NO = 3;


-- 자료 삭제
-- delete from 테이블명 whrere 조건   -- 전체 또는 부분적 레코드 삭제 가능
-- truncate table 테이블명    -- where 조건을 사용X, 전체 레코드 삭제 가능__ 자주 안씀
DELETE FROM dept 		-- 모두 지우기
DELETE FROM dept WHERE NAME = '자재2과';
truncate table dept;  -- 전체 삭제(많은 양의 레코드를 한번에 지우고 싶을 때 >> 속도가 더 빠름)

DROP TABLE dept;			-- 테이블 자체 제거 : 구조, 자료

SELECT * FROM dept;			-- 테이블 보기


-- 무결성 제약조건 : 테이블 생성시 잘못된 자료 입력을 막고자 다양한 입력 제한 조건을 줄 수 있다

-- 1) 기본키 제약 : primary key(pk) 사용, 중복 레코드 입력 방지
CREATE TABLE aa(bun INT PRIMARY KEY, irum CHAR(10));   -- bun : MOT NULL, UNIQUE  반드시 입력해야하고 중복 불가
SELECT * FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_NAME = 'aa';
INSERT INTO aa VALUES(1, 'tom');
INSERT INTO aa VALUES(2, 'tom');			-- 이름은 중복 가능,pk가 아니기 때문에
INSERT INTO aa VALUES(2, 'tom');			-- err : pk error
INSERT INTO aa(irum) VALUES('tom');    -- err : pk가 입력이 안된 상태이기 때문에
INSERT INTO aa(bun) VALUES(3);			-- 에러 없음, NULL 허용
SELECT * FROM aa;
DROP TABLE aa;
-- 다르게 작성 방법
CREATE TABLE aa(bun INT, irum CHAR(10), CONSTRAINT aa_bun_pk PRIMARY KEY(bun)); -- 이름을 명시적으로 지정해줌
INSERT INTO aa VALUES(1, 'tom');
SELECT * FROM aa;
DROP TABLE aa;

-- 2) check 제약 : 입력 자료의 특정 칼럼값 조건 검사
CREATE TABLE aa(bun INT, nai INT CHECK(nai >= 20));		-- 다른 언어에서 확인을 한 후에 최종 확인 단계
INSERT INTO aa VALUES(1, 23);
INSERT INTO aa VALUES(2, 13);			-- err : 입력 값 조건 미충족
SELECT * FROM aa;
DROP TABLE aa;

-- 3) unique 제약 : 특정 칼럼값 중복 불허
CREATE TABLE aa(bun INT, irum CHAR(10) NOT NULL UNIQUE);
INSERT INTO aa VALUES(1, 'tom');
INSERT INTO aa VALUES(2, 'john');
INSERT INTO aa VALUES(3, 'john');			-- err : unique 제약 조건에 걸림
SELECT * FROM aa;
DROP TABLE aa;

-- 4) : foreign key(fk) : 외부키, 참조키 제약, 툭정 칼럼이 다른 테이블의 칼럼을 참조
-- fk 대상은 pk 다!!! (unique 해야 되기 때문에)
CREATE TABLE jikwon(bun INT PRIMARY KEY, irum VARCHAR(10) NOT NULL, buser CHAR(10) NOT NULL);
INSERT INTO jikwon VALUES(1, '한송이', '인사과');
INSERT INTO jikwon VALUES(2, '이기자', '인사과');
INSERT INTO jikwon VALUES(3, '한송이', '판매과');
SELECT * FROM jikwon;

CREATE TABLE gajok(CODE INT PRIMARY KEY, NAME VARCHAR(10) NOT NULL, birth DATETIME, jikwonbun INT, FOREIGN KEY(jikwonbun) REFERENCES jikwon(bun));
 				-- fk 와 pk가 칼럼명은 달라도 타입은 같아야 한다
INSERT INTO gajok VALUES(10, '한가해', '2015-05-12', 3);
INSERT INTO gajok VALUES(20, '공기밥', '2011-12-12', 2);
INSERT INTO gajok VALUES(30, '김밥', '2013-12-12', 5);  -- err : 참조 대상 행이 없어서 error
INSERT INTO gajok VALUES(30, '심심해', '2010-05-12', 3);		-- 같은걸 참조해도 되는건가...?

DELETE FROM jikwon WHERE bun = 1;
DELETE FROM jikwon WHERE bun = 2;		-- err : 참조가 되어 있는 자료가 살아 있어서 지울 수 없다
DROP TABLE jikwon;		-- err : 위와 같은 이유로 error

DELETE FROM gajok WHERE jikwonbun = 2;		-- 1) 참조키(pk가 2번) 삭제 (가족자료)
DELETE FROM jikwon WHERE bun = 2;			-- 2) 참조가 되어 지던게 없으므로  직원 자료도 삭제가 가능하다

SELECT * FROM gajok;
SELECT * FROM jikwon;

DROP TABLE gajok;			-- 이 순서로 지워야 함
DROP TABLE jikwon;
-- 참고
-- create table gajok (----------) on delete cascade  # 테이블을 만들면서 옵션을 걸어줌(위험한 옵션)
-- 직원 자료를 삭제하면 관련 있는 가족자료 함께 삭제 가능 -> 프로그램으로 짜는게 더 좋다


-- default : 특정 칼럼에 초기치 부여 => NULL 예방 
CREATE TABLE aa(bun INT AUTO_INCREMENT PRIMARY KEY, juso CHAR(20) DEFAULT '강남구 역삼동');
					-- auto_increment : bun 자동 증가 		==>  게시판이나 방명록 만들 떄 사용하면 좋음
-- 만약에 SQL사용하는 회사가 달라서 문법이  다를 것 같으면 프로그램으로 짜면 해결된다
INSERT INTO aa VALUES(1, '서초구 서초2동');
INSERT INTO aa(juso) VALUES('서초구 서초3동');
INSERT INTO aa(juso) VALUES('서초구 서초4동');
INSERT INTO aa(bun) VALUES(5);		-- 초기값 자동 입력
INSERT INTO aa(bun) VALUES(6);
SELECT * FROM aa;

DROP TABLE aa;

-- 연습 문제
CREATE TABLE 교수(교수코드 INT PRIMARY KEY, 교수명 VARCHAR(10), 연구실번호 INT CHECK(연구실번호 >= 100 AND 연구실번호  <= 500));
CREATE TABLE 과목(과목코드 INT auto_increment PRIMARY KEY, 과목명 VARCHAR(15) UNIQUE, 교재명 VARCHAR(20), 담당교수 INT, FOREIGN KEY(담당교수) REFERENCES 교수(교수코드));
CREATE TABLE 학생(학번 INT PRIMARY KEY, 학생명 VARCHAR(10), 수강과목 INT, FOREIGN KEY(수강과목) REFERENCES 과목(과목코드), 학년번호 INT DEFAULT 1 CHECK(학년번호 >= 1 AND 학년번호 <= 4));
CREATE TABLE 학생(학번 INT PRIMARY KEY, 학생명 VARCHAR(10), 수강과목 INT, FOREIGN KEY(수강과목) REFERENCES 과목(과목코드), 학년번호 INT CHECK(학년번호 >= 1 AND 학년번호 <= 4) DEFAULT 1);

INSERT INTO 교수 VALUES(1, '가나다', 111);
INSERT INTO 교수 VALUES(2, '라마바', 222);
INSERT INTO 교수 VALUES(3, '사아자', 333);

INSERT INTO 과목 VALUES(1, '수학', '수학책', 1);
INSERT INTO 과목(과목명, 교재명, 담당교수) VALUES('과학', '과학책', 3);
INSERT INTO 과목(과목명, 교재명, 담당교수) VALUES('미술', '미술책', 1);

INSERT INTO 학생 VALUES(1, '김가나', 1, 2); 
INSERT INTO 학생(학번, 학생명, 수강과목) VALUES(2, '김다라', 1);
INSERT INTO 학생 VALUES(3, '김마바', 3, 4);


SELECT * FROM 교수
SELECT * FROM 과목
SELECT * FROM 학생


DROP TABLE 학생;
DROP TABLE 과목;
DROP TABLE 교수;


-- index 색인 : 검색 속도 향상을 위해 특정 칼럼에 대하 색인 부여 가능
-- pk 칼럼은 자동으로 인덱싱 됨(ascending sort 오름차순 정렬)
-- index를 자제해야하는 경우 : 입력, 수정, 삭제 등의 작업이 빈번한 경우

CREATE TABLE aa(bun INT PRIMARY KEY, irum VARCHAR(10) NOT NULL, juso VARCHAR(50));
INSERT INTO aa VALUES(1, '신선해', '테헤란로111');
ALTER TABLE aa ADD INDEX ind_juso(juso);		-- juso 칼럼에 인덱스 부여
SELECT * FROM aa;
EXPLAIN SELECT * FROM aa;
DESC aa;
SHOW INDEX FROM aa;
ALTER TABLE aa DROP INDEX ind_juso;			-- 없애기
DROP TABLE aa;


-- 테이블 관련 주요 명령
-- create table 테이블 명
-- alter table 테이블 명
-- drop table 테이블 명
CREATE TABLE aa(bun INT PRIMARY KEY, irum VARCHAR(10), juso VARCHAR(50));
INSERT INTO aa VALUES (1, 'tom', 'seoul');
SELECT * FROM aa;

ALTER TABLE aa RENAME kbs;			-- 공유되어서 사용되는 테이블은 이름을 바꾸지 않음
SELECT * FROM aa;  -- 원래는 test.aa 가 맞지만, 보통은 그 데이터베이스 안에서 작업하기 때문에 생략해도 됨
SELECT * FROM kbs;
ALTER TABLE kbs RENAME aa;


-- 칼럼 관련 명령
ALTER TABLE aa ADD (job_id INT DEFAULT 10);		-- 칼럼 추가
ALTER TABLE aa CHANGE job_id job_num INT;			-- 칼럼 수정(이름이나 성격 변경)
ALTER TABLE aa MODIFY job_num VARCHAR(10);		-- 칼럼 성격 변경  --> 구조 변경은 거의 없음
DESC aa;
ALTER TABLE aa DROP COLUMN job_num;					-- 칼럼 삭제
DESC aa;
DROP TABLE aa;
-- --------------------------------------------------------------------------------------------------------------------




CREATE TABLE customers(cno INT PRIMARY KEY, cname CHAR(10), caddress VARCHAR(50), cemail CHAR(20), cphone VARCHAR(20));
CREATE TABLE orders(ono INT PRIMARY KEY, odate DATETIME, oaddress VARCHAR(50), ophone VARCHAR(20), ostatus VARCHAR(10), ono_cus INT, FOREIGN KEY(ono_cus) REFERENCES customers(cno));










