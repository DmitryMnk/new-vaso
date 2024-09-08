import {Swiper} from '../package/swiper-bundle.min.mjs';
const switcherButtons = document.querySelectorAll('.account__orders-switchers-button');
const swipers = document.querySelectorAll('.order-swiper');

document.addEventListener('DOMContentLoaded', () => {
    for (const swiper of swipers) {
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
    }
})


switcherButtons.forEach(item => item.addEventListener('click', () =>{
    if (!item.classList.contains('switch-button--active')) {
        const id = parseInt(item.id.split('-')[1]);
        const activeButton = document.querySelector('.switch-button--active');
        const activeBlock = document.querySelector('.switch-block--active');
        const nextBlock = document.getElementById(`switch-block-${id}`);

        activeBlock.classList.remove('switch-block--active');
        activeButton.classList.remove('switch-button--active');
        item.classList.add('switch-button--active');
        setTimeout(() => {
            activeBlock.style.display = 'none';
            nextBlock.style.display = 'block';
        }, 150)
        setTimeout(() => {
            nextBlock.classList.add('switch-block--active');
        }, 170)
    }
}))