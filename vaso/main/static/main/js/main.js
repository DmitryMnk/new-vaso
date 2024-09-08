import { sendCodeAPI, getCSRF, getScrollbarWidth, phoneInputCorrecting } from "./base.js";

const openModalAccountButton = document.querySelector('.user-account-button');
const openModalFormButton = document.querySelector('.user-form-button');
const closeModalButton = document.querySelector('.close-modal-button');
const modalBack = document.querySelector('.auth-block-back');
const authModal = document.querySelector('.auth-block');
const phoneInput = document.querySelector('.auth-block__phone-input');
const sendCode = document.querySelector('.auth-block__send-code');
const sendMessage = document.getElementById('send-message');
const checkMessage = document.getElementById('check-message');
const sendForm = document.querySelector('.auth-block__send-form');
const checkForm = document.querySelector('.auth-block__check-form');
const checkCode = document.getElementById('check-code');
const subTitlePhone = document.getElementById('sub-title-phone');

const part1 = document.getElementById('label-code-input-one');
const part2 = document.getElementById('label-code-input-two');
const part3 = document.getElementById('label-code-input-three');
const part4 = document.getElementById('label-code-input-four');


function closeModal() {
    modalBack.classList.remove('modal-back--active');
    authModal.classList.remove('modal--active');
    setTimeout(() => {
        modalBack.style.display = 'none';
        document.body.style.paddingRight = '0';
        document.body.style.overflow = 'auto';
    }, 300)
}

function openModal() {
    modalBack.style.display = 'block';
    const scrollWidth =  getScrollbarWidth();
    document.body.style.paddingRight = scrollWidth + 'px';
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
        modalBack.classList.add('modal-back--active');
        authModal.classList.add('modal--active')
    }, 20)
}

function changeBlocks(activeBlock, hideBlock) {
    activeBlock.style.display = 'none';
    activeBlock.classList.remove('step-block--active');
    hideBlock.style.display = 'flex';
    setTimeout(() => {
        hideBlock.classList.add('step-block--active');

    }, 20)    
}

openModalAccountButton.addEventListener('click', () => {
    localStorage.setItem('account', 1)
    openModal();
})

openModalFormButton.addEventListener('click', () => {
    localStorage.setItem('account', 0)
    openModal();
})


modalBack.addEventListener('click', () => {
    closeModal();
})


phoneInput.addEventListener('input', () => {
    phoneInputCorrecting(phoneInput);
})

phoneInput.addEventListener('blur', () => {
    const value = phoneInput.value;
    if (value.startsWith('8')) {
        phoneInput.value = '+7' + value.slice(1, value.length);
    }

})

phoneInput.addEventListener('focus', () => {
    const value = phoneInput.value;
    if (value == '') {
        phoneInput.value = '+7';
    }
})

sendCode.addEventListener('click', () => {
    var error = false;

    if (phoneInput.value.startsWith('+7') && phoneInput.value.length != 12) {
        error = true;
    } else if (phoneInput.value.startsWith('8') && phoneInput.value.length != 11) {
        error = true;
    } else if (phoneInput.value.length < 11) {
        error = true;
    }

    if (error) {
        sendMessage.textContent = 'Неверный формат телефона'
    } else {
        const request_data = {'phone': phoneInput.value}
        const account = localStorage.getItem('account');
        sendCodeAPI('users/api/send_auth_code/', request_data).then(response => {
            if (response.response.ok) {
                sendMessage.textContent = '';
                subTitlePhone.textContent = phoneInput.value;
                changeBlocks(sendForm, checkForm);
            } else {
                sendMessage.textContent = 'Что-то пошло не так. Попробуйте снова.';
            }
        })
    }
})

checkCode.addEventListener('click', () => {
    if (part1.value == '' || part2.value == '' || part3.value == '' || part4.value == '') {
        checkMessage.textContent = 'Введите код'
        return;
    }
    
    const code = part1.value + part2.value + part3.value + part4.value;
    const account = localStorage.getItem('account');
    const request_data = {'code': code, 'account': account}
    sendCodeAPI('users/api/check_auth_code/', {'code': code}).then(response => {
        if (response.data.error) {
            checkMessage.textContent = response.data.error
        } else {
            if (account == 1){

                window.location = 'users/account/';
            } else {
                window.location = 'catalog/create_bouquet/';
            }            
        }
    })

    
})