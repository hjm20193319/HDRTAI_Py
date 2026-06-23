-- 아래 자료는 실습을 위해 가상으로 만들어진 자료임을 밝힙니다.

-- SANGDATA TABLE
create table sangdata(
code int primary key,
sang varchar(20),
su int,
dan INT);                  --   참고 : 한글이 깨질 경우 ... dan int)charset=utf8;

insert into sangdata values(1,'장갑',3,10000);
insert into sangdata values(2,'벙어리장갑',2,12000);
insert into sangdata values(3,'가죽장갑',10,50000);
insert into sangdata values(4,'가죽점퍼',5,650000);

-- BUSER TABLE
create table buser(
buserno int primary key, 
busername varchar(10) not null,
buserloc varchar(10),
busertel varchar(15));

insert into buser values(10,'총무부','서울','02-100-1111');
insert into buser values(20,'영업부','서울','02-100-2222');
insert into buser values(30,'전산부','서울','02-100-3333');
insert into buser values(40,'관리부','인천','032-200-4444');

-- JIKWON TABLE
create table jikwon(
jikwonno int primary key,
jikwonname varchar(10) not null,
busernum int not NULL,			-- buser table의 buserno(pk)를 참조하는 foreign key 같은 역할임 / 공통 칼럼 ---> 구속력이 약하다(부서가 없는 직원이 있을 수 있기 때문에)
jikwonjik varchar(10) default '사원', 
jikwonpay int,
jikwonibsail date,
jikwongen varchar(4),
jikwonrating char(3),
CONSTRAINT ck_jikwongen check(jikwongen='남' or jikwongen='여'));

insert into jikwon values(1,'홍길동',10,'이사',9900,'2008-09-01','남','a');
insert into jikwon values(2,'한송이',20,'부장',8800,'2010-01-03','여','b');
insert into jikwon values(3,'이순신',20,'과장',7900,'2010-03-03','남','b');
insert into jikwon values(4,'이미라',30,'대리',4500,'2014-01-04','여','b');
insert into jikwon values(5,'이순라',20,'사원',3000,'2017-08-05','여','b');
insert into jikwon values(6,'김이화',20,'사원',2950,'2019-08-05','여','c');
insert into jikwon values(7,'김부만',40,'부장',8600,'2009-01-05','남','a');
insert into jikwon values(8,'김기만',20,'과장',7800,'2011-01-03','남','a');
insert into jikwon values(9,'채송화',30,'대리',5000,'2013-03-02','여','a');
insert into jikwon values(10,'박치기',10,'사원',3700,'2016-11-02','남','a');
insert into jikwon values(11,'김부해',30,'사원',3900,'2016-03-06','남','a');
insert into jikwon values(12,'박별나',40,'과장',7200,'2011-03-05','여','b');
insert into jikwon values(13,'박명화',10,'대리',4900,'2013-05-11','남','a');
insert into jikwon values(14,'박궁화',40,'사원',3400,'2016-01-15','여','b');
insert into jikwon values(15,'채미리',20,'사원',4000,'2016-11-03','여','a');
insert into jikwon values(16,'이유가',20,'사원',3000,'2016-02-01','여','c');
insert into jikwon values(17,'한국인',10,'부장',8000,'2006-01-13','남','c');
insert into jikwon values(18,'이순기',30,'과장',7800,'2011-11-03','남','a');
insert into jikwon values(19,'이유라',30,'대리',5500,'2014-03-04','여','a');
insert into jikwon values(20,'김유라',20,'사원',2900,'2019-12-05','여','b');
insert into jikwon values(21,'장비',20,'사원',2950,'2019-08-05','남','b');
insert into jikwon values(22,'김기욱',40,'대리',5850,'2013-02-05','남','a');
insert into jikwon values(23,'김기만',30,'과장',6600,'2015-01-09','남','a');
insert into jikwon values(24,'유비',20,'대리',4500,'2014-03-02','남','b');
insert into jikwon values(25,'박혁기',10,'사원',3800,'2016-11-02','남','a');
insert into jikwon values(26,'김나라',10,'사원',3500,'2016-06-06','남','b');
insert into jikwon values(27,'박하나',20,'과장',5900,'2012-06-05','여','c');
insert into jikwon values(28,'박명화',20,'대리',5200,'2013-06-01','여','a');
insert into jikwon values(29,'박가희',10,'사원',4100,'2016-08-05','여','a');
insert into jikwon values(30,'최미숙',30,'사원',4000,'2015-08-03','여','b');

-- GOGEK TABLE
create table gogek(
gogekno int primary key,
gogekname varchar(10) not null,
gogektel varchar(20),
gogekjumin char(14),
gogekdamsano INT,			-- foreign key 걸어줌
CONSTRAINT FK_gogekdamsano foreign key(gogekdamsano) references jikwon(jikwonno));		-- pk를 참조하고 있는 fk --> 직접 걸어줬기 때문에 구속력이 강하다(담당 직원이 없는 고객이 없기 때문에)

insert into gogek values(1,'이나라','02-535-2580','850612-1156777',5);
insert into gogek values(2,'김혜순','02-375-6946','700101-1054777',3);
insert into gogek values(3,'최부자','02-692-8926','890305-1065777',3);
insert into gogek values(4,'김해자','032-393-6277','770412-2028777',13);
insert into gogek values(5,'차일호','02-294-2946','790509-1062777',2);
insert into gogek values(6,'박상운','032-631-1204','790623-1023777',6);
insert into gogek values(7,'이분','02-546-2372','880323-2558777',2);
insert into gogek values(8,'신영래','031-948-0283','790908-1063777',5);
insert into gogek values(9,'장도리','02-496-1204','870206-2063777',4);
insert into gogek values(10,'강나루','032-341-2867','780301-1070777',12);
insert into gogek values(11,'이영희','02-195-1764','810103-2070777',3);
insert into gogek values(12,'이소리','02-296-1066','810609-2046777',9);
insert into gogek values(13,'배용중','02-691-7692','820920-1052777',1);
insert into gogek values(14,'김현주','031-167-1884','800128-2062777',11);
insert into gogek values(15,'송운하','02-887-9344','830301-2013777',2);


create table board(
num int primary key,
author varchar(10),
title varchar(50),
content varchar(4000),
bwrite date,
readcnt int default 0);

insert into board(num,author,title,content,bwrite) values(1,'홍길동','연습','연습내용',now());



