from paystack.resource import TransactionResource

import random
import string

rand = ''.join(
        [random.choice(
            string.ascii_letters + string.digits) for n in range(16)])
secret_key = 'sk_test_c7f5d0f0a3a4ed4a499d47185d25b217d62a638c'
random_ref = rand
test_email = 'abiodunajao01@gmail.com'
test_amount = 1000
client = TransactionResource(secret_key, random_ref)
response = client.initialize(test_amount,
                             test_email)
print(response)
client.authorize() # Will open a browser window for client to enter card details
#verify = client.verify() # Verify client credentials
#print(verify)
#print(client.charge()) # Charge an already exsiting client


