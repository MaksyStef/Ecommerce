import { appendProductCard } from "./base.js"


// Fill product cards
let products = JSON.parse(JSON.parse(document.querySelector('#products').textContent));
var container = document.querySelector('.products-list');
for (let product of products) {
    let item = document.createElement('li');
    item.classList.add('products-item', 'row', 'flex-center');
    appendProductCard(item, product);
    container.append(item);
}


// Create range filters
const rangeInputs = document.querySelectorAll(".range-input"),
    numberInputs = document.querySelectorAll(".number-input"),
    priceGap = 2;
const addRangeEventListener = input => {
    input.addEventListener("input", e => {
        let minRangeInput = input.firstElementChild,
            maxRangeInput = input.lastElementChild,
            minVal = parseInt(minRangeInput.value),
            maxVal = parseInt(maxRangeInput.value),
            range = input.parentElement.querySelector('.slider');
        if ((maxVal - minVal) < priceGap) {
            if (e.target.className === "range-min") {
                minRangeInput.value = maxVal - priceGap
            } else {
                maxRangeInput.value = minVal + priceGap;
            }
        } else {
            input.parentElement.querySelector('.number-input .field:first-child input').value = minRangeInput.value;
            input.parentElement.querySelector('.number-input .field:last-child input').value = maxRangeInput.value;
            range.style.paddingLeft = ((minVal / minRangeInput.getAttribute('max')) * 100) + "%";
            range.style.paddingRight = 100 - (maxVal / maxRangeInput.getAttribute('max')) * 100 + "%";
        }
    });
}
const addNumberEventListener = input => {
    input.addEventListener("input", e => {
        let minNumberInput = input.firstElementChild.firstElementChild,
            maxNumberInput = input.lastElementChild.firstElementChild,
            minPrice = parseInt(minNumberInput.value),
            maxPrice = parseInt(maxNumberInput.value),
            range = input.parentElement.querySelector('.slider');

        if ((maxPrice - minPrice >= priceGap) && (maxPrice <= maxNumberInput.getAttribute('max')) && (minPrice >= minNumberInput.getAttribute('min'))) {
            if (e.target.className === "input-min") {
                input.parentElement.querySelector('.range-input input:first-child').value = minPrice;
                range.style.paddingLeft = ((minPrice / minNumberInput.getAttribute('max')) * 100) + "%";
            } else {
                input.parentElement.querySelector('.range-input input:last-child').value = maxPrice;
                range.style.paddingRight = 100 - (maxPrice / maxNumberInput.max) * 100 + "%";
            }
        } else {
            if (e.target.className === "input-min") {
                minNumberInput.value = minNumberInput.getAttribute('min');
            } else {
                maxNumberInput.value = maxNumberInput.getAttribute('max');
            }
        }
    });
}
rangeInputs.forEach(addRangeEventListener);
numberInputs.forEach(addNumberEventListener);


// Add event listeners for filter details
const detailsList = document.querySelectorAll(".filter");
for (let details of detailsList) {
    details.addEventListener("click", e => {
        if (e.target === details.querySelector('summary')) {
            if (details.hasAttribute("open")) {
                e.preventDefault();
                details.classList.add("closing");
                setTimeout(() => {
                    details.removeAttribute("open");
                    details.classList.remove("closing");
                }, 200);
            }
        }
    })

    if (details.classList.contains('filter_checkbox') && !(details.classList.contains('filter_rating'))) {
        // Set --height var individually for checkbox filters
        details.lastElementChild.style.setProperty(
            "--height",
            `${details.lastElementChild.childElementCount * 28 + 14}px`)
    }
}