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
let csrf = getCookie('csrftoken');

// Render the PayPal button
paypal.Buttons({
  createOrder: function(data, actions) {
    return fetch('/api/orders/create-paypal-order/', {
      method: 'GET',
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
      method: 'PUT',
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
      console.log(err);
      // location.href = '/failure/'
    });
  },
  style: {
    shape: 'rect',
  }
}).render('#paypal-button-container');