--  ------------------------------------------------
-- 1) 앨범 테이블
CREATE TABLE albums (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2) 사진 테이블
CREATE TABLE photos (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  album_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX (album_id),
  FOREIGN KEY (album_id) REFERENCES albums(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


SELECT * FROM sangdata;
SELECT * FROM buser;
SELECT * FROM jikwon;
SELECT * FROM gogek;
SELECT * FROM board;


-- ---------------실습 내용-----------------------------------------------------------

DESC sangdata;
DESC buser;
DESC jikwon;
DESC gogek;

-- select : db 서버로부터 클라이언트로 ***자료를 읽는 명령***
-- select 칼럼명 as 별명, ...from 테이블명 where 조건  order by 기준키,...
SELECT * FROM jikwon;		-- 모든 칼럼 읽기
SELECT jikwonno, jikwonname FROM jikwon;		-- selection : 특정 칼럼만 읽기 , projection : 원하는 레코드만 읽기
SELECT jikwonno, jikwongen, busernum, jikwonname FROM jikwon;  -- 순서 선택 가능
SELECT jikwonno AS 직원번호, jikwonname AS 직원명 FROM jikwon;		-- 별명 지정 가능  --->  칼럼의 이름이 바뀜
SELECT 10, '안녕', 12 / 3 as 결과 FROM DUAL;		-- 가상의 테이블을 만듦 DB서버에서 한 작업 아님! / 수식은 계산 됨
SELECT jikwonname, jikwonpay, jikwonpay * 0.05 as tax FROM jikwon;		-- 연산에 의해서 램에 기존 칼럼을 가공해서 칼럼 생성 가능
SELECT jikwonname, CONCAT(jikwonname, '님') AS jikwonetc FROM jikwon;		-- 기존 칼럼 가공 /  CONCAT : 문자열 더하기 함수 



-- 정렬 SORT 
SELECT * FROM jikwon ORDER BY jikwonpay ASC;		-- 칼럼명 직접 작성하는 것이 원칙, 계산속도가 더 빠름 / jikwonpay를 기준으로 오름차순 정렬
SELECT * FROM jikwon ORDER BY jikwonpay;			-- 오름차순은 생략가능(기본값)
SELECT * FROM jikwon ORDER BY jikwonpay DESC;	-- 내림차순 DESC
SELECT * FROM jikwon ORDER BY jikwonjik ASC;		-- 문자열은 사전식으로 정렬
SELECT * FROM jikwon ORDER BY jikwonjik ASC, busernum DESC, jikwongen ASC, jikwonpay ASC;		-- 1,2,3,4차키 부여 : 직원 직급별 > 부서별 > 성별 > 급여별 순으로 분류 가능
SELECT jikwonname, jikwonpay, jikwonpay / 100 * 100 AS pay FROM jikwon ORDER BY pay DESC;

SELECT distinct jikwonjik FROM jikwon;		-- distinct 중복 배제 : 칼럼 데이터의 종류를 알고 싶을 때
SELECT DISTINCT jikwonjik, jikwonname FROM jikwon; -- 불가!


-- 연산자 : () > 산술 > 관계(비교) > is null, like, in > between, not > and > or
SELECT * FROM jikwon WHERE jikwonjik = '대리';		-- 레코드 선택 가능
SELECT * FROM jikwon WHERE jikwonno = 3;
SELECT * FROM jikwon WHERE jikwonibsail = '2010-03-03';
SELECT * FROM jikwon WHERE jikwonno = 5 OR jikwonno = 7;
SELECT * FROM jikwon WHERE jikwonjik = '사원' AND jikwongen = '여' AND jikwonpay <= 3000;		-- 여러 조건을 동시에 만족시키는 레코드 값을 선택할 수 있음
SELECT * FROM jikwon WHERE jikwonjik = '사원' AND (jikwongen = '여' OR jikwonibsail >= '2017-01-01');

SELECT * FROM jikwon WHERE jikwonno >= 5 AND jikwonno <= 10;
SELECT * FROM jikwon WHERE jikwonno BETWEEN 5 AND 10;			-- 위와 같은 결과
SELECT * FROM jikwon WHERE jikwonibsail BETWEEN '2017-1-1' AND '2019-12-31';		-- between 은 문자도 가능함
SELECT * FROM jikwon WHERE jikwonno < 5 or jikwonno > 20;		-- 긍정적 형태의 조건이 연산속도를 향상 시킴
SELECT * FROM jikwon WHERE jikwonno not BETWEEN 5 AND 20;		-- 위와 같은 결과  --> 부정적 조건은 연산속도가 떨어짐

SELECT * FROM jikwon WHERE jikwonpay > 5000;
SELECT * FROM jikwon WHERE jikwonpay > 3000 + 2000;		-- 산술이 관계보다 우선순위가 높기 때문에 위와 결과는 같다
SELECT * FROM jikwon WHERE jikwonname >= '이' ORDER BY jikwonname;
SELECT ASCII('a'), ASCII('A'), ASCII('가'), ASCII('나') FROM DUAL;
SELECT * FROM jikwon WHERE jikwonname BETWEEN '김' AND '이';			-- 이 전가지만 나옴


-- in 멤버 조건 연산
SELECT * FROM jikwon WHERE jikwonjik = '대리' OR jikwonjik = '과장' OR jikwonjik = '부장';
SELECT * FROM jikwon WHERE jikwonjik IN('대리', '과장', '부장');		-- or가 연속적으로 나올 때 in 연산자 사용 가능
SELECT * FROM jikwon WHERE jikwonno IN(3, 12, 29);


-- like 조건 연산 : %(0개 이상의 문자열), _(한개 문자)       둘 줄 하나 쓰면 됨
SELECT * FROM jikwon WHERE jikwonname LIKE '이%';		--  첫글자가 '이'로 시작하는 글자, 이후 글자는 어떤 글자도 상관 없음 
SELECT * FROM jikwon WHERE jikwonname LIKE '이순%';
SELECT * FROM jikwon WHERE jikwonname LIKE '%라';		--  앞글자는 상관 없고 마지막 글자가 '라'인 레코드
SELECT * FROM jikwon WHERE jikwonname LIKE '이%라';		-- 가운데에는 글자수 상관 없이 아무글자, 첫과 마지막만 지정

SELECT * FROM jikwon WHERE jikwonname LIKE '이__';			-- 두번째 세번째 글자는 아무거나 , 이로 시작하는 세글자짜리  / 언더바는 글자수를지정 
SELECT * FROM jikwon WHERE jikwonname LIKE '__';			-- 두글자 짜리 이름

SELECT * FROM gogek WHERE gogekjumin LIKE '_______1%'; 
SELECT * FROM gogek WHERE gogekjumin LIKE '%-1%';


-- 실습을 위한 세팅(NULL 만들기 위해)
SELECT * FROM jikwon;
UPDATE jikwon SET jikwonjik = NULL WHERE jikwonno = 5;
SELECT * FROM jikwon;

-- IS NULL
SELECT * FROM jikwon WHERE jikwonjik = NULL;			-- NULL은 이렇게 하면 안됨
SELECT * FROM jikwon WHERE jikwonjik IS NULL;		-- NULL 사용법

-- LIMIT
SELECT * FROM jikwon LIMIT 3;			-- 앞에서부터 3개만/  limit -> 개수를 제한
SELECT * FROM jikwon ORDER BY jikwonno DESC LIMIT 3;		-- 뒤에서부터 3개만
SELECT * FROM jikwon LIMIT 5,3;			-- 시작 행, 개수 (인덱스는 0번째부터)


-- 조합
SELECT jikwonno AS 직원번호, jikwonname AS 직원명, jikwonjik AS 직급, jikwonpay AS 연봉,
jikwonpay / 12 AS 보너스, jikwonibsail AS 입사일 FROM jikwon
WHERE jikwonjik IN('과장', '부장','사원')
AND jikwonpay >= 4000 AND jikwonibsail BETWEEN '2015-1-1' AND '2019-12-31'
ORDER BY jikwonjik, jikwonpay DESC LIMIT 3;



-- select 뿐만 아니라 다른 명령어에도 사용가능하다



-- 내장 함수 : 데이터 조작의 효율성 증진이 목적
-- 단일 행 함수 : 각 행에 대해 작업한다. 행 단위 처리
-- 문자 함수
SELECT LOWER ('Hello'), UPPER ('Hello') FROM DUAL;			-- 소문자 대문자
SELECT SUBSTR('hello world', 3),SUBSTR ('hello world', 3, 3), SUBSTR('hello world',-3, 3) FROM DUAL;
SELECT LENGTH('hello world'), INSTR('hello world', 'e') FROM DUAL;
SELECT REPLACE('010.111.1234','.','-') FROM DUAL;			-- 글자 바꿔줌

-- 직원 테이블에서 이름에 '이' 가 포함된 직원이 있으면 '이'부터 두글자 출력하기
SELECT jikwonname, SUBSTR(jikwonname, INSTR(jikwonname, '이'),2) FROM jikwon WHERE jikwonname LIKE '%이%';



-- 숫자 함수
SELECT ROUND(45.678, 2), ROUND(45.678), ROUND(45.678, 0), ROUND(45.678, -1) FROM DUAL;		-- 반올림 함수

SELECT jikwonname, jikwonpay, jikwonpay * 0.25 AS tax, ROUND(jikwonpay * 0.25, 0) FROM jikwon;

SELECT TRUNCATE(45.678, 0), TRUNCATE(45.678, 1), TRUNCATE(45.678, -1) FROM DUAL;		-- 버림

SELECT MOD(15, 2), 15 / 2 FROM DUAL;		-- 나머지

SELECT GREATEST(23, 25, 5, 1, 12), LEAST(23, 25, 5, 1, 12) FROM DUAL;


-- 날짜 함수
SELECT NOW(), NOW() + 2, SYSDATE(), CURDATE() FROM DUAL;		-- 값을 연산에 참여시킬 수 있다
SELECT NOW(), SLEEP(3), NOW() FROM DUAL;			-- 한 쿼리 안에서는 NOW는 동일 값을 유지( 빠져나올때 최종 NOW값)
SELECT SYSDATE(), SLEEP(3), SYSDATE() FROM DUAL;		-- SYSDATE는 실행 시점 값 출력

SELECT ADDDATE('2020-08-01',3), ADDDATE('2020-08-01',-3), SUBDATE('2020-08-01',3)FROM DUAL;		-- 날짜 더하고 빼기,, 윤년도 반영함

SELECT DATE_ADD(NOW(), INTERVAL 1 MINUTE), DATE_ADD(NOW(), INTERVAL 5 DAY), DATE_ADD(NOW(), INTERVAL 5 MONTH) FROM DUAL;		-- year 도 가능하다

SELECT DATEDIFF(NOW(), '2025-5-5') FROM DUAL;		-- 날짜 차이


-- 형 변환 함수
SELECT NOW(), DATE_FORMAT(NOW(), '%Y%m%d'), DATE_FORMAT(NOW(), '%Y년 %m월 %d일')			-- 서식을 지정하는 것  출력 모양을 바꿔주는 것

SELECT jikwonname, jikwonibsail FROM jikwon WHERE busernum = 10;
SELECT jikwonname, jikwonibsail, DATE_FORMAT(jikwonibsail, '%Y') FROM jikwon WHERE busernum = 10;

SELECT STR_TO_DATE('2026-02-12', '%Y-%m-%d') FROM DUAL;
SELECT STR_TO_DATE('2026-02-12 13:16:34', '%Y-%m-%d %H:%i:%S') FROM DUAL;


-- 기타 함수
-- RANK : 순위를 결정
SELECT jikwonno, jikwonname, jikwonpay, RANK() OVER (ORDER BY jikwonpay desc) AS result, dense_RANK() OVER (ORDER BY jikwonpay desc) as result2 FROM jikwon;			-- 동점자 누적 처리가 됨 / dense_RANK() 는 동점자 누적 처리가 안됨
-- 기본적으로는 오름차순 처리함



-- nvl(value1, value2) : value1이 NULL 이면 value2를 취함
SELECT jikwonname, jikwonjik, nvl(jikwonjik, '임시직') AS 비고 FROM jikwon;

-- nvl2(value1, value2, value3) : value1이 NULL이면 value3, 아니면 value2를 취함
SELECT jikwonname, jikwonjik, nvl2(jikwonjik, '정규직', '임시직') AS 비고 FROM jikwon;



-- NULLIF(value1, value2) : 두개의 값이 일치하면 NULL, 아니면 value1 취함
SELECT jikwonname, jikwonjik, NULLIF(jikwonjik, '대리') FROM jikwon;



-- 조건 표현식 
-- 형식 1) 
-- case 표현식 when 비교값1 then 결과값1 when 비교값2 then 결과값2 ... [else 결과값n] end as 별명
SELECT case 10 / 5 when 5 then '안녕' when 2 then '반가워' ELSE '잘가' END AS 결과 FROM DUAL;

SELECT jikwonname, jikwonpay, jikwonjik, case jikwonjik when '이사' then jikwonpay * 0.05 when '부장' then jikwonpay * 0.04 when '과장' then jikwonpay * 0.03
ELSE jikwonpay * 0.02 END AS donation FROM jikwon;  


-- 형식 2)
-- case when 조건1 then 결과값1 when 조건 2 then 결과값2 ... [else 결과값n] end as 별명
SELECT jikwonname, case when jikwongen = '남' then '남성' when jikwongen = '여' then '여성' END AS gender FROM jikwon;

