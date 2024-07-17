#! /usr/bin/env python3.10
__fname = 'server'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
from sites_env import env #required: sites_env/__init__.py

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, jsonify, redirect, request

import stripe
# This test secret API key is a placeholder. Don't include personal details in requests with this key.
# To see your test secret API key embedded in code samples, sign in to your Stripe account.
# You can also find your test secret API key at https://dashboard.stripe.com/test/apikeys.
# stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
# stripe.api_key = STRIPE_PUBLISHABLE_KEY
stripe.api_key = env.STRIPE_PUB_KEY

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

# testing stripe payment link intgration w/ simple webhook (no-code)
#  ref: https://docs.stripe.com/no-code/payment-links
#  ref: https://dashboard.stripe.com/payment-links/create/customer-chooses-pricing
#  ref: https://dashboard.stripe.com/test/webhooks/create?endpoint_location=hosted
# This endpoint will handle the webhook
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers['STRIPE_SIGNATURE']
    # endpoint_secret = STRIPE_ENDPOINT_SECRET_LOCAL
    endpoint_secret = env.STRIPE_EP_SEC_LOC
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    print('EVENT TYPE: {}'.format(event['type']))
    print(f'PAYLOAD ...\n {payload}')
    print(cStrDivider, cStrDivider, sep='\n')
    print()
    # # Handle the checkout.session.completed event
    # if event['type'] == 'checkout.session.completed' or event['type'] == 'payment_intent.succeeded':
    #     session = event['data']['object']
        
    #     # Retrieve custom fields
    #     custom_fields = session.get('metadata', {})

    #     # You can now use custom_fields as needed
    #     print('printing custom_fields ...')
    #     print(custom_fields)

    return '', 200
    # return jsonify(success=True)

# testing stripe checkout integration ("low-code payment form")
#  ref: https://docs.stripe.com/payments/checkout
#  ref: https://checkout.stripe.dev/preview
#  ref: https://docs.stripe.com/checkout/embedded/quickstart?lang=python
#  ref: https://docs.stripe.com/payments/accept-a-payment?platform=web&ui=embedded-form#create-product-prices-upfront
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    print(f'ENTER - create_checkout_session()')
    try:
        PRICE_ID = 'pr_1234'
        session = stripe.checkout.Session.create(
            ui_mode = 'embedded',
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': f'{PRICE_ID}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url=YOUR_DOMAIN + '/return.html?session_id={CHECKOUT_SESSION_ID}',
        )
    except Exception as e:
        print(f'e - create_checkout_session() ...')
        print(e)
        print()
        return str(e)

    print(f'EXIT - create_checkout_session()')
    return jsonify(clientSecret=session.client_secret)

@app.route('/session-status', methods=['GET'])
def session_status():
  print(f'ENTER - session_status()')
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))

  return jsonify(status=session.status, customer_email=session.customer_details.email)

if __name__ == '__main__':
    app.run(port=4242)