var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
  base: {
      color: '#000',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
          color: '#aab7c4'
      }
  },
  invalid: {
      color: '#dc3545',
      iconColor: '#dc3545'
  }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

card.addEventListener("change", function (event) {
  var errorDiv = document.getElementById("card-error");
  if (event.error) {
    var errorMessage = `
      <span class="icon" role="alert">
        <i class="fas fa-times"></i>
      </span>
      <span>${event.error.message}</span>
    `;
    $(errorDiv).html(errorMessage).addClass("text-danger");
  } else {
    errorDiv.textContent = ''
  }
});

var form = document.getElementById('payment-form');

form.addEventListener('btnSubmit ', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});
    $('#btnSubmit ').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html).addClass("text-danger");
            card.update({ 'disabled': false});
            $('#btnSubmit').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
              console.log(result.paymentIntent.status)
              form.submit();
            }
        }
    });
});
