export const authenticated = JSON.parse(document.querySelector("#authenticated")?.textContent);
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
    if (authenticated === true) {
        await fetch('/product/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body:
                `{
                    "product_id": ${cardId.value},
                    "rating" : ${rating},
                }`,
        });
        let personalRating = cardId.parentElement.querySelector('.product-card__personal-rating')
        if (cardId.parentNode.contains(personalRating) === true) {
            personalRating.value = rating
        } else {
            personalRating = document.createElement('input')
            personalRating.type = 'hidden';
            personalRating.value = rating;
            personalRating.classList.add('product-card__personal-rating');
            cardId.parentNode.appendChild(personalRating);
        }
        setStars(rating, cardRating);
    }
}
export function appendProductCard(container, product) {
    let template = document.querySelector('#product-card-template').content.cloneNode(true);
    // Define card and it's parts
    let card = template.querySelector('.product-card'),
        cardId = template.querySelector('.product-card__id'),
        cardImage = template.querySelector('.product-card__image img'),
        cardTitle = template.querySelector('.product-card__row_title h2'),
        cardSize = template.querySelector('.product-card__size h3'),
        cardMaterials = template.querySelector('.product-card__materials h3'),
        cardRating = template.querySelector('.product-card__rating'),
        cardPersonalRating = template.querySelector('.product-card__personal-rating'),
        cardRateCount = template.querySelector('.product-card__rate-count h3'),
        cardPrice = template.querySelector('.product-card__price h3');
    // Fill card's parts
    cardId.setAttribute('value', product['rating']);
    cardImage.parentElement.href = product['url'];
    let imageSource = (product['images'].length > 0) ? product['images'].keys()[0] : 'https://www.discountcutlery.net/assets/images/NewProductImages/FOX620B.jpg';
    cardImage.setAttribute('src', imageSource);
    cardTitle.innerText = product["title"];
    cardSize.innerText = product["size"];
    cardMaterials.innerText = product["materials"];
    product['personal_rating'] ? cardPersonalRating.value = product['personal_rating'] : null;
    cardRateCount.innerText = product["votes_count"] + " votes";
    cardPrice.innerText = product["price"] + "$";

    let stars = cardRating.querySelectorAll('.rate');
    for (let [ind, star] of Object.entries(stars)) {
        star.addEventListener('click', async () => await rate(Number(ind) + 1, cardRating, cardId))
    }
    cardPersonalRating.value != 0 ? setStars(product['personal_rating'], cardRating) : setStars(product['rating'], cardRating);

    container.appendChild(card);
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