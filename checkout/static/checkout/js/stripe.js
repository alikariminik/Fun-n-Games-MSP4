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
    $('#payment-form').fadeToggle(100);
    $('#processing-overlay').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
              name: $.trim(form.full_name.value),
              phone: $.trim(form.phone_number.value),
              email: $.trim(form.email.value),
              address:{
                  line1: $.trim(form.street_address1.value),
                  line2: $.trim(form.street_address2.value),
                  city: $.trim(form.town_or_city.value),
                  country: $.trim(form.country.value),
                  state: $.trim(form.county.value),
              }
          }
      },
      shipping: {
          name: $.trim(form.full_name.value),
          phone: $.trim(form.phone_number.value),
          address: {
              line1: $.trim(form.street_address1.value),
              line2: $.trim(form.street_address2.value),
              city: $.trim(form.town_or_city.value),
              country: $.trim(form.country.value),
              postal_code: $.trim(form.postcode.value),
              state: $.trim(form.county.value),
          }
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
            $('#payment-form').fadeToggle(100);
            $('#processing-overlay').fadeToggle(100);
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

