// 각종 요소
// document.querySelector: CSS 선택자를 사용하여 DOM(Document Object Model) 요소에 접근
const code = document.querySelector('#code');
const sang = document.querySelector('#sang');
const su = document.querySelector('#su');
const dan = document.querySelector('#dan');

const msg = document.querySelector('#msg');
const tbody = document.querySelector('#tbody');

const btnAdd = document.querySelector('#btnAdd');
const btnUpdate = document.querySelector('#btnUpdate');
const btnDelete = document.querySelector('#btnDelete');
const btnReload = document.querySelector('#btnReload');

// 메시지 출력 함수
function setMsg(text) {
    msg.textContent = text;
}

// 입력 폼 초기화: input 요소들의 value 속성을 빈 문자열로 설정
function clearForm(){
    code.value = '';
    sang.value = '';
    su.value = '';
    dan.value = '';
}

// 전체 자료 읽기
// async/await: 비동기 처리를 동기적인 코드 흐름처럼 작성할 수 있게 해주는 문법
async function loadAll(){
    const res = await fetch('/api/sangdata'); // fetch: 네트워크 요청을 보내는 API (기본 GET 방식)
    const data = await res.json(); // .json(): 응답 본문을 JSON 객체로 파싱(변환)
    // console.log(data);
    // alert(data);

    tbody.innerHTML = ''; // 기존 테이블 내용 비우기

    // data.data: 서버에서 보낸 JSON 객체 내의 실제 데이터 배열
    data.data.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = '<td>' + r.code + '</td>' +
            '<td>' + r.sang + '</td>' +
            '<td>' + r.su + '</td>' +
            '<td>' + r.dan + '</td>';
        tbody.appendChild(tr);      // 자식으로 들어가게 됨
    });

    clearForm(); // 입력창 초기화
    setMsg('조회 완료');
}

// 추가
// POST 방식: 서버에 새로운 리소스를 생성할 때 사용
async function addData(){
    const data = {
        code:Number(code.value),        // 수치화 하고 싶을 때 Number( )
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    };
    // alert(data);

    const res = await fetch('/api/sangdata', {
        method:'POST',      // rest 방식에서는 post가 추가를 의미
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify(data)      // js 객체를 문자열로 변환해서 전송
    });

    await res.json();       // ok 값을 받아서 추가 성공, 추가 실패 등등을 if 문으로 실행하는 등의 내용을 더 추가할 수 있음(입력자료 오류 검사 등등)
    setMsg('추가 완료');
    clearForm();
    loadAll();      // 추가 후 전체 자료 보기
}

// 수정
// PUT 방식: 기존 리소스를 전체적으로 업데이트(수정)할 때 사용
async function updateData(){
    const data = {
        // 수치화 하고 싶을 때 Number( ), code는 수정 대상이 아님
        sang:sang.value,
        su:Number(su.value),
        dan:Number(dan.value)
    };
    // alert(data);

    // URL 파라미터로 수정할 대상의 code를 전달 (/api/sangdata/1)
    const res = await fetch('/api/sangdata/' + code.value, {
        method:'PUT',      // rest 방식에서는 put이 수정을 의미
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify(data)      // js 객체를 문자열로 변환해서 전송
    });

    const imsi = await res.json();
    if(imsi.ok)
        setMsg('수정 완료');
    else
        setMsg('수정 실패');
    
    clearForm();
    loadAll();      // 수정 후 전체 자료 보기
}

// 삭제
// DELETE 방식: 서버의 특정 리소스를 삭제할 때 사용
async function deleteData(){
    const res = await fetch('/api/sangdata/' + code.value, {
        method:'DELETE',      
    });
    
    const imsi = await res.json();
    if(imsi.ok)
        setMsg(imsi.msg);
    else
        setMsg('삭제 실패 : ' + imsi.msg);
    
    clearForm();
    loadAll();      // 삭제 후 전체 자료 보기
}

window.onload = loadAll;

btnAdd.onclick = addData;
btnUpdate.onclick = updateData;
btnDelete.onclick = deleteData;
btnReload.onclick = loadAll;