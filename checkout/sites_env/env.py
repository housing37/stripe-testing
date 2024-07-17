__fname = 'env'
__filename = __fname + '.py'
cStrDivider = '#================================================================#'
cStrDivider_1 = '#----------------------------------------------------------------#'
print('', cStrDivider, f'GO _ {__filename} -> starting IMPORTs & declaring globals', cStrDivider, sep='\n')
#============================================================================#
## .env support
import os
from read_env import read_env

try:
    #ref: https://github.com/sloria/read_env
    #ref: https://github.com/sloria/read_env/blob/master/read_env.py
    read_env() # recursively traverses up dir tree looking for '.env' file
except:
    print("#==========================#")
    print(" ERROR: no .env files found ")
    print("#==========================#")

# stripe 'Publishable key' & 'Secret key'
# ref: https://dashboard.stripe.com/test/apikeys (acct created 07.15.24)
STRIPE_PUB_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']
STRIPE_SEC_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_EP_SEC_LOC = os.environ['STRIPE_ENDPOINT_SECRET_LOCAL']

#============================================================================#