SELECT jikwonname, jikwonpay, case when jikwonpay >= 7000 then '우수연봉' when jikwonpay >= 5000 then '보통연봉' ELSE '저조' END AS result, jikwongen FROM jikwon WHERE jikwonjik IN ('대리', '과장');




-- if(조건) 참값, 거짓값 as 별명
SELECT jikwonname, jikwonpay, jikwonjik, if(TRUNCATE(jikwonpay / 1000,0) >= 5, 'good', 'normal') AS result FROM jikwon;



-- 1번 연습문제 
SELECT jikwonname AS '직원명', TRUNCATE(DATEDIFF(NOW(), jikwonibsail) / 365, 0) AS '근무년수', case when TRUNCATE(DATEDIFF(NOW(), jikwonibsail) / 365, 0) >= 10 then '감사합니다' ELSE '열심히' END AS '표현(10년 기준)', case when TRUNCATE(DATEDIFF(NOW(), jikwonibsail) / 365, 0) >= 10 then jikwonpay * 0.05 ELSE jikwonpay * 0.03 END AS '특별수당', jikwonibsail AS '입사일 확인용' FROM jikwon WHERE jikwonibsail >= '2010-01-01';

-- 2번 연습문제
SELECT jikwonname AS '직원명', jikwonjik AS '직급', jikwonibsail AS '입사년월일', case when TRUNCATE(DATEDIFF(NOW(), jikwonibsail) / 365, 0) >= 8 then '왕고참' when TRUNCATE(DATEDIFF(NOW(), jikwonibsail) / 365, 0) >= 3 then '보통' ELSE '일반' END AS '구분', case when busernum = '10' then '총무부' when busernum = '20' then '영업부' when busernum = '30' then '전산부' when busernum = '40' then '관리부' END AS '부서' FROM jikwon;

-- 3번 연습문제
SELECT jikwonno AS '사번', jikwonname AS '직원명', busernum AS '부서', jikwonpay AS '연봉', case when busernum = 10 then round(jikwonpay * 1.1, 0) when busernum = 30 then round(jikwonpay * 1.2, 0) ELSE jikwonpay END AS '인상연봉', case when TRUNCATE(DATEDIFF(NOW(), jikwonibsail) / 365, 0) >= 10 then 'O' ELSE 'X' END AS '장기근속(10년기준)' FROM jikwon;


SELECT * FROM jikwon;
SELECT * FROM buser;



-- 집계 함수(복수행 함수) : 전체 자료를 그룹별로 구분해 통계 결과를 얻기 위한 함수
SELECT sum(jikwonpay) AS 합, AVG(jikwonpay) as 평균 FROM jikwon;
SELECT max(jikwonpay) AS 최대, min(jikwonpay) as 최소 FROM jikwon;

SELECT * FROM jikwon;
UPDATE jikwon SET jikwonpay = NULL WHERE jikwonno = 5;
SELECT * FROM jikwon;
desc jikwon;			-- NULL 할때는 항상 확인하고 하기

SELECT AVG(jikwonpay), AVG(nvl(jikwonpay, 0)) FROM jikwon;			--  *** NULL 은 작업에서 제외하고 처리함 ***   -->> AVG(nvl(jikwonpay, 0)) : NULL도 작업에 참여시키려면
SELECT SUM(jikwonpay) / 29, SUM(jikwonpay) / 30 FROM jikwon;		-- 둘이 같은결과

SELECT COUNT(jikwonno), COUNT(jikwonpay) FROM jikwon;					-- NULL 처리X
SELECT COUNT(*) AS 인원수 FROM jikwon;			-- NULL, NOT NULL 찾기 어려우니까 전체 건수로 처리
SELECT stddev(jikwonno) AS 표준편차, var_samp(jikwonpay) AS 분산 FROM jikwon;

