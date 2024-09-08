const switchBlocks = document.querySelectorAll('.create-step');
var activeBlock = document.querySelector('.create-step--active');
var blockButtons = document.querySelectorAll('.catalog__form-block-button');


blockButtons.forEach(item => item.addEventListener('click', (e) => {
    e.preventDefault();
    const parent = item.parentNode.parentNode
    const message = parent.querySelector('.catalog__form-block-message');


    if (parent.classList.contains('create-step--active')) {
        const elemId = parseInt(item.id.split('-')[3]);

        const validation = validateStep(elemId, parent, message);
        if (!validation) {
            return;
        }

        const nextBlock = document.getElementById(`step-block-${elemId + 1}`);

        parent.classList.remove('create-step--active');
        setTimeout(() => {
            parent.style.display = 'none';
            nextBlock.style.display = 'flex'; 
        }, 200)
        setTimeout(() => {
            nextBlock.classList.add('create-step--active');
        }, 220)

    }

}))

function validateStep(elemId, parent, message) {
    if (elemId == 1 || elemId == 2) {
        const inputs = parent.querySelectorAll('input');
        var accept = false;
        for (const inp of inputs) {
            if (inp.checked) {
                accept = true;
                break;
            }
        }
        if (!accept) {
            if (elemId == 2) {
                message.textContent = 'Необходимо выбрать тип  упаковки'
            } else if (elemId == 1) {
                message.textContent = 'Необходимо выбрать хотя бы 1 цвет'
            }
            
        }
        return accept
    }

    if (elemId == 3 || elemId >= 5) {
        const input = parent.querySelector('input');

        if (input.value == '') {
            message.textContent = 'Необходимо заполнить поле'
            return false
        }

        if (elemId == 3 && input.value < 5000) {
            message.textContent = 'Сумма должна составлять не менее 5000р.'
            return false
        }

        return true
    }
    return true

}