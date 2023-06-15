export const isAuthenticated= JSON.parse(document.querySelector("#authenticated")?.textContent);
export const changeStar = (image, type = 'fill') => {
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
export const setStars = (rating, cardRating) => {
    const fillSpan = (from, to) => {
        const floatPart = (rating - Math.floor(rating))

        const span = Object.values(cardRating.children).slice(from, to)
        span.forEach(
            star => star.querySelector('img').setAttribute('src', `/static/store/images/icons/star-icon.svg`)
        )
        if (to !== -1) {
            Object.values(cardRating.children).slice(to).forEach(
                star => changeStar(star.querySelector('img'), 'empty')
            )
        }
        if (0.3 < floatPart) {
            changeStar(cardRating.children[to].querySelector('.rating-star'), 'half')
        }
        if (0.6 < floatPart) {
            changeStar(cardRating.children[to].querySelector('.rating-star'), 'fill')
        }
    }
    // If rating is n.3-...-n.7, we fill n stars, half fill 1 star and the rest remain empty
    switch (Math.floor(rating)) {
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
export const rate = async (rating, cardRating, cardId) => {
    if (isAuthenticated=== true) {
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
        let csrf = getCookie('csrftoken')
        await fetch(`/api/product/${cardId.value}/rate/`, {
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
        var personalRating = cardId.parentElement.querySelector('.product-card__personal-rating'), 
            rateCount = cardId.parentElement.querySelector('.product-card__rate-count span');
        (personalRating.value!=='') ? function () {
            personalRating.value = rating;
        }() : function () {
            personalRating.remove();
            personalRating = document.createElement('input')
            personalRating.type = 'hidden';
            personalRating.setAttribute('value', rating);
            personalRating.classList.add('product-card__personal-rating');
            cardId.parentNode.appendChild(personalRating);
            rateCount.textContent = Number(rateCount.textContent) + 1;
        }();
        setStars(rating, cardRating);
    } else {
        location.href = `/account/sign?next=${location.href}`;
    }
}
export function appendProductCard(container, product) {
    var template = document.querySelector('#product-card-template').content.cloneNode(true),
        card = template.querySelector('.product-card');
    if (product) {
            // Define card and it's parts
            let cardId = template.querySelector('.product-card__id'),
            cardImage = template.querySelector('.product-card__image img'),
            cardTitle = template.querySelector('.product-card__row_title h2'),
            cardSize = template.querySelector('.product-card__size h3'),
            cardMaterials = template.querySelector('.product-card__materials h3'),
            cardRating = template.querySelector('.product-card__rating'),
            cardPersonalRating = template.querySelector('.product-card__personal-rating'),
            cardRateCount = template.querySelector('.product-card__rate-count h3'),
            cardPrice = template.querySelector('.product-card__price h3'),
            cardPurchaseButton = template.querySelector('.btn-orange'),
            favouriteToggler = template.querySelector('.product-card__row_composition .favourite-toggler');
        // Fill card's parts
        cardId.setAttribute('value', product['id']);
        cardImage.parentElement.href = product['url'];
        let imageSource = product['image_general'] ? product['image_general'] : '/static/store/images/icons/loading.gif';
        cardImage.setAttribute('src', imageSource); 
        cardTitle.innerText = product["title"];
        cardSize.innerText = product["size"];
        cardMaterials.innerText = product["materials"];
        product['personal_rating'] ? cardPersonalRating.value = product['personal_rating'] : null;
        cardRateCount.innerHTML = `<span>${product["votes_count"]}</span> votes`;
        cardPrice.innerHTML = `<span>${product["price"]}</span>€`;

        let stars = cardRating.querySelectorAll('.rate');
        for (let [ind, star] of Object.entries(stars)) {
            star.addEventListener('click', async () => await rate(Number(ind) + 1, cardRating, cardId))
        }
        product['personal_rating'] != 0 ? setStars(product['personal_rating'], cardRating) : setStars(product['rating'], cardRating);
        if (product['in_cart']) {
            cardPurchaseButton.innerHTML = `Remove from the cart <img src="/static/store/images/icons/cart-icon.svg" alt="cart-icon">`;
            cardPurchaseButton.classList.toggle('toggled');
        }
        product['in_favourite'] ? favouriteToggler.classList.toggle('toggled') : null;
        container.appendChild(card);
    } else {
        let cardStars = template.querySelector('.product-card__rating'),
            cardComposition= template.querySelector('.product-card__row_composition'),
            cardBuyButton = template.querySelector('.btn-orange'),
            cardImage = template.querySelector('.product-card__image img');
            cardStars.innerHTML = '';
            cardBuyButton.innerHTML = '';
            cardComposition.innerHTML = '';
            cardImage.style.visibility = 'hidden';
        container.appendChild(card);
    }
}
export const signNewsletter = () => {
    const email = document.querySelector('#newsletter-email');
    fetch(`/newsletters?action=sign`, {
        method: 'POST',
        body: JSON.stringify({
            email: email.value,
        })
    })
}
export const unsignNewsletter = () => {
    const email = document.querySelector('#newsletter-email');
    fetch(`/newsletters?action=unsign`, {
        method: 'POST',
        body: JSON.stringify({ email: email.value }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8;'
        }
    })
}
export const toggleNewsletter = (toggler) => {
    const sign = toggler.parentNode.querySelector('.newsletter-button_sign'),
        unsign = toggler.parentNode.querySelector('.newsletter-button_unsign');
    sign.classList.toggle('toggled');
    unsign.classList.toggle('toggled');

    let toChange = (toggler.parentNode.parentNode.parentNode.querySelector('.page-footer__item-link a')) ? toggler.parentNode.parentNode.parentNode.querySelector('.page-footer__item-link a') : undefined;
    if (unsign.classList.contains('toggled')) {
        toChange.innerText = 'Sign up now!';
    }
    else {
        toChange.innerText = 'Unsign newsletter';
    }
}
export const pullProducts = async (urlQuery) => await fetch(`/api/product/?${urlQuery}`)
                                                    .then(response => response.json())
                                                    .then(data => data.results)