SELECT COUNT(*) AS 인원, VAR_SAMP(jikwonpay) AS 분산 FROM jikwon WHERE busernum = 10;
SELECT COUNT(*) AS 인원, VAR_SAMP(jikwonpay) AS 분산 FROM jikwon WHERE busernum = 20;


-- 과장은 몇명인지 알고싶을 때
SELECT COUNT(*) AS 인원수 FROM jikwon WHERE jikwonjik = '과장';

-- 2010 년 이전에 입사한 남 직원은 몇 명?
select COUNT(*) AS 인원수 FROM jikwon WHERE jikwonibsail < '2010-1-1' AND jikwongen = '남';

-- 2015년 이후 입사한 여직원의 연봉합,연봉 평균, 인원수는?
SELECT SUM(jikwonpay) AS 연봉합, AVG(jikwonpay) AS 연봉평균, COUNT(*) AS 인원수 FROM jikwon WHERE jikwonibsail > '2015-1-1' AND jikwongen = '여';



-- 그룹 함수 : group by 절 : 소개출력
-- select 그룹 칼럼명, 계산함수, ... from 테이블명 where 조건 group by 그룹칼럼명 having 조건
-- 그룹칼럼에 대해 order by 할 수 없다. 단, 출력 결과는 oreder by 가능

-- 성별 연봉 평균, 인원수를 출력
SELECT AVG(jikwongen), COUNT(jikwonpay)  from jikwon GROUP BY jikwongen;

-- 부서별 연봉 함
select busernum, SUM(jikwonpay) FROM jikwon group BY busernum;

-- 부서별 연봉합이 3500 이상
GROUP BY busername HAVING SUM(jikwonpay) >= 35000;

-- 부서별 연봉합 : 여성만
SELECT busernum, SUM(jikwonpay) FROM jikwon WHERE jikwongen = '여' GROUP BY busernum;

-- 부서별 연봉합 : 연봉함이 15000이상만 여성만
SELECT busernum, SUM(jikwonpay) FROM jikwon WHERE jikwongen = '여' GROUP BY busernum HAVING SUM(jikwonpay) >= 15000;
SELECT busernum, SUM(jikwonpay) AS paytotal FROM jikwon WHERE jikwongen = '여' GROUP BY busernum HAVING paytotal >= 15000;

-- 주의
SELECT busernum, SUM(jikwonpay) FROM jikwon order by busernum GROUP BY busernum;		-- error
SELECT busernum, SUM(jikwonpay) FROM jikwon GROUP BY busernum ORDER BY SUM(jikwonpay) DESC;


SELECT * FROM jikwon;
SELECT * FROM buser;


-- 연습문제
-- 1) 직급별 급여의 평균 (NULL인 직급 제외)
SELECT jikwonjik, round(AVG(jikwonpay),0) AS 급여평균 FROM jikwon WHERE jikwonjik IS NOT NULL GROUP BY jikwonjik;

-- 2) 부장,과장에 대해 직급별 급여의 총합
SELECT jikwonjik, SUM(jikwonpay) AS 급여의총합 FROM jikwon WHERE jikwonjik IN ('부장', '과장') GROUP BY jikwonjik ORDER BY jikwonjik DESC;

-- 3) 2015년 이전에 입사한 자료 중 년도별 직원수 출력
SELECT DATE_FORMAT(jikwonibsail, '%Y') AS 입사연도, COUNT(jikwonname) AS 직원수 FROM jikwon WHERE DATE_FORMAT(jikwonibsail, '%Y') < 2015 GROUP BY DATE_FORMAT(jikwonibsail, '%Y')

-- 4) 직급별 성별 인원수, 급여합 출력 (NULL인 직급은 임시직으로 표현)
SELECT nvl(jikwonjik, '임시직') AS 직급, jikwongen AS 성별, COUNT(*) AS 인원수, SUM(jikwonpay) AS 급여합 FROM jikwon GROUP BY jikwonjik, jikwongen;

-- 5) 부서번호 10,20에 대한 부서별 급여 합 출력
SELECT busernum AS 부서번호, SUM(jikwonpay) FROM jikwon WHERE busernum IN(10, 20) GROUP BY busernum;

-- 6) 급여의 총합이 7000 이상인 직급 출력(NULL인 직급은 임시직으로 표현)
SELECT nvl(jikwonjik, '임시직') AS 직급, SUM(jikwonpay) AS 급여합 FROM jikwon GROUP BY jikwonjik HAVING SUM(jikwonpay) >= 7000;

-- 7) 직급별 인원수, 급여합계를 구하되 인원수가 3명 이상인 직급만 출력
SELECT nvl(jikwonjik, '임시직') AS 직급, COUNT(jikwonname) AS 인원수, SUM(jikwonpay) AS 급여합계 FROM jikwon GROUP BY jikwonjik HAVING COUNT(jikwonname) >= 3;



-- ****JOIN**** : 하나 이상의 테이블에서 원하는 자료 추출
-- 공통 칼럼이 필요하다

DESC buser;
DESC jikwon;
DESC gogek;

SELECT * FROM buser;
INSERT INTO buser(buserno, busername) VALUES(50, '기획실');		-- 연습을 위해 세팅

SELECT * FROM jikwon;
ALTER TABLE jikwon MODIFY busernum INT NULL;
UPDATE jikwon SET busernum = NULL WHERE jikwonno = 5;

SELECT jikwonname FROM jikwon;  -- select test.jikwon.jikwonname 으로 써야 정석
SELECT mytab.jikwonname FROM jikwon AS mytab;		-- 테이블 이름으로 구분 

-- cross join : 한 쪽 테이블의 모든 행과 다른 쪽 테이블의 모든 행을 연결하는 기능
SELECT jikwonname, busername FROM jikwon, buser;			-- 서로 1:1 대응(실제로는 잘 안씀)

SELECT jikwonname, busername feom jikwon CROSS JOIN buser;		-- 정석 방법

-- cross join 중 self join이 있다
SELECT a.jikwonname, b.jikwonname FROM jikwon a, jikwon b;

-- EQUI join : 조인 조건식에 '=' 을 사용. 두 테이블은 '같다' 조건으로 join
-- 대부분의 pk, fk 조인은 EQUI join이다.
SELECT jikwonname, busername FROM jikwon, buser WHERE jikwon.busernum = buser.buserno;		-- null은 제외 됨

-- non-EQUI join : 조인 조건식에 '=' 이외의 관계연산자를 사용
CREATE TABLE paygrade(grade INT PRIMARY KEY, lpay INT, hpay INT);		-- 실습을 위한 세팅
INSERT INTO paygrade VALUES(1, 0, 1999);
INSERT INTO paygrade VALUES(2, 2000, 2999);
INSERT INTO paygrade VALUES(3, 3000, 3999);
INSERT INTO paygrade VALUES(4, 4000, 4999);
INSERT INTO paygrade VALUES(5, 5000, 9999);
SELECT * FROM paygrade;

SELECT jiktab.jikwonname, jiktab.jikwonpay, paytab.grade FROM jikwon AS jiktab, paygrade AS paytab WHERE jiktab.jikwonpay >= paytab.lpay AND jiktab.jikwonpay <= paytab.hpay;			-- non- EQUI join 자주 안쓰임

-- inner join : 두테이블을 조인할 때, 두 테이블의 모두 지정한 열의 데이터가 있는 경우만 추출
SELECT jikwonno, jikwonname, busername FROM jikwon, buser WHERE busernum = buserno;			-- 표준방식 아님, 오라클에서 주로 사용
SELECT jtab.jikwonno, jtab.jikwonname, btab.busername FROM jikwon AS jtab, buser as btab WHERE jtab.busernum = btab.buserno;			-- 표준방식
SELECT jikwonno, jikwonname, busername FROM jikwon, buser WHERE busernum = buserno AND jikwongen = '남';		--  whrer 조건에 join 조건 + record 제한 조건 --> 가독성 나쁨

