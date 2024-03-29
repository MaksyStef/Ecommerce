import { appendProductCard, pullProducts } from "./base.js";
// Image gallery init
const scrollerContainer = document.querySelector('.product__thumbnail-images');
const scrollSpeed = 1;

// initialize variables to track the starting position of the user's mouse drag
let isDragging = false;
let startX, scrollLeft;

// add event listeners for mouse down, mouse up, and mouse move events
scrollerContainer.addEventListener('mousedown', e => {
    isDragging = true;
    startX = e.pageX - scrollerContainer.offsetLeft;
    scrollLeft = scrollerContainer.scrollLeft;
});

scrollerContainer.addEventListener('mouseup', () => {
    isDragging = false;
});

scrollerContainer.addEventListener('mousemove', e => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - scrollerContainer.offsetLeft;
    const walk = (x - startX) * scrollSpeed; // adjust the scroll speed as needed
    scrollerContainer.scrollLeft = scrollLeft - walk;
});

// add event listeners for touch start, touch end, and touch move events
scrollerContainer.addEventListener('touchstart', e => {
    isDragging = true;
    startX = e.touches[0].pageX - scrollerContainer.offsetLeft;
    scrollLeft = scrollerContainer.scrollLeft;
});

scrollerContainer.addEventListener('touchend', () => {
    isDragging = false;
});

scrollerContainer.addEventListener('touchmove', e => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.touches[0].pageX - scrollerContainer.offsetLeft;
    const walk = (x - startX) * scrollSpeed; // adjust the scroll speed as needed
    scrollerContainer.scrollLeft = scrollLeft - walk;
});

const mainImage = document.querySelector('.product__main-image img');
const thumbnails = document.querySelector('.product__thumbnail-images');

const updateProductImage = clicked => {
    thumbnails.querySelector('.active')?.classList.toggle('active');
    clicked.classList.toggle('active');
    mainImage.classList.add('disappear');
    setTimeout(() => {
        mainImage.src = clicked.firstElementChild.src;
        mainImage.classList.remove('disappear');
    })
}
updateProductImage(thumbnails.firstElementChild)

for (let el of thumbnails.children) { // set onclick for thumbnail images 
    el.onclick = e => updateProductImage(el);
}

// Get cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrf = getCookie('csrftoken') // CSRF Token for API access
const authenticated = JSON.parse(document.querySelector("#authenticated").textContent);

// Rating system init
const changeStar = (image, type = 'fill') => {
    let path = '/static/store/images/icons/';
    switch (type) {
        case 'empty':
            image.setAttribute('src', path + 'emptystar-icon.svg')
            break;
        case 'half':
            image.setAttribute('src', path + 'halfstar-icon.svg')
            break;
        default:
            image.setAttribute('src', path + 'star-icon.svg')
            break
    }
}
const setStars = (value, container) => {
    const fillSpan = (from, to) => {
        const floatPart = (value - Math.floor(value))

        const span = Object.values(container.children).slice(from, to)
        span.forEach(
            star => star.querySelector('img').setAttribute('src', `/static/store/images/icons/star-icon.svg`)
        )
        if (to !== -1) {
            Object.values(container.children).slice(to).forEach(
                star => changeStar(star.querySelector('img'), 'empty')
            )
        }
        if (0.3 < floatPart) {
            changeStar(container.children[to].querySelector('.rating-star'), 'half')
        }
        if (0.6 < floatPart) {
            changeStar(container.children[to].querySelector('.rating-star'), 'fill')
        }
    }
    // If rating is n.3-...-n.7, we fill n stars, half fill 1 star and the rest remain empty
    switch (Math.floor(value)) {
        case 1:
            fillSpan(0, 1)
            break;
        case 2:
            fillSpan(0, 2)
            break;
        case 3:
            fillSpan(0, 3)

            break;
        case 4:
            fillSpan(0, 4)

            break;
        case 5:
            fillSpan(0, 5)
            break
        default:
            break;
    }
}
export const rate = async (rating, productId) => {
    if (authenticated === true) {
        await fetch(`/api/product/${productId.value}/rate/`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                'Accept': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify({
                "value": rating,
            }),
        });
        let personalRating = document.querySelector('.product__personal-rating');

        if (document.contains(personalRating) === true) {
            personalRating.value = rating;
        } else {
            personalRating = document.createElement('input');
            personalRating.type = 'hidden';
            personalRating.value = rating;
            personalRating.classList.add('product__personal-rating');
            productId.parentNode.appendChild(personalRating);
        }
        setStars(rating, container);
    }
}
const rating = document.querySelector('.product__personal-rating') ? document.querySelector('.product__personal-rating') : document.querySelector('.product__rating');
const productId = document.querySelector('.product__id');
let container = document.querySelector('.product__stars');
for (let star = 0; star < container.children.length; star++) {
    let el = container.children[star];
    el.onclick = e => rate(star + 1, productId);
}
setStars(rating.value, container);

