const csrf = document.querySelector('input[name=csrfmiddlewaretoken]').value;

// Render the PayPal button
paypal.Buttons({
  createOrder: function(data, actions) {
    return fetch('/api/orders/create-paypal-order/', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrf,
        'csrfmiddlewaretoken': csrf
      }
    }).then(function(res) {
      return res.json();
    }).then(function(data) {
      return data.order_id;
    });
  },
  onApprove: function(data, actions) {
    return fetch('/api/orders/capture-paypal-order/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
        'csrfmiddlewaretoken': csrf
      },
      body: JSON.stringify({
        "order_id": data.orderID,
      })
    }).then(function(res) {
      // Handle success
      location.href = '/success/'
    }).catch(function(err) {
      // Handle errors
      location.href = '/failure/'
    });
  },
  style: {
    shape: 'rect',
  }
}).render('#paypal-button-container');

window.addEventListener('DOMContentLoaded', ()=> {
  if (document.querySelector('.products__empty')) {
    let container = document.querySelector('#paypal-button-container');
    container.style.opacity = 0.75;
    container.style.pointerEvents = 'none';
  }
})