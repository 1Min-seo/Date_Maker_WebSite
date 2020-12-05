/*elements */ 
const form = document.getElementById('form');
const user_name = document.getElementById('inputName');
const user_id = document.getElementById('inputId');
const user_passwd = document.getElementById('inputPassword');
const inputTag = document.getElementsByClassName('input');


/* e handler */
form.addEventListener('submit',checkForm);
user_name.addEventListener('click',clickEvent);
user_id.addEventListener('click',clickEvent);
user_passwd.addEventListener('click',clickEvent);
user_passwd.addEventListener('click',passwdEvent); 
/* reset */
user_name.value='이름을 입력해 주세요';
user_id.value = '아이디를 입력해 주세요';
user_passwd.value ='비밀번호를 입력해 주세요'; 
user_passwd.type = 'text';

/* func */ 

function spaceCheck(value){
    if(value.search(/\s/) != -1){
        return true;
    }else{
        return false;
    }
}

function checkForm(e) {

    const check1 =  /[0-9]/;    //숫자 포함 여부
    const check2 = /[a-zA-Z]/;  //문자 포함 여부
    const check3 =  /[~!@#$%^&*()_+|<>?:{}]/;  //특수문자 포함 여부
    var  isSubmit = true
    
    // 이름 유효성 검사 
    if(user_name.value.length<2 || check1.test(user_name.value) || check3.test(user_name.value)){
        isSubmit  = false;
        user_name.value = '숫자와 특수 문자는 포함하실 수 없습니다.';
        user_name.style.backgroundColor = '#ffe0e0';
    }

    // 아이디 유효성 검사 
    if(user_id.value.length < 6 || !check1.test(user_id.value) || check3.test(user_id.value)){
        isSubmit  = false; 
        user_id.value = '아이디는 6자 이상 문자와 숫자로 구성해 주세요';
        user_id.style.backgroundColor = '#ffe0e0';
    }

    // 비밀번호 유효성 검사 
    if(user_passwd.value.length<8 || !check1.test(user_passwd.value) || !check2.test(user_passwd.value)){
        isSubmit  = false; 
        user_passwd.type = 'text';
        user_passwd.value = '8자 이상 문자,숫자,특수문자로 구성해 주세요';
        user_passwd.style.backgroundColor = '#ffe0e0';
    }
    if(!isSubmit){
        e.preventDefault();
    }
  
}
function clickEvent(e){
    e.target.value = '';
    e.target.style.backgroundColor = 'white';
}
function passwdEvent(e){
    e.target.type ='password' ;
}