SELECT jikwonno, jikwonname, busername FROM jikwon INNER JOIN buser ON busernum = buserno;		-- 결과는 똑같음
SELECT jikwonno, jikwonname, busername FROM jikwon INNER JOIN buser ON busernum = buserno WHERE jikwongen = '남'  -- 표준방식 : 두 조건을 구분 지어서 걸어주는 방법



-- outer join : 두 테이블을 조인할 때 1개의 테이블에만 자료가 있어도 경과 추출
-- left outer join
SELECT jikwonno, jikwonname, busername FROM jikwon, buser WHERE busername = buserno(+); 		-- 오라클 방식, 사용 불가

-- right outer join
SELECT jikwonno, jikwonname, busername FROM jikwon, buser WHERE busername(+) = buserno;  -- 오라클..

-- left outer join
SELECT jikwonno, jikwonname, busername FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno;		-- 왼쪽은 다 나옴

-- right outer join
SELECT jikwonno, jikwonname, busername FROM jikwon RIGHT OUTER JOIN buser ON busernum = buserno;	-- 오른쪽 다 나옴

-- full outer join			-->>  지원하지 않음, 오라클 전용
SELECT jikwonno, jikwonname, busername FROM jikwon FULL OUTER JOIN buser ON busernum = buserno;

SELECT jikwonno, jikwonname, busername FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno UNION SELECT jikwonno, jikwonname, busername FROM jikwon RIGHT OUTER JOIN buser ON busernum = buserno;
-- mariaDB는 full outer join을 union 을 이용해서 사용해야 한다 left + Right

SELECT SUM(jikwonpay) AS hap, COUNT(*) AS COUNT FROM jikwon INNER JOIN buser ON busernum = buserno WHERE jikwongen = '남';

SELECT FROM gogek;		-- buser TABLE과는 join 불가(공통 칼럼X)   중간에 jikwon을 걸어두면 가능


-- 연습문제

-- 문1) 직급이 '사원' 인 직원이 관리하는 고객자료 출력
SELECT * FROM jikwon;
SELECT * FROM gogek;

SELECT jikwonno AS 사번, jikwonname AS 직원명, jikwonjik AS 사원, gogekname AS 고객명, gogektel AS 고객전화, case when gogekjumin LIKE '_______1%' then '남' ELSE '여' END AS 고객성별 from jikwon inner JOIN gogek ON jikwonno = gogekdamsano WHERE jikwonjik = '사원';

-- 문2) 직원별 고객 확보 수  -- GROUP BY 사용
SELECT jikwonname AS 직원명, COUNT(gogekname) AS 고객확보수 FROM jikwon LEFT OUTER JOIN gogek ON jikwonno = gogekdamsano GROUP BY jikwonno;		-- 동명이인이 있는경우 jikwonname으로 그룹하면 문제 발생 

-- 문3) 고객이 담당직원의 자료를 보고 싶을 때 즉, 고객명을 입력하면,  담당직원 자료 출력 
SELECT jikwonname AS 직원명, jikwonjik AS 직급 FROM jikwon INNER JOIN gogek ON jikwonno = gogekdamsano WHERE gogekname = '강나루';

-- 문4) 직원명을 입력하면 관리고객 자료 출력
SELECT gogekname AS 고객명, gogektel AS 고객전화, gogekjumin AS 주민번호, 2026- (1900 + SUBSTR(gogekjumin, 1, 2)) AS 나이 FROM gogek INNER JOIN jikwon ON gogekdamsano = jikwonno WHERE jikwonname = '이순라';



-- 세 개의 테이블 조인 : 두개를 먼저 조인 후 그 결과와 나머지 테이블로 조인
SELECT jikwonname, busername, gogekname FROM jikwon, buser, gogek WHERE busernum = buserno AND jikwonno = gogekdamsano;		-- inner join(null 값 제외)

SELECT jikwonname, busername, gogekname FROM jikwon INNER JOIN buser ON busernum = buserno INNER JOIN gogek ON jikwonno = gogekdamsano;		-- 표준 방식


-- 연습문제
-- 문1) 총무부에서 관리하는 고객수 출력 (고객 30살 이상만 작업에 참여)
SELECT busername AS 부서, COUNT(gogekname) AS 고객수 FROM jikwon INNER JOIN buser ON busername = '총무부' INNER JOIN gogek ON jikwonno = gogekdamsano WHERE busernum = 10 AND (2026- (1900 + SUBSTR(gogekjumin, 1, 2))) >= 30; 

SELECT * FROM buser;

-- 문2) 부서명별 고객 인원수 (부서가 없으면 "무소속")
SELECT nvl(busername, '무소속') AS 부서, COUNT(gogekname) AS 고객인원수 FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno INNER JOIN gogek ON jikwonno = gogekdamsano GROUP BY busername;


-- 문3) 고객이 담당직원의 자료를 보고 싶을 때 즉, 고객명을 입력하면  담당직원 자료 출력
SELECT jikwonname AS 직원명, jikwonjik AS 직급, busername AS 부서명, busertel AS 부서전화, jikwongen AS 성별 FROM jikwon INNER JOIN buser ON busernum = buserno INNER JOIN gogek ON jikwonno = gogekdamsano WHERE gogekname = '강나루';

-- 문4) 부서와 직원명을 입력하면 관리고객 자료 출력
SELECT gogekname AS 고객명, gogektel AS 고객전화, case when gogekjumin LIKE '_______1%' then '남' ELSE '여' END AS 고객성별 FROM jikwon INNER JOIN gogek ON jikwonno = gogekdamsano INNER JOIN buser ON busernum = buserno WHERE busername = '영업부' AND jikwonname = '이순신';


-- union : 구조가 일치하는 두 개 이상의 테이블 자료 합쳐 출력. 원래의 테이블 계속 유지,, (이름이 같을 필요 없음)
CREATE TABLE pum1(bun INT, pummok VARCHAR(20));
INSERT INTO pum1 VALUES(1, '귤');
INSERT INTO pum1 VALUES(2, '한라봉');
INSERT INTO pum1 VALUES(3, '바나나');

SELECT * FROM pum1;

CREATE TABLE pum2(mum INT, sangpum VARCHAR(20));
INSERT INTO pum2 VALUES(10, '토마토');
INSERT INTO pum2 VALUES(20, '딸기');
INSERT INTO pum2 VALUES(30, '참외');
INSERT INTO pum2 VALUES(40, '수박');

SELECT * FROM pum2;

SELECT bun AS 번호, pummok AS 품명 FROM pum1 UNION SELECT mum, sangpum FROM pum2;



-- subquery : query 내에 query가 있는 형태 (주로 안쪽 질의 결과를 바깥쪽 질의에서 참조)
-- 다른 테이블의 결과를 조건으로 쓰고 싶을 때 
-- 계산된 값을 이용하고 싶을 때
-- 복잡한 조건을 단계적으로 나눠 처리하고 싶을 때.....

-- where 안에 있는 subquery__ 제일 많이 쓰임 
-- 이미라 직원과 직급이 같은 직원 출력
SELECT jikwonjik FROM jikwon WHERE jikwonname = '이미라';		-- 대리
SELECT * FROM jikwon WHERE jikwonjik = '대리';						-- select 문 2번 > 서버에 2번 접속

SELECT * FROM jikwon WHERE jikwonjik = (SELECT jikwonjik FROM jikwon WHERE jikwonname = '이미라');	-- 한번에 처리

-- 직급이 대리 중에서 가장 먼저 입사한 직원 출력
SELECT * FROM jikwon WHERE jikwonjik = '대리' AND jikwonibsail = (SELECT MIN(jikwonibsail) FROM jikwon WHERE jikwonjik = '대리');		-- 맞는 것같아 보이지만 입사연월을 반환하기 떄문에 대리라는 조건이 들어가지 않음


-- 인천에 근무하는 직원 출력
SELECT * FROM jikwon WHERE busernum = (SELECT buserno FROM buser WHERE buserloc = '인천');		-- 다른 테이블에서 부터도 얻을 수 있다 /  꼭 join만있는건 아님

