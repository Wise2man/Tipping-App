import hashlib

# PayFast configuration
PAYFAST_MERCHANT_ID = '10035640'  # Replace with your PayFast merchant ID
PAYFAST_MERCHANT_KEY = 'njtokoc5074bx'  # Replace with your PayFast merchant key
PAYFAST_PASSPHRASE = 'your_passphrase'  # Replace with your actual passphrase
PAYFAST_URL = 'https://sandbox.payfast.co.za/eng/process'  # Use the live URL for production

def generate_payfast_url(amount, username, name_first, email):
    # Create a payload for PayFast
    payload = {
        'merchant_id': PAYFAST_MERCHANT_ID,
        'merchant_key': PAYFAST_MERCHANT_KEY,
        'amount': amount,
        'item_name': 'Tip Payment',
        'return_url': 'http://your-return-url.com',  # Your return URL
        'cancel_url': 'http://your-cancel-url.com',
        'notify_url': 'http://your-server-url.com/notify',  # Your notification URL
        'name_first': name_first,
        'email_address': email,
    }
    
    # Generate the signature
    param_string = '&'.join(f"{key}={value}" for key, value in payload.items() if value)
    param_string += f"&passphrase={PAYFAST_PASSPHRASE}"
    signature = hashlib.md5(param_string.encode()).hexdigest()
    
    # Add the signature to the payload
    payload['signature'] = signature
    
    # Construct the PayFast URL
    payfast_url = PAYFAST_URL + '?' + '&'.join(f"{key}={value}" for key, value in payload.items())
    return payfast_url
import hashlib

# PayFast configuration
PAYFAST_MERCHANT_ID = '10035640'  # Replace with your PayFast merchant ID
PAYFAST_MERCHANT_KEY = 'njtokoc5074bx'  # Replace with your PayFast merchant key
PAYFAST_PASSPHRASE = 'your_passphrase'  # Replace with your actual passphrase
PAYFAST_URL = 'https://sandbox.payfast.co.za/eng/process'  # Use the live URL for production

def generate_payfast_url(amount, username, name_first, email):
    # Create a payload for PayFast
    payload = {
        'merchant_id': PAYFAST_MERCHANT_ID,
        'merchant_key': PAYFAST_MERCHANT_KEY,
        'amount': amount,
        'item_name': 'Tip Payment',
        'return_url': 'http://your-return-url.com',  # Your return URL
        'cancel_url': 'http://your-cancel-url.com',
        'notify_url': 'http://your-server-url.com/notify',  # Your notification URL
        'name_first': name_first,
        'email_address': email,
    }
    
    # Generate the signature
    param_string = '&'.join(f"{key}={value}" for key, value in payload.items() if value)
    param_string += f"&passphrase={PAYFAST_PASSPHRASE}"
    signature = hashlib.md5(param_string.encode()).hexdigest()
    
    # Add the signature to the payload
    payload['signature'] = signature
    
    # Construct the PayFast URL
    payfast_url = PAYFAST_URL + '?' + '&'.join(f"{key}={value}" for key, value in payload.items())
    return payfast_url
