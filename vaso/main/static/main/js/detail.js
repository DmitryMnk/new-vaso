import {Swiper} from '../package/swiper-bundle.min.mjs';
import { openModal, toggleModal } from "./catalog_functions.js";
import { phoneInputCorrecting, sendCodeAPI } from "./base.js";

const openModalButton = document.querySelectorAll('.catalog__open-modal');
const modal = document.querySelector('.modal');
const closeModalButton = document.querySelector('.modal-close-button');
const phoneInput = document.querySelector('.detail-phone-input');
const phoneInputHidden = document.querySelector('.detail-phone-input-hidden');
const nameInput = document.getElementById('name-input');
const nameInputHidden = document.getElementById('name-input-hidden');
const addressInput = document.getElementById('address-input');
const addressInputHidden = document.getElementById('address-input-hidden');
const detailMessage = document.querySelector('.detail-message');
const detailMessageHidden = document.querySelector('.detail-message-hidden');
const checkCode = document.getElementById('check-code');

const part1 = document.getElementById('label-code-input-one');
const part2 = document.getElementById('label-code-input-two');
const part3 = document.getElementById('label-code-input-three');
const part4 = document.getElementById('label-code-input-four');


openModalButton.forEach(element => element.addEventListener('click', (e) => {
    var isError = false;
    e.preventDefault();

    if (phoneInput.value == '' || nameInput.value == '' || addressInput.value == '') {
        isError = true;
    }

    if (!isError) {
        console.log('awdad')
        openModal(modal, phoneInput.value, detailMessage);
    } else {
        detailMessage.textContent = 'Заполните все поля';
        detailMessage.classList.add('message-error');
    }
}));


phoneInput.addEventListener('input', () => {
    phoneInputCorrecting(phoneInput);
    console.log('awdsd')
})

checkCode.addEventListener('click', () => {
    if (part1.value == '' || part2.value == '' || part3.value == '' || part4.value == '') {
        detailMessage.textContent = 'Введите код'
        return;
    }
    
    const code = part1.value + part2.value + part3.value + part4.value;

    sendCodeAPI('../../users/api/check_auth_code/', {'code': code}).then(response => {
        if (response.data.error) {
            checkMessage.textContent = response.data.error
        } else {
            window.location = response.data.href;
        }
    })
})

closeModalButton.addEventListener('click', () => {
    toggleModal(modal);
})