-- 인천 이외에 근무하는 직원 출력
SELECT * FROM jikwon WHERE busernum IN (SELECT buserno FROM buser WHERE NOT buserloc = '인천');		-- 서브쿼리에서 몇개의 값이 나오는지 주의해서 작성
SELECT * FROM jikwon WHERE busernum <> (SELECT buserno FROM buser WHERE buserloc = '인천');			-- 서브쿼리의 결과를 부정해서 받는 방법(같은 결과)


-- 고객 중 차일호와 나이가 같은 자료 출력
SELECT * FROM gogek WHERE SUBSTR(gogekjumin, 1, 2) = (SELECT SUBSTR(gogekjumin, 1, 2) FROM gogek WHERE gogekname = '차일호');


SELECT * FROM jikwon;

-- subquery 연습문제
-- 문1) 2010년 이후에 입사한 남자 중 급여를 가장 많이 받는 직원은?
SELECT * FROM jikwon WHERE jikwongen = '남' AND jikwonibsail >= '2010-1-1' AND jikwonpay = (SELECT MAX(jikwonpay) FROM jikwon WHERE jikwongen = '남' AND SUBSTR(jikwonibsail, 1,4) >= 2010);
-- 2010 년 이후 입사한 정보 빠지지 않게 주의!!

-- 문2) 평균급여보다 급여를 많이 받는 직원은?
SELECT * FROM jikwon WHERE jikwonpay > (SELECT AVG(jikwonpay) FROM jikwon);

-- 문3) '이미라' 직원의 입사 이후에 입사한 직원은?
SELECT * FROM jikwon WHERE jikwonibsail >= (SELECT jikwonibsail FROM jikwon WHERE jikwonname = '이미라') ORDER BY jikwonibsail;

-- 문4) 2010 ~ 2015년 사이에 입사한 총무부(10),영업부(20),전산부(30) 직원 중 급여가 가장 적은 사람은?
SELECT * FROM jikwon WHERE jikwonibsail BETWEEN '2010-1-1' AND '2015-12-31' AND busernum IN (10, 20, 30) AND jikwonpay = (SELECT MIN(jikwonpay) FROM jikwon WHERE jikwonibsail BETWEEN '2010-1-1' AND '2015-12-31' AND busernum IN (10, 20, 30)) AND jikwonjik IS NOT NULL;

-- 문5) 한송이, 이순신과 직급이 같은 사람은 누구인가?
SELECT * FROM jikwon WHERE jikwonjik IN (SELECT jikwonjik FROM jikwon WHERE jikwonname = '한송이' OR jikwonname = '이순신') ORDER BY jikwonjik;

-- 문6) 과장 중에서 최대급여, 최소급여를 받는 사람은?
SELECT * FROM jikwon WHERE jikwonjik = '과장' AND jikwonpay IN ((SELECT MAX(jikwonpay) FROM jikwon WHERE jikwonjik = '과장'), (SELECT min(jikwonpay) FROM jikwon WHERE jikwonjik = '과장'));

-- 문7) 10번 부서의 최소급여보다 많은 사람은?
SELECT * FROM jikwon WHERE jikwonpay > (SELECT MIN(jikwonpay) FROM jikwon WHERE busernum = 10);

-- 문8) 30번 부서의 평균급여보다 급여가 많은 '대리' 는 몇명인가?
SELECT COUNT(*) FROM jikwon WHERE jikwonjik = '대리' AND jikwonpay > (SELECT AVG(jikwonpay) FROM jikwon WHERE busernum = 30);

-- 문9) 고객을 확보하고 있는 직원들의 이름, 직급, 부서명을 입사일 별로 출력하라.
SELECT jikwonname AS 직원명, jikwonjik AS 직급, busername AS 부서명, jikwonibsail AS 입사일  FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno WHERE jikwonno IN (SELECT DISTINCT gogekdamsano FROM gogek) ORDER BY jikwonibsail;

-- 문10) 이순신과 같은 부서에 근무하는 직원과 해당 직원이 관리하는 고객 출력(고객은 나이가 30 -> 40 이하면 '청년', 50 이하면 '중년', 그 외는 '노년'으로 표시하고, 고객 연장자 부터 출력)
SELECT jikwonname AS 직원명, busername AS 부서명, busertel AS 부서전화, jikwonjik AS 직급, gogekname AS 고객명, gogektel AS 고객전화, case when (2026- (1900 + SUBSTR(gogekjumin, 1, 2))) <= 40 then '청년' when (2026- (1900 + SUBSTR(gogekjumin, 1, 2))) <= 50 then '중년' when (2026- (1900 + SUBSTR(gogekjumin, 1, 2))) > 50 then '노년' ELSE '없음' END AS '고객구분' FROM jikwon INNER JOIN buser ON busernum = buserno LEFT OUTER JOIN gogek ON jikwonno = gogekdamsano WHERE busernum = (SELECT busernum FROM jikwon WHERE jikwonname = '이순신') ORDER BY (YEAR(CURDATE() - (1900 + SUBSTR(gogekjumin, 1, 2))) DESC;
-- outer join 이 아니라 inner join이 더 맞음
-- 2026 상수 값 보다는 now, sysdate등등을 사용하는 것이 더 좋음



-- 쿼리문은 동일한 결과를 여러 방법으로 수행 가능
-- 예) 총무부에 근무하는 직원들이 관리하는 고객 출력
-- subquery를 이용해서
SELECT gogekno, gogekname, gogektel FROM gogek WHERE gogekdamsano IN (SELECT jikwonno FROM jikwon WHERE busernum = (SELECT buserno FROM buser WHERE busername = '총무부'));

-- join을 이용해서
SELECT gogekno, gogekname, gogektel FROM gogek INNER JOIN jikwon ON jikwon.jikwonno = gogek.gogekdamsano INNER JOIN buser ON jikwon.busernum = buser.buserno WHERE busername = '총무부';



-- subquey 다양하게 활용                                                                                   

-- any, all 연산자 : null 인 자료는 제외하고 작업한다.

-- 공식처럼 사용한다고 생각하면 됨
-- < any : subquery의 반환값 중 최대값 보다 작은 ~     <= 도 가능
-- > any : subquery의 반환값 중 최소값 보다 큰 ~
-- < all : subquery의 반환값 중 최소값 보다 작은 ~
-- > any : subquery의 반환값 중 최대값 보다 큰 ~

-- '대리'의 최대값보다 적은 연봉을 받는 직원은?
SELECT jikwonno, jikwonname, jikwonpay FROM jikwon WHERE jikwonpay < ANY (SELECT jikwonpay FROM jikwon WHERE jikwonjik = '대리');

-- 30번 부서의 최고 연봉자 보다 연봉을 많이 받는 직원은?
SELECT jikwonno, jikwonname, jikwonpay FROM jikwon WHERE jikwonpay > ALL (SELECT jikwonpay FROM jikwon WHERE busernum = 30);

-- 30번 부서의 최저 연봉자 보다 연봉을 많이 받는 직원은?
SELECT jikwonno, jikwonname, jikwonpay FROM jikwon WHERE jikwonpay > ANY (SELECT jikwonpay FROM jikwon WHERE busernum = 30) ORDER BY jikwonpay;



-- exists 연산자

-- 직원이 있는 부서 출력
SELECT busername, buserloc FROM buser bu WHERE EXISTS (SELECT 'imsi' FROM jikwon WHERE jikwon.busernum = bu.buserno);		-- true 반환

-- 직원이 없는 부서 출력
SELECT busername, buserloc FROM buser bu WHERE NOT EXISTS (SELECT 'imsi' FROM jikwon WHERE jikwon.busernum = bu.buserno);		-- false 반환


