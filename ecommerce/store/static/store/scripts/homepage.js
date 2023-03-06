import * as base from './base.js';

let scene = document.querySelector('.welcome-section__sheath > .image-container');
const sheathParallax = new Parallax(scene);


const fillProductsSwiper = (products, swiper) => {
    var slides = []
    var cond;
    switch (true) {
        case window.innerWidth >= 1440:
            cond = 4;
            break;
        case window.innerWidth >= 768:
            cond = 2;
            break;
        case window.innerWidth >= 1:
            cond = 1;
            break;
    }

    for (let i = 0; i < 16; i++) {
        var container;
        if (i === 0 || i % cond === 0) {
            var slide = document.createElement('div');
            slide.classList.add('swiper-slide');
            container = document.createElement('div');
            container.classList.add('products-row');
        }
        base.appendProductCard(container, products[i]);
        slide.appendChild(container);
        slides.push(slide);
      }
    swiper.appendSlide(slides);
}
const fillBrandnewProductsSwiper = (products, swiper) => {
    var slides = []
    var cond;
    switch (true) {
        case window.innerWidth >= 1440:
            cond = 3;
            break;
        case window.innerWidth >= 768:
            cond = 2;
            break;
        case window.innerWidth >= 1:
            cond = 1;
            break;
    }

    for (let i = 0; i < 9; i++) {
        if (i === 0 || i % cond === 0) {
            var slide = document.createElement('div');
            var container = document.createElement('div');
            slide.classList.add('swiper-slide')
            container.classList.add('products-row')
            slide.append(container)
            slides.push(slide);
        }
        base.appendProductCard(container, products[i]);
    }
    swiper.appendSlide(slides);
}

const bestsellerSwiper = new Swiper('.bestsellers-section .swiper', {
    // Optional parameters
    loop: true,
    spaceBetween: 1024,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },
});

let products = await base.pullProducts("ordering=sold&limit=16")
fillProductsSwiper(products, bestsellerSwiper);


for (let [i, brandnewContainer] of Object.entries(document.querySelectorAll('.brandnew-section__swiper-container'))) {
    let swipe = new Swiper(brandnewContainer.querySelector('.product-swiper'), {
        // Optional parameters
        loop: true,
        spaceBetween: 1024,

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
        },
    });
    products = await base.pullProducts(`ordering=created_at&limit=9&offset=${i * 9}`)
    fillBrandnewProductsSwiper(products, swipe)
}

for (let [i, discountedContainer] of Object.entries(document.querySelectorAll('.discounted-section'))) {
    let swipe = new Swiper(discountedContainer.querySelector('.product-swiper'), {
        // Optional parameters
        loop: true,
        spaceBetween: 1024,

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
        },
    });
    products = await base.pullProducts(`/api/product/?discount__gte=0&limit=16&offset=${i * 16}`)
    fillProductsSwiper(products, swipe);
}

let flashlightProducts = await fetch(`/api/flashlight/?limit=16`).then(resp => resp.json()).then(data => data['results']);
let flashlightSwiper = new Swiper('.product-section_flashlight .product-swiper', {
    loop: true,
        spaceBetween: 1024,

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
        },
})
fillProductsSwiper(flashlightProducts, flashlightSwiper);

for (let swiper of document.querySelectorAll('.swiper')) {
    swiper = swiper.swiper;
    swiper.slideTo(1, 100);
}