// Init Favourite system
const toggleFavourite = async toggler => {
    let id = document.querySelector('.product__id').value;
    await fetch(`/api/product/${id}/toggle-favourite/`, {
        method: "PUT",
        headers: {'X-CSRFToken': csrf}
    })
    toggler.parentElement.classList.toggle('toggled');
}

let toggler = document.querySelector('.favourite-toggler')
for (let btn of toggler.children) { // set onclick for favourite buttons 
    btn.onclick = () => toggleFavourite(btn);
}

// Init Cart system
const toggleCart = async toggler => {
    var id = document.querySelector('.product__id').value;
    await fetch(`/api/product/${id}/toggle-cart/`, { 
        method: "PUT", 
        headers: { 'X-CSRFToken':  csrf }
    })
    var cartCounter = document.querySelector('.page-header .cart-btn'),
        purchaseCount = Number(cartCounter.getAttribute('purchase-count')),
        purchaseSummary = document.querySelector('#purchase-summary'),
        priceAmount = Number(purchaseSummary.textContent),
        productPrice = Number(document.querySelector('.product__price span').textContent);

    toggler.classList.toggle('toggled');
    
    if (toggler.classList.contains('toggled')) {
        toggler.innerHTML = `Remove from cart <img src="/static/store/images/icons/cart-icon.svg" alt="cart-icon">`;
        cartCounter.setAttribute('purchase-count', purchaseCount + 1);
        purchaseSummary.textContent = (priceAmount + productPrice).toFixed(2);
    } else { 
        toggler.innerHTML = `Add to the cart <img src="/static/store/images/icons/cart-icon.svg" alt="cart-icon">`;
        cartCounter.setAttribute('purchase-count', purchaseCount - 1);
        purchaseSummary.textContent = (priceAmount - productPrice).toFixed(2);
    }
}
toggler = document.querySelector('.action-container_4 .btn-orange');
toggler.onclick = () => toggleCart(toggler);

// Dropdown menus init
const dropdownHeaders = document.querySelectorAll(".dropdown-header");

dropdownHeaders.forEach(dropdownHeader => {
    let dropdownMenu = dropdownHeader.nextElementSibling;
    dropdownHeader.addEventListener("click", () => {
        dropdownMenu.classList.toggle("active");
        dropdownHeader.classList.toggle("active");
    });
    dropdownMenu.addEventListener("click", (event) => {
        const selectedOption = event.target;
        dropdownHeader.textContent = selectedOption.textContent;
        dropdownHeader.setAttribute('data-subcat', selectedOption.getAttribute('data-subcat'));
        dropdownMenu.classList.remove("active");
        dropdownHeader.classList.remove("active");
    });
})

// Product quantity init
const quantityInput = document.querySelector(".quantity-input");
const priceSpan = document.querySelector(".product__price span");
const bonusPoints = document.querySelector(".product__additional-bonus-points");
const basePrice = parseFloat(document.querySelector(".product__base-price").value);
let quantity = parseInt(quantityInput.value).toFixed(2);

const updatePrice = () => {
    priceSpan.textContent = basePrice * quantity;
    if (parseInt(priceSpan.textContent) <= 0) {
        priceSpan.textContent = basePrice;
        quantity = 1;
    }
    bonusPoints.textContent = (basePrice * quantity * 0.05).toFixed(2);
}
quantityInput.addEventListener("change", () => {
    quantity = parseInt(quantityInput.value ? quantityInput.value : 1);
    updatePrice();
});
document.querySelector('.minus-btn').onclick=() => {
    quantity--; 
    updatePrice();
    quantityInput.value = quantity;
}
document.querySelector('.plus-btn').onclick=() => {
    quantity++; 
    updatePrice();
    quantityInput.value = quantity;
}
updatePrice();

// Create sliders
const fillProductsSwiper = (products, swiper) => {
    for (let i = 0; i < 8; i++) {
        var container = document.createElement('div');
        appendProductCard(container, products[i]);
        container.classList.add('swiper-slide', 'row', 'flex-center');
        swiper.appendSlide(container);
    }
}
let suggestions = await pullProducts(`${productId.value}/suggestions`);
let swiper = new Swiper(`.swiper_1`, {
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
fillProductsSwiper(suggestions, swiper);

let buyAltogether = await pullProducts(`${productId.value}/buy-altogether`);
swiper = new Swiper(`.swiper_2`, {
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
fillProductsSwiper(buyAltogether, swiper);