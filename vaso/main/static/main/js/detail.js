import {Swiper} from '../package/swiper-bundle.min.mjs';
import { openModal, toggleModal } from "./catalog_functions.js";
import { phoneInputCorrecting, sendCodeAPI, startInput } from "./base.js";

const swiper = document.querySelector('.swiper')
const openModalButton = document.querySelector('.open-modal');
const openModalButtonHidden = document.querySelector('.open-modal-hidden');
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


openModalButton.addEventListener('click', (e) => {
    var isError = false;
    console.log('Check modal open');
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
});

openModalButtonHidden.addEventListener('click', (e) => {
    var isError = false;
    console.log('Check modal open');
    e.preventDefault();

    if (phoneInputHidden.value == '' || nameInputHidden.value == '' || addressInputHidden.value == '') {
        isError = true;
    }

    if (!isError) {
        console.log('awdad')
        openModal(modal, phoneInputHidden.value, detailMessage);
    } else {
        detailMessage.textContent = 'Заполните все поля';
        detailMessage.classList.add('message-error');
    }
});


phoneInput.addEventListener('input', () => {
    phoneInputCorrecting(phoneInput);
})

phoneInput.addEventListener('focus', () => {
    startInput(phoneInput);
})

phoneInputHidden.addEventListener('input', () => {
    phoneInputCorrecting(phoneInputHidden);
})

phoneInputHidden.addEventListener('focus', () => {
    startInput(phoneInputHidden);
})


checkCode.addEventListener('click', (e) => {
    e.preventDefault();
    if (part1.value == '' || part2.value == '' || part3.value == '' || part4.value == '') {
        detailMessage.textContent = 'Введите код'
        return;
    }

    let name = nameInput.value;
    let address = addressInput.value;
    
    if (name == '') {
        name = nameInputHidden.value;
    }

    if (address == '') {
        address = addressInputHidden.value;
    }

    
    const code = part1.value + part2.value + part3.value + part4.value;

    const b_id = checkCode.dataset.bouquet;

    sendCodeAPI('../../users/api/check_code_and_pay/', {'code': code, 'id': b_id, 'name': name, 'address': address}).then(response => {
        console.log(response)
        if (response.data.error) {
            checkMessage.textContent = response.data.message
        } else {
            window.location.href = response.data.redirect_url;
        }
    })
})

closeModalButton.addEventListener('click', () => {
    toggleModal(modal);
})


new Swiper(swiper, {
    slidesPerView: 1,
    spaceBetween: 10,
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    loop: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },   
})