-- from 절에 사용하는 subquery (흔하진 않음)
-- 전체 평균 연봉과 최대 연봉 사이의 연봉을 받는 직원 출력
SELECT jikwonno, jikwonname, jikwonpay FROM jikwon a, (SELECT AVG(jikwonpay) avgs, MAX(jikwonpay) maxs FROM jikwon) b WHERE a.jikwonpay BETWEEN b.avgs AND b.maxs;


-- group by 의 having 절에 포함된 subquery 
-- 부서별 평균연봉 중 30번 부서의 평균 연봉보다 큰 자료(부서) 출력
SELECT busernum, AVG(jikwonpay) FROM jikwon GROUP BY busernum HAVING AVG(jikwonpay) > (SELECT AVG(jikwonpay) FROM jikwon WHERE busernum = 30);



-- 상관 subquery : outer query의 각 행을 inner query에서 참조하여 수행하는 subquery
-- 안쪽 질의에서 바깥쪽 질의를 참조하고, 다시 안쪽의 결과를 바깥쪽 질의에서 참조하는 형태
-- 각 부서의 최대 연봉자는?
SELECT *FROM jikwon a WHERE a.jikwonpay = (SELECT MAX(b.jikwonpay) FROM jikwon b WHERE a.busernum = b.busernum);

-- 연봉 순위 3위 이내의 직원 출력(descending sort)
SELECT a.jikwonno, a.jikwonname, a.jikwonpay FROM jikwon a WHERE 3 > (SELECT COUNT(*) FROM jikwon b WHERE b.jikwonpay > a.jikwonpay) AND jikwonpay IS NOT NULL ORDER BY jikwonpay DESC;


-- subquery 를 이용한 table 생성 및 insert 수행
CREATE TABLE jiktab1 AS SELECT * FROM jikwon;		-- jikwon과 동일 테이블 생성 / pk는 제외
DESC jiktab1;
SELECT * FROM jiktab1;

DROP TABLE jiktab2;
CREATE TABLE jiktab2 AS SELECT * FROM jikwon WHERE 1 = 0;			-- jikwon과 동일 구조 테이블 생성
SELECT * FROM jiktab2;
DESC jiktab2;
INSERT INTO jiktab2 SELECT * FROM jikwon WHERE jikwonjik = '과장';		-- insert + subquery

INSERT INTO jiktab2 (jikwonno, jikwonname, busernum) SELECT jikwonno, jikwonname, busernum FROM jikwon WHERE jikwonjik = '대리';


-- update + subquery
SELECT * FROM jiktab1;
UPDATE jiktab1 SET jikwonjik = (SELECT jikwonjik FROM jikwon WHERE jikwonname = '이순신') WHERE jikwonno = 2;

-- delete + subquery
DELETE FROM jiktab1 WHERE jikwonno IN (SELECT DISTINCT gogekdamsano FROM gogek);


-- -------------------------------------------------------------------------------------------------------------------------------------------------------------

-- transaction : DB의 상태를 변경시키는 논리적인 작업 단위
-- 4가지 특징 : ACID 
-- insert, update, delete 시 트랜잭션 시작됨(데이터의 변화)
-- COMMIT, ROLLBACK 으로 트랜잭션 종료
-- 서버종료, 타임아웃 등이 발생해도 트랜잭션 종료

SHOW VARIABLES LIKE 'autocommit%';		-- autocommit 설정값 확인(현재는 기본으로 on 되어 있음)
SET autocommit = TRUE;				-- autocommit 설정
SET autocommit = FALSE;				-- autocommit 해제		off로 작업을 했어도 작업이 끝나면 on으로 복구해놓고 마쳐야 함


-- Transaction 연습
CREATE TABLE jiktab3 AS SELECT * FROM jikwon;
SELECT * FROM jiktab3; -- 연습용 테이블

-- 연습 1
SET autocommit = FALSE;
DELETE FROM jiktab3 WHERE jikwonno = 2;		-- 트랜잭션 시작 : 현재 클라이언트에서만 삭제된 상태 / 서버에는 아무 영향 없음
SELECT * FROM jiktab3;
ROLLBACK;			-- 트랜잭션 종료 : 다시 클라이언트 내용 복구
COMMIT; 			-- 트랜잭션 종료 : DB 서버에 클라이언트의 내용을 근거로 원본 갱신
SET autocommit = TRUE;			-- 다시 자동으로 복구


-- 연습 2 : save point(저장점)를 이용해 부분적인 트랜잭션 처리 가능
SET autocommit = FALSE;
SELECT * FROM jiktab3 WHERE jikwonno = 4;
UPDATE jiktab3 SET jikwonpay = 7777 WHERE jikwonno = 4;			-- 트랜잭션 시작
SAVEPOINT a;		-- 저장점 설정
UPDATE jiktab3 SET jikwonpay = 8888 WHERE jikwonno = 5;
SELECT * FROM jiktab3 WHERE jikwonno = 5;
ROLLBACK TO SAVEPOINT a;								-- save point 까지 롤백 ( 부분 작업 취소 )  --> 트랜잭션 종료 아님
SELECT * FROM jikwon WHERE jikwonno <= 6;			-- 4번은 수정 5번은 ROLLBACK됨
ROLLBACK;					-- 전체 작업 취소 / 트랜잭션 종료(하나의 작업 단위가 끝남)

UPDATE jiktab3 SET jikwonpay = 9999 WHERE jikwonno = 5;		-- 트랜잭션 시작
COMMIT;				-- 트랜잭션 종료  --> DB 서버 내용 갱신
SET autocommit = TRUE;	-- 다시 자동으로 복구



-- 교착 상태(DeadLock) : 두 개 이상의 트랜잭션이 서로 상대방이 가진 LOCK을 기다리면서 영원히 진행하지 못하는 상태
-- 해결책은 트랜잭션을 수행완료 또는 취소하면 된다
-- 일관성 유지가 중요함

SET autocommit = FALSE;
SELECT * FROM jiktab3 WHERE jikwonno = 7;
UPDATE jiktab3 SET jikwonpay = 1234 WHERE jikwonno = 7;		-- 트랜잭션 시작
-- DELETE FROM jiktab3 WHERE jikwonno = 7;  --> 이 내용을 프롬포트에 치면 아무 진행이 되지 않음 timeout 에러 ( 트랜잭션이 종료 되지 않았기 때문에 )
COMMIT;		-- 트랜잭션 종료와 동시에 데드락 해결되고 작업이 진행됨
SET autocommit = TRUE;	-- 다시 자동으로 복구



-- ------------------------------------------------------------------------------------------------------------------------------------------------

-- view 파일
-- 물리적인 테이블을 근거로 select 문(조건포함)을 파일로 저장하여, 가상의 테이블로 사용한다
-- 물리적인 테이블이 아니므로 메모리 소모가 거의 없다
-- 복잡하고 긴 쿼리문을 단순화 가능, 보안 강화, 자료의 독립성 확보
-- 형식 : create [or replace] view 뷰파일명 as select 문
-- 		 alter view 뷰파일명~
-- 		 drop view 뷰파일명~

SELECT jikwonno, jikwonname, jikwonpay FROM jikwon WHERE jikwonibsail < '2010-12-31';		-- 클라이언트 상으로 데이터 읽어옴

CREATE OR REPLACE VIEW v_a AS SELECT jikwonno, jikwonname, jikwonpay FROM jikwon WHERE jikwonibsail < '2010-12-31';		-- 뷰파일 생성

SHOW TABLES;		-- 테이블과 동일하게 사용 가능
SELECT * FROM v_a;
DESC v_a;

SHOW FULL TABLES IN test WHERE table_type LIKE 'VIEW';		-- 뷰파일 목룍 확인
SELECT SUM(jikwonpay) AS 연봉합 FROM v_a;				-- 테이블에서 하는 모든 것 가능

CREATE VIEW v_b AS SELECT * FROM jikwon WHERE jikwonname LIKE '김%' OR jikwonname LIKE '이%' OR jikwonname LIKE '박%';
SELECT * FROM v_b ORDER BY jikwonname;
SELECT jikwonno, jikwonname, jikwonpay FROM v_b WHERE jikwonjik = '사원';

