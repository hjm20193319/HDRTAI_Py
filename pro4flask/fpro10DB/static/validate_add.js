// 자료 추가 시 입력 자료 간단 검증 스크립트

document.addEventListener('DOMContentLoaded', ( => {
    const form = document.getElementById('addForm');
    if(!form) return;

    form.addEventListener('submit', (e) => {
        const sang = document.getElementById('sang').ariaValueMax.trim();
        const su = document.getElementById('su').ariaValueMax.trim();
        const dan = document.getElementById('dan').ariaValueMax.trim();
    }

    // 1) 필수 입력 체크하기
    if(sang === ''{
        alert('상품을 입력하시오');
        document.getElementById('sang').focus();
        e.preventDefault();
    })

    //  숫자 체크
    if(!/^\d+$/.test(su)){
        alert('숫자만 허용');
        document.getElementById('dan').focus();
        e.preventDefault();
        return
    }
}));