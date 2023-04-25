function getQuantity(productElement) {
  return parseInt(productElement.querySelector('.quantity input[type="number"]')?.value);
}
function getSKU(productElement) {
  return parseInt(productElement.querySelector('input[name="inStock"')?.value);
}
function getCart() {
  let arr = [];
  for (let productElement of document.querySelectorAll('.products > .product')) {
    let quantity = getQuantity(productElement);
    let sku = getSKU(productElement);
  }
}

paypal.Buttons({
  style: {
      layout: 'horizontal',
      color: 'black',
      shape: 'rect',
      label: 'paypal',
      height: 43,
      borderRadius: 0
  },
  // Order is created on the server and the order id is returned
  createOrder() {
    return fetch("/my-server/create-paypal-order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // use the "body" param to optionally pass additional order information
      // like product skus and quantities
      body: JSON.stringify({
        cart: getCart(),
      }),
    })
      .then((response) => response.json())
      .then((order) => order.id);
  },
  // Finalize the transaction on the server after payer approval
  onApprove(data) {
    return fetch("/my-server/capture-paypal-order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        orderID: data.orderID
      })
    })
      .then((response) => response.json())
      .then((orderData) => {
        // Successful capture! For dev/demo purposes:
        console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
        const transaction = orderData.purchase_units[0].payments.captures[0];
        alert(`Transaction ${transaction.status}: ${transaction.id}\n\nSee console for all available details`);
        // When ready to go live, remove the alert and show a success message within this page. For example:
        // const element = document.getElementById('paypal-button-container');
        // element.innerHTML = '<h3>Thank you for your payment!</h3>';
        // Or go to another URL:  window.location.href = 'thank_you.html';
      });
  }
}).render('#paypal-button-container');

setTimeout(()=>{document.querySelector('#paypal-button-container .paypal-button.paypal-button-shape-rect').style.borderRadius=0;})