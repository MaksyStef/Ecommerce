import * as base from './base.js';

let scene = document.querySelector('.welcome-section__sheath > .image-container');
const sheathParallax = new Parallax(scene);

const slideTo = () => {
    if (window.outerWidth >= 768) {
        return 2;
    } else if (window.outerHeight >= 1440) {
        return 4;
    } else if (window.outerHeight >= 2560) {
        return 8;
    } else {
        return 1;
    }
}
const fillProductsSwiper = (products, swiper) => {
    for (let i = 0; i < 16; i++) {
        var container = document.createElement('div');
        base.appendProductCard(container, products[i]);
        container.classList.add('swiper-slide', 'row', 'flex-center');
        swiper.appendSlide(container);
    }
    swiper.slideTo(slideTo(), 100);
}
const fillBrandnewProductsSwiper = (products, swiper) => {
    for (let i = 0; i < 9; i++) {
        var container = document.createElement('div');
        container.classList.add('swiper-slide', 'row', 'flex-center');
        base.appendProductCard(container, products[i]);
        swiper.appendSlide(container);
    }
    swiper.slideTo(slideTo(), 100);
}

const bestsellerSwiper = new Swiper('.bestsellers-section .swiper', {
    // Optional parameters
    loop: true,
    spaceBetween: 0,
    slidesPerView: 1,
    slidesPerGroup: 1,

    breakpoints: {
        768 : {
            slidesPerView: 2,
            slidesPerGroup: 2,
        },
        1440 : {
            slidesPerGroup: 4,
            slidesPerView: 4,
        },
        2560 : {
            slidesPerView: 8,
            slidesPerGroup: 8,
        },
    },
    pagination: {
        el: '.swiper-pagination',
    },
});

let products = await base.pullProducts("ordering=sold&limit=16");
fillProductsSwiper(products, bestsellerSwiper);


for (let [i, brandnewContainer] of Object.entries(document.querySelectorAll('.brandnew-section__swiper-container'))) {
    let swipe = new Swiper(brandnewContainer.querySelector('.product-swiper'), {
        // Optional parameters
        loop: true,
        spaceBetween: 0,
        slidesPerView: 1,

        breakpoints: {
            768 : {
                slidesPerView: 2,
            },
            1440 : {
                slidesPerGroup: 3,
                slidesPerView: 3,
            }

        },
        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
        },
    });
    products = await base.pullProducts(`ordering=created_at&limit=9&offset=${i * 9}`);
    fillBrandnewProductsSwiper(products, swipe);
}

for (let [i, discountedContainer] of Object.entries(document.querySelectorAll('.discounted-section'))) {
    let swipe = new Swiper(discountedContainer.querySelector('.product-swiper'), {
        // Optional parameters
        loop: true,
        spaceBetween: 0,
        slidesPerView: 1,
        slidesPerGroup: 1,
    
        breakpoints: {
            768 : {
                slidesPerView: 2,
                slidesPerGroup: 2,
            },
            1440 : {
                slidesPerGroup: 4,
                slidesPerView: 4,
            },
            2560 : {
                slidesPerView: 8,
                slidesPerGroup: 8,
            },
        },

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
    spaceBetween: 0,
    slidesPerView: 1,
    slidesPerGroup: 1,

    breakpoints: {
        768 : {
            slidesPerView: 2,
            slidesPerGroup: 2,
        },
        1440 : {
            slidesPerGroup: 4,
            slidesPerView: 4,
        },
        2560 : {
            slidesPerView: 8,
            slidesPerGroup: 8,
        },
    },
    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },
})
fillProductsSwiper(flashlightProducts, flashlightSwiper);


// for (let swiper of document.querySelectorAll('.swiper')) {
//     swiper = swiper.swiper;
// }