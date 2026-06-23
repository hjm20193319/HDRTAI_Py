/**
 * $ 함수: document.querySelector를 짧게 줄여서 사용하기 위한 헬퍼 함수 (화살표 함수 문법)
 * (sel) => ... : 매개변수가 하나일 때 괄호 생략 가능, 한 줄 코드일 때 return 키워드와 중괄호 생략 가능
 */
const $ = (sel) => document.querySelector(sel); 

// DOM 요소들을 한 번에 찾아 변수(객체)에 담아두고, 이후에 편하게 쓰려고 만든 요소 캐싱 패턴.
// els는 각 DOM 요소를 key-value로 모아 둔 객체 변수명. els.code, els.sang 이렇게 호출
// const: 재할당이 불가능한 상수를 선언할 때 사용 (객체 내부의 속성 값은 변경 가능)
const els = {
  // key: value 형태의 객체 리터럴 문법
  code: $("#code"), 
  sang: $("#sang"), 
  su: $("#su"), 
  dan: $("#dan"),
  msg: $("#msg"),
  tbody: $("#tbody"),
  btnAdd: $("#btnAdd"), btnUpdate: $("#btnUpdate"), btnDelete: $("#btnDelete"), 
  btnClear: $("#btnClear"),
  btnReload: $("#btnReload"),
};

// <div id="msg" class="msg">메시지 영역</div>에 메세지 출력용 함수
function setMsg(text, isError = false) {
  els.msg.textContent = text;
  els.msg.classList.toggle("error", isError);   // msg 요소에 error 클래스를 조건에 따라 붙이거나 뗌
     // classList.toggle(클래스명, 조건) 형태는
     // 조건이 true면 → 해당 클래스를 추가(add), 조건이 false면 → 해당 클래스를 제거(remove)
     // isError가 true일 때 CSS에서 정의한 .error 스타일이 적용됨
     // textContent: 요소 내의 텍스트 콘텐츠를 설정하거나 반환 (HTML 태그는 해석하지 않음)
}

// 입력 폼의 값들을 객체 형태로 반환하는 함수
function getForm() {
  return {
    // 객체 리터럴 반환: 함수 호출 시 현재 input들의 상태를 스냅샷처럼 찍어서 객체로 만듦
    code: els.code.value.trim(), // trim(): 문자열 양 끝의 공백을 제거하여 유효성 검사 용이하게 함
    sang: els.sang.value.trim(),
    su: els.su.value.trim(),
    dan: els.dan.value.trim(),
  };
}

function clearForm() {
  els.code.value = "";
  els.sang.value = "";
  els.su.value = "";
  els.dan.value = "";
  setMsg("초기화 완료");
}

// 서버에서 받은 상품 목록(rows)을 tr로 만들어서 테이블 tbody에 한 번에 뿌려주는 함수
// 결과는 [ "<tr ...>...</tr>", "<tr ...>...</tr>", ... ]
function renderRows(rows) {
  // map(): 배열의 각 요소를 순회하며 새로운 형태(HTML 문자열)로 변환
  // 템플릿 리터럴(``): 백틱을 사용하여 문자열 내부에 변수(${...})를 직접 삽입 가능
  // join(""): 생성된 배열의 요소들을 하나의 문자열로 합침
  els.tbody.innerHTML = rows.map(r => `
    <tr data-code="${r.code}">
      <td>${r.code}</td>
      <td>${r.sang ?? ""}</td> 
      <td>${r.su ?? ""}</td>
      <td>${r.dan ?? ""}</td> 
    </tr>` ).join("");
}
// ?? (Nullish coalescing operator): 왼쪽 피연산자가 null 또는 undefined일 때만 오른쪽 값을 반환
// <tr data-code="${r.code}"> : tr(한 행)에 data-code="1" 같은 커스텀 데이터 속성을 달아둔다.
// 나중에 '행 클릭했을 때 code를 쉽게 꺼내기'에 좋음. 예: tr.dataset.code 로 읽음

// async : 이 함수 안에서 await를 쓸 수 있게 해주는 표시임. 이 함수는 호출하면 즉시 Promise를 반환
async function loadAll() {
  setMsg("조회 중..."); // 사용자 경험(UX)을 위해 로딩 상태 표시
try {
   // 서버 API로 GET 요청을 보내고, 응답이 올 때까지 기다린 다음 그 응답 객체를 res에 담는 코드
   // await: 비동기 작업(Promise)이 완료될 때까지 함수의 실행을 일시 중지함
 // fetch()는 HTTP 요청을 보내는 브라우저 내장 함수
 // fetch의 기본 method는 'GET'임
 // window 객체: 브라우저의 전역 객체로, 어디서든 접근 가능한 변수나 함수를 담고 있음
 // window.API_LIST는 index.html에서 주입한 API 주소:<script>window.API_LIST = ...</script>
   // 아래 코드를 통해 브라우저가 GET /api/sangdata 요청을 보냄
    const res = await fetch(window.API_LIST, { 
      headers: { "Accept": "application/json" } // 서버에게 JSON 형태의 응답을 원한다고 알림
    });

    // 서버 응답(res)의 본문(body)을 “JSON으로 읽어서” 자바스크립트 객체로 변환.
    const data = await res.json();
    // res.ok: HTTP 상태 코드가 200-299 범위인지 확인하는 불리언 속성
    // throw: 의도적으로 에러를 발생시켜 catch 블록으로 제어권을 넘김
    if (!res.ok || data.ok === false) throw new Error(data.error || "조회 실패");

    renderRows(data.data);  // tbody에 결과 출력 함수 호출
    setMsg(`조회 완료: ${data.data.length}건`);
  } catch (e) {
    // try 블록 내에서 에러 발생 시 catch 블록으로 이동하여 예외 처리 (네트워크 에러, 파싱 에러 등)
    setMsg(`조회 오류: ${e.message}`, true);
  }
}