-- ALTER TABLE jikwon RENAME kbs;  --> 원본 테이블(물리적인)이 없어졌으므로 뷰 참조 불가

CREATE VIEW v_c AS SELECT * FROM jikwon ORDER BY jikwonpay DESC;		-- order by 에 대해서도 뷰파일 생성 가능
SELECT * FROM v_c;				-- 항상 내림차순으로 출력됨

CREATE VIEW v_d AS SELECT jikwonno, jikwonname, jikwonpay * 10000 AS ypay FROM jikwon;			-- 수식도 가능함
SELECT * FROM v_d;

CREATE VIEW v_e AS SELECT jikwonname, ypay FROM v_d WHERE ypay >= 50000000;		-- 뷰로 다시 뷰파일을 만들 수 있다
SELECT * from v_e;

UPDATE v_e SET jikwonname = '김치국' WHERE jikwonname = '김부만';
SELECT * FROM v_e;
SELECT * FROM v_d;
SELECT * FROM jikwon;			-- 뷰 파일을 수정하면 원본 테이블도 수정됨 --> 상위 뷰파일, 원본 테이블 모두 수정

DELETE FROM v_d WHERE jikwonname = '최미숙';
SELECT * FROM v_d;
SELECT * FROM jikwon;

DELETE FROM v_d WHERE ypay = 41000000;			-- 계산칼럼에 의한 수정도 가능하다
SELECT * FROM v_d;
SELECT * FROM jikwon;

SELECT * FROM v_d;
UPDATE v_d SET ypay = 1111 WHERE jikwonname = '홍길동';		-- err :  원본테이블에 ypay가 없으므로 수정 불가 / 계산으로 만들어진 칼럼은 수정할 수 없다

CREATE OR REPLACE view v_e AS SELECT jikwonno, jikwonname, busernum, jikwonpay FROM jikwon;		-- 덮어씀
SELECT * FROM v_e;
INSERT INTO v_e VALUES(31, '김밥', 20, 5000);			-- 원본 테이블에 업데이트 된 것/ view file로 insert 도 가능하다
SELECT * FROM jikwon;

DESC jikwon;		-- view의 insert는 원본의 not null 칼럼은 반드시 참여해야 한다

CREATE OR REPLACE VIEW v_f AS SELECT jikwonno, jikwonname, busernum, jikwonpay, jikwonibsail FROM jikwon WHERE jikwonibsail < '2015-1-1';
SELECT * FROM v_f;
INSERT INTO v_f VALUES(32, '공기밥', 10, 6000, '2014-5-6');
INSERT INTO v_f VALUES(33, '주먹밥', 10, 7000, '2025-5-7');		-- err 아님
SELECT * FROM v_f;    -- 33번 데이터가 없다 / 데이터 추가는 잘 된거지만, 조건이 맞지 않기 때문에 보이지 않는 것
SELECT * FROM jikwon;		-- jikwon table에는 들어가 있음을 확인할 수 있다

CREATE VIEW v_group AS SELECT jikwonjik,SUM(jikwonpay) AS hap, AVG(jikwonpay) AS ave FROM jikwon GROUP BY jikwonjik;
SELECT * FROM v_group;		-- GROUP BY에 의한 view는 참조만 가능하다( insert, update, delete 불가)

CREATE or REPLACE VIEW v_join AS SELECT jikwonno, jikwonname, busernum, jikwonjik FROM jikwon INNER JOIN buser ON jikwon.busernum = buser.buserno WHERE jikwon.busernum IN (10, 20);
SELECT * FROM v_join;			-- join에 의한 view도 가능하다
UPDATE v_join SET jikwonname = '손오공' WHERE jikwonname = '박명화';
SELECT * FROM v_join;
UPDATE v_join SET jikwonname = '사오정', busername = '영업부'  WHERE jikwonname = '손오공';		-- err : busername은 buser table의 칼럼
SELECT * FROM v_join;
-- join에 의한 view는 한 개의 테이블만 수정에 참여해야 함
DELETE FROM v_join WHERE jikwonname = '손오공';		-- err : join에 의한 view는 데이터 삭제 불가능 / Oracle은 가능..


-- 연습문제
-- 문1) 사번   이름    부서  직급  근무년수  고객확보
--       1   홍길동  영업부 사원     6           O   or  X
-- 조건 : 직급이 없으면 임시직, 전산부 자료는 제외
-- 위의 결과를 위한 뷰파일 v_exam1을 작성
CREATE OR REPLACE VIEW v_exam1 AS SELECT distinct jikwonno AS 사번, jikwonname AS 이름, busername AS 부서, nvl(jikwonjik, '임시직') AS 직급, DATE_FORMAT(NOW(), '%Y') - DATE_FORMAT(jikwonibsail, '%Y') AS 근무년수, case nvl(gogekname, 'a') when 'a' then 'X' ELSE 'O' END AS 고객확보 FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno LEFT OUTER JOIN gogek ON jikwonno = gogekdamsano WHERE busername <> '전산부' OR busername IS NULL;
SELECT * FROM v_exam1;



-- 문2) 부서명   인원수
--      영업부     7
-- 조건 : 직원수가 가장 많은 부서 출력
-- 위의 결과를 위한 뷰파일 v_exam2을 작성
CREATE OR REPLACE VIEW v_exam2 AS SELECT busername AS 부서명, COUNT(*) AS 인원수 FROM jikwon INNER JOIN buser ON busernum = buserno GROUP BY busername ORDER BY 인원수 desc;
SELECT * FROM v_exam2 WHERE 인원수 = (SELECT MAX(인원수) FROM v_exam2);
SELECT * FROM v_exam2;

-- 강사님 풀이
CREATE OR REPLACE VIEW v_exam2 AS 
SELECT busername AS 부서명, COUNT(*) AS 인원수 FROM buser INNER JOIN jikwon ON buser.buserno = jikwon.busernum GROUP BY busername HAVING 인원수 = (SELECT COUNT(*) FROM jikwon GROUP BY busernum ORDER BY COUNT(*) DESC LIMIT 1);
SELECT * FROM v_exam2;

-- 문3) 가장 많은 직원이 입사한 요일에 입사한 직원 출력
--    직원명   요일     부서명   부서전화
--    한국인  수요일   전산부   222-2222
-- 위의 결과를 위한 뷰파일 v_exam3을 작성
CREATE OR REPLACE VIEW v_exam3 AS SELECT jikwonname AS 직원명, DAYNAME(jikwonibsail) AS 요일, busername AS 부서명, busertel AS 부서전화 FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno ORDER BY 요일;
SELECT * FROM v_exam3;

CREATE OR REPLACE VIEW v_test AS SELECT jikwonname AS 직원명, DAYNAME(jikwonibsail) AS 요일, COUNT(*) AS 직원수, busername AS 부서명, busertel AS 부서전화 FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno GROUP BY 요일 having 요일 IS NOT null;
SELECT * FROM v_test WHERE 직원수 = (SELECT MAX(직원수) FROM v_test);
SELECT * FROM v_test;

-- 강사님 풀이
CREATE OR REPLACE VIEW v_exam3 AS 
SELECT jikwonname AS 직원명, DATE_FORMAT(jikwonibsail, '%W') AS 요일, busername AS 부서명, busertel AS 부서전화 FROM jikwon LEFT OUTER JOIN buser ON busernum = buserno WHERE DATE_FORMAT(jikwonibsail, '%W') = (SELECT DATE_FORMAT(jikwonibsail, '%W') FROM jikwon GROUP BY DATE_FORMAT(jikwonibsail, '%W') HAVING COUNT(*) = (SELECT COUNT(*) FROM jikwon GROUP BY DATE_FORMAT(jikwonibsail, '%W') ORDER BY COUNT(*) DESC LIMIT 1));

SELECT * FROM v_exam3;

