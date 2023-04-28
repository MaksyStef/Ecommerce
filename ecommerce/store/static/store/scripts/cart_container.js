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
    return fetch('/api/orders/create_payment/', {
      method: 'put',
      headers: {
        'X-CSRFToken': csrf
      }
    }).then(function(res) {
      return res.json();
    }).then(function(data) {
      return data.id;
    });
  },
  onApprove: function(data, actions) {
    return fetch('/api/orders/execute_payment/', {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf
      },
      body: JSON.stringify({
        "order_id": data.orderID,
      })
    }).then(function(res) {
      // Handle success
    }).catch(function(err) {
      // Handle errors
    });
  },
  style: {
    shape: 'rect',
  }
}).render('#paypal-button-container');