// 추가
async function addOne() {
  const f = getForm();   // form tag의 입력된 자료 읽기 함수 호출
  if (!f.code || !f.sang) return setMsg("code, sang는 필수!", true); // Early Return: 필수값 없으면 중단
  try {
    const res = await fetch(window.API_LIST, {
      method: "POST", // 리소스 생성을 위한 HTTP 메서드
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify( {    // stringify : JS 객체/배열을 JSON 문자열로 변환 (네트워크 전송용)
        // Number(): 문자열을 숫자로 변환 (산술 연산이나 DB 타입을 맞추기 위함)
        // || (논리 OR 연산자): 왼쪽 값이 falsy(빈 문자열 등)일 때 오른쪽의 0을 선택 (단축 평가)
        code: Number(f.code),
        sang: f.sang,
        su: Number(f.su || 0),
        dan: Number(f.dan || 0),
      } )
    } );
    
    // HTTP 응답(res)의 본문(body)을 끝까지 읽어서 JSON으로 파싱한 뒤, 그 결과가 나올 때까지 대기
    const data = await res.json();
    // 서버에서 반환한 JSON에 ok: false가 포함되어 있을 경우 에러 처리
    if (!res.ok || data.ok === false) throw new Error(data.error || "추가 실패");

    setMsg(`추가 완료: code=${data.code}`);
    await loadAll();   // loadAll()이 반환하는 Promise가 resolve/reject 될 때까지 대기.
  } catch (e) {
    setMsg(`추가 오류: ${e.message}`, true);
  }
}

// 수정
async function updateOne() {
  const f = getForm();
  if (!f.code) return setMsg("수정하려면 code가 필요!", true);

  try {
    // 템플릿 리터럴(`${}`)을 사용하여 URL 경로에 수정할 대상의 ID(code)를 포함
    // RESTful API 설계 원칙: /api/sangdata/100 과 같이 경로에 식별자를 포함
    const res = await fetch(`${window.API_LIST}/${Number(f.code)}`, {
      method: "PUT", // 전체 수정을 의미하는 HTTP 메서드
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify( {
        sang: f.sang,
        su: Number(f.su || 0),
        dan: Number(f.dan || 0),
      })
    } );
    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.error || "수정 실패");

    setMsg(`수정 완료: code=${data.code}`);
    await loadAll();
  } catch (e) {
    setMsg(`수정 오류: ${e.message}`, true);
  }
}

// 삭제
async function deleteOne() {
  const f = getForm();
  if (!f.code) return setMsg("삭제하려면 code가 필요!", true);

  // confirm(): 사용자에게 확인/취소 선택창을 띄움 (취소 시 함수 종료)
  // 사용자의 실수로 인한 데이터 삭제를 방지하는 기본적인 방어 코드
  if (!confirm(`code=${f.code}를 삭제할까요?`)) return; 

  try {
    const res = await fetch(`${window.API_LIST}/${Number(f.code)}`, { // 삭제 대상을 URL에 명시
      method: "DELETE", // 리소스 삭제를 위한 HTTP 메서드
      headers: { "Accept": "application/json" }
    });
    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.error || "삭제 실패");

    setMsg(`삭제 완료: code=${data.code}`);
    clearForm();
    await loadAll();
  } catch (e) {
    setMsg(`삭제 오류: ${e.message}`, true);
  }
}

// 행 클릭 → 폼 채우기
els.tbody.addEventListener("click", (e) => {
  // 이벤트 위임(Event Delegation): 개별 td가 아닌 부모 tbody에 이벤트를 걸어 효율적으로 관리
  // closest(): 클릭된 요소(e.target)에서 상위로 올라가며 가장 가까운 tr 요소를 찾음
  const tr = e.target.closest("tr"); 
  if (!tr) return; // tr이 아닌 곳(여백 등)을 클릭했을 경우 무시
  
  const tds = tr.querySelectorAll("td"); // 해당 행의 모든 열(td)을 가져옴
  els.code.value = tds[0].textContent; // 첫 번째 td의 텍스트를 code 입력창에 할당
  els.sang.value = tds[1].textContent;
  els.su.value = tds[2].textContent;
  els.dan.value = tds[3].textContent;
  setMsg(`선택됨: code=${els.code.value}`);
});

// 버튼 이벤트 장착
// addEventListener: 하나의 요소에 여러 이벤트를 등록할 수 있는 현대적인 방식
els.btnReload.addEventListener("click", loadAll);
els.btnClear.addEventListener("click", clearForm);
els.btnAdd.addEventListener("click", addOne);
els.btnUpdate.addEventListener("click", updateOne);
els.btnDelete.addEventListener("click", deleteOne);

// 최초 로딩 시 전체조회
// DOMContentLoaded: HTML 문서가 완전히 로드되고 파싱되었을 때 발생 (이미지 등 무거운 리소스 대기 안 함)
window.addEventListener("DOMContentLoaded", loadAll);