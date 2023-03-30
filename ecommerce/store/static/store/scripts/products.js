import * as base from './base.js';


// Fill product cards
const baseUrl = location.protocol+"//"+location.host+JSON.parse(document.querySelector("#ApiUrl")?.textContent); // Get API URL
var apiParams = new URLSearchParams(); // String of additional query parameters

const limit = 24; // Number of items to display per page
let currentPage = 1;
let totalItemsCount = await fetch(baseUrl + "total-count").then(response => response.json());
totalItemsCount = totalItemsCount['total_count']


// Helper function to fetch data from the API and update the UI
function updatePage() {
    apiParams.set("offset", (currentPage-1)*limit); // Set offset
    
    // Create apiUrl
    let apiUrl = new URL(baseUrl);
    apiUrl.search = apiParams.toString();
    console.log(apiUrl.toString());
    // Refill product list
    fetch(apiUrl.toString())
    .then(res => res.json())
    .then(data => {
            const products = data.results;
            const productList = document.querySelector('.products-list');
            productList.innerHTML = ""; // Clear out previous results
            for (let product of products) {
                // Create HTML element(s) to display each product, e.g.:
                base.appendProductCard(productList, product)
            }
            updatePagination();
        })
        .catch(error => console.error(error));
}

// Helper function to update the pagination links at the bottom of the page
function updatePagination() {
    const totalPages = Math.ceil(totalItemsCount / limit);
    const paginationContainer = document.querySelector('.products__pagination');
    paginationContainer.innerHTML = ''; // Clear out previous pagination links
    // Add "Previous" link if not on first page
    if (currentPage > 1) {
        const previousLink = document.createElement('a');
        previousLink.innerText = '« Previous';
        previousLink.href = '#';
        previousLink.addEventListener('click', () => {
            currentPage--;
            updatePage();
        });
        paginationContainer.appendChild(previousLink);
    }
    // Add numbered page links
    for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('a');
        pageLink.innerText = i;
        pageLink.href = '#';
        pageLink.className = i === currentPage ? 'active' : '';
        pageLink.addEventListener('click', () => {
            currentPage = i;
            updatePage();
        });
        paginationContainer.appendChild(pageLink);
    }
    // Add "Next" link if not on last page
    if (currentPage < totalPages) {
        const nextLink = document.createElement('a');
        nextLink.innerText = 'Next »';
        nextLink.href = '#';
        nextLink.addEventListener('click', () => {
            currentPage++;
            updatePage();
        });
        paginationContainer.appendChild(nextLink);
    }
}
updatePage(); // Initial call to fetch and display the first page of results

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
            const totalRange = maxRangeInput.max - minRangeInput.min;
            const leftPadding = ((minVal - maxRangeInput.min) / totalRange) * 100;
            const rightPadding = ((maxRangeInput.max - maxVal) / totalRange) * 100;
            range.style.paddingLeft  = `${leftPadding}%`;
            range.style.paddingRight = `${rightPadding}%`;
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


// Filters system
function toggleSubcatsExcludeParam(e) {
    // Get the value of the "subcat-id" input field of the parent element
    const subcatId = e.target.parentElement.querySelector('input[name="subcat-id"]').value;

    // Add the "rating_exclude" parameter to the URL string with the subcatId value
    if (urlParams.length > 0) { // if any other params and not 
        urlParams += "&";
    }
        
    const myRegex = /exclude_subcats=\d+(,\d+)*/;
    const match = urlParams.match(myRegex);

}
for (let filterCat of document.querySelectorAll('.filterCat')) {
    filterCat.onclick = toggleSubcatsExcludeParam
}

function filterButtons(e) {

}