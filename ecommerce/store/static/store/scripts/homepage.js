import * as base from './base.js';

let scene = document.querySelector('.welcome-section__sheath > .image-container');
const sheathParallax = new Parallax(scene);


let bestsellerProducts = JSON.parse(JSON.parse(document.querySelector('#bestsellers').textContent))
const bestsellerSwiper = new Swiper('.bestsellers-section .swiper', {
    // Optional parameters
    loop: true,
    spaceBetween: 1024,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },
});
let fillProductsSwiper = (products, swiper) => {
    var slides = []
    var cond;
    if (window.matchMedia('(min-width:0px)').matches) {
        cond = 1;
    }
    if (window.matchMedia('(min-width:768px)').matches) {
        cond = 2;
    }
    if (window.matchMedia('(min-width:1440px)').matches) {
        cond = 4;
    }

    for (const [index, product] of products.entries()) {
        if (index === 0 || index % cond === 0) {
            var slide = document.createElement('div');
            var container = document.createElement('div');
            slide.classList.add('swiper-slide')
            container.classList.add('products-row')
            slide.append(container)
            slides.push(slide);
        }
        base.appendProductCard(container, product);
    }
    swiper.appendSlide(slides);
}
let fillBrandnewProductsSwiper = (products, swiper) => {
    var slides = []
    var cond;
    if (window.matchMedia('(min-width:0px)').matches) {
        cond = 1;
    }
    if (window.matchMedia('(min-width:768px)').matches) {
        cond = 2;
    }
    if (window.matchMedia('(min-width:1440px)').matches) {
        cond = 3;
    }

    for (const [index, product] of products.entries()) {
        if (index === 0 || index % cond === 0) {
            var slide = document.createElement('div');
            var container = document.createElement('div');
            slide.classList.add('swiper-slide')
            container.classList.add('products-row')
            slide.append(container)
            slides.push(slide);
        }
        base.appendProductCard(container, product);
    }
    swiper.appendSlide(slides);
}
fillProductsSwiper(bestsellerProducts, bestsellerSwiper);


let brandnewProducts = [],
    brandnewSwiperContainers = document.querySelectorAll('.brandnew-section__swiper-container');

brandnewProducts.push(JSON.parse(JSON.parse(document.querySelector('#brandnew_1').textContent)));
brandnewProducts.push(JSON.parse(JSON.parse(document.querySelector('#brandnew_2').textContent)));

for (let [index, products] of brandnewProducts.entries()) {
    let swipe = new Swiper(brandnewSwiperContainers[index].querySelector('.product-swiper'), {
        // Optional parameters
        loop: true,
        spaceBetween: 1024,

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
        },
    });
    fillBrandnewProductsSwiper(products, swipe)
}

let discountedProducts = [],
    discountedSwiperContainers = document.querySelectorAll('.discounted-section');

discountedProducts.push(JSON.parse(JSON.parse(document.querySelector("#discounted_1").textContent)));
discountedProducts.push(JSON.parse(JSON.parse(document.querySelector("#discounted_2").textContent)));
discountedProducts.push(JSON.parse(JSON.parse(document.querySelector("#discounted_3").textContent)));
discountedProducts.push(JSON.parse(JSON.parse(document.querySelector("#discounted_4").textContent)));

for (let [index, products] of discountedProducts.entries()) {
    let swipe = new Swiper(discountedSwiperContainers[index].querySelector('.product-swiper'), {
        // Optional parameters
        loop: true,
        spaceBetween: 1024,

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
        },
    });
    fillProductsSwiper(products, swipe);
}

let flashlightProducts = await fetch(
    '/api/products?supercategory_id=15&count=4&ordering=created_at',
    { method: 'GET', }
).then(
    response => response.json()
).then(
    json => JSON.parse(json)
)
var list = document.querySelector('.flashlights');
for (let product of flashlightProducts) {
    let item = document.createElement('li');
    item.classList.add('flashlight');
    base.appendProductCard(item, product);
    list.append(item);
}