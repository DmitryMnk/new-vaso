import { 
    getScrollbarWidth, 
    sendCodeAPI
} from "./base.js";
var is_animated = false;

function openModal(modal, phone, message) {

    const request_data = {'phone': phone}
    sendCodeAPI('../../users/api/send_auth_code/', request_data).then(response => {
        if (response.response.ok) {
            message.textContent = '';
            toggleModal(modal);
            modal.addEventListener('click', (e) => {
                if (e.target == modal) {
                    toggleModal(modal);
                }
            })
        } else {
            message.textContent = response.data.error;
        }
    })

}

function toggleModal(modal) {
    if (!is_animated) {
        is_animated = true;
        setTimeout(() => {
            is_animated = false;
        }, 300)
        if (modal.classList.contains('modal--active')) {
            document.body.style.overflow = 'auto'
            document.body.style.paddingRight = '0';
            modal.classList.toggle('modal--active');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 320)
        } else {
            const scrollbarWidth = getScrollbarWidth();
            document.body.style.overflow = 'hidden'
            document.body.style.paddingRight = scrollbarWidth + 'px';
            modal.style.display = 'flex';
            setTimeout(() => {
                modal.classList.toggle('modal--active');
            }, 20)
        }
    }
    
}

export {
    openModal,
    toggleModal
}