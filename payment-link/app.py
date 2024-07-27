#! /usr/bin/env python3.10
__fname = 'app'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')

# testing stripe payment link intgration w/ simple webhook (no-code)
#  ref: https://github.com/stripe/stripe-cli/wiki/installation
#  ref: https://docs.stripe.com/no-code/payment-links
#  ref: https://dashboard.stripe.com/payment-links/create/customer-chooses-pricing
#  ref: https://dashboard.stripe.com/test/webhooks/create?endpoint_location=hosted

#------------------------------------------------------------#
#   IMPORTS
#------------------------------------------------------------#
from sites_env import env #required: sites_env/__init__.py
import stripe
from flask import Flask, request
import sys, time, os, traceback
from datetime import datetime

#------------------------------------------------------------#
#   GLOBALS
#------------------------------------------------------------#
DEBUG_PRINT_LEVEL = 1
PORT = 4242
kSTRIPE_PUBLIC = env.STRIPE_PUB_KEY
kSTRIPE_SECRET = env.STRIPE_EP_SEC_LOC
# YOUR_DOMAIN = 'http://localhost:4242'

#------------------------------------------------------------#
#   INIT FLASK                                         
#------------------------------------------------------------#
app = Flask(__name__,
            static_url_path='',
            static_folder='public')

#------------------------------------------------------------#
#   ENDPOINT SUPPORT                                         
#------------------------------------------------------------#
# This endpoint will handle the webhook
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers['STRIPE_SIGNATURE']
    endpoint_secret = kSTRIPE_SECRET
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

#------------------------------------------------------------#
#   DEFAULT SUPPORT                                          
#------------------------------------------------------------#
READ_ME = f'''
{cStrDivider_1}
    *DESCRIPTION*
        stripe payment-link integration testing

    *INSTALL* (stripe CLI _ MacOSx)
        $ $ brew install stripe/stripe-cli/stripe

    *INSTALL* (stripe CLI _ linux/ubuntu)
        $ sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net:80 --recv-keys 379CE192D401AB61
        $ echo "deb https://dl.bintray.com/stripe/stripe-cli-deb stable main" | sudo tee -a /etc/apt/sources.list
        $ sudo apt-get update
        $ sudo apt-get install stripe
        
    *RUN* (python direct)
        $ python3.10 {__filename}

    *RUN* (flask embedded)
        $ cd .../{os.path.basename(os.getcwd())}
        $ export FLASK_APP={__filename}
        $ python3.10 -m flask run --port={PORT}

    *RUN* (input params)
        nil
{cStrDivider_1}
'''

#ref: https://stackoverflow.com/a/1278740/2298002
def print_except(e, debugLvl=0):
    #print(type(e), e.args, e)
    if debugLvl >= 0:
        print('', cStrDivider, f' Exception Caught _ e: {e}', cStrDivider, sep='\n')
    if debugLvl >= 1:
        print('', cStrDivider, f' Exception Caught _ type(e): {type(e)}', cStrDivider, sep='\n')
    if debugLvl >= 2:
        print('', cStrDivider, f' Exception Caught _ e.args: {e.args}', cStrDivider, sep='\n')
    if debugLvl >= 3:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        strTrace = traceback.format_exc()
        print('', cStrDivider, f' type: {exc_type}', f' file: {fname}', f' line_no: {exc_tb.tb_lineno}', f' traceback: {strTrace}', cStrDivider, sep='\n')

def print_wait_dots():
    global RESP_RECEIVED
    while not RESP_RECEIVED:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)  # Adjust sleep duration as needed
        
def wait_sleep(wait_sec : int, b_print=True, bp_one_line=True): # sleep 'wait_sec'
    print(f'waiting... {wait_sec} sec')
    for s in range(wait_sec, 0, -1):
        if b_print and bp_one_line: print(wait_sec-s+1, end=' ', flush=True)
        if b_print and not bp_one_line: print('wait ', s, sep='', end='\n')
        time.sleep(1)
    if bp_one_line and b_print: print() # line break if needed
    print(f'waiting... {wait_sec} sec _ DONE')

def get_time_now(dt=True):
    if dt: return '['+datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-4]+']'
    return '['+datetime.now().strftime("%H:%M:%S.%f")[0:-4]+']'

def read_cli_args():
    print(cStrDivider_1)
    print(f'read_cli_args...\n # of args: {len(sys.argv)}\n argv lst: {str(sys.argv)}')
    for idx, val in enumerate(sys.argv): print(f' argv[{idx}]: {val}')
    print('read_cli_args _ DONE')
    print(cStrDivider_1, '\n')
    return sys.argv, len(sys.argv)

if __name__ == "__main__":
    ## start ##
    RUN_TIME_START = get_time_now()
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\n'+READ_ME)
    lst_argv_OG, argv_cnt = read_cli_args()
    
    ## exe ##
    try:
        # This test secret API key is a placeholder. Don't include personal details in requests with this key.
        # To see your test secret API key embedded in code samples, sign in to your Stripe account.
        # You can also find your test secret API key at https://dashboard.stripe.com/test/apikeys.
        # stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
        stripe.api_key = kSTRIPE_PUBLIC
        app.run(port=PORT)

    except Exception as e:
        print_except(e, debugLvl=DEBUG_PRINT_LEVEL)
    
    ## end ##
    print(f'\n\nRUN_TIME_START: {RUN_TIME_START}\nRUN_TIME_END:   {get_time_now()}\n')

print('', cStrDivider, f'# END _ {__filename}', cStrDivider, sep='\n')