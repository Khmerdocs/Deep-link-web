import random
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

# @app.route('/checkout')
# def checkout_page():
#     return render_template('checkout.html')

# identity_code = 32
# purpose_of_transaction = 3162  # Assuming it starts from P0003123

# Generate random values for identity code and purpose of transaction
identity_code = random.randint(1, 9999999)  # Adjust the range as needed
purpose_of_transaction = random.randint(1, 9999999)

@app.route('/checkout', methods=['POST','GET'])
def checkout_page():
    global identity_code, purpose_of_transaction

    # Increment identity code and purpose of transaction by 1
    identity_code += 1
    purpose_of_transaction += 1

    # Convert integers to strings with leading zeros
    identity_code_str = str(identity_code).zfill(4)
    purpose_of_transaction_str = "P" + str(purpose_of_transaction).zfill(7)

    # Static data to be sent in the request
    data = {
        "identity_code": identity_code_str,
        "purpose_of_transaction": purpose_of_transaction_str,
        "device_code": "679812",
        "description": "TEST",
        "currency": "USD",
        "amount": 1.2,
        "language": "km",
        "cancel_url": "",
        "redirect_url": "www.exampleshop.com",
        "channel_code": "CH1",
        "user_ref": "001",
        "customers": [
            {
                "branch_code": "PP",
                "branch_name": "Phnom Penh",
                "customer_code": "C0001",
                "customer_name": "nana",
                "customer_name_latin": "Sapientia Potentia Est",
                "bill_no": "T0001",
                "amount": 1.2
            }
        ]
    }
    
    # Token for authorization (replace 'YOUR_BILLER_TOKEN' with your actual token)
    biller_token = 'a358cdff7990403580f430b026943fd3'

    # API endpoint
    api_url = 'https://merchantapi-demo.bill24.io/transaction/v2/init'

    # Request headers
    headers = {'token': biller_token}

    # Send POST request to external API with static data
    response = requests.post(api_url, json=data, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the response JSON
        response_data = response.json()

        # Extract the tran_id from the response if response_data is not None
        if response_data is not None:
            tran_id = response_data.get('data', {}).get('tran_id')
            # Print the tran_id
            print("Transaction ID:", tran_id)
        else:
            return jsonify({'error': 'Empty response from API'}), 500

        # Pass tran_id to the checkout.html template
        return render_template('checkout.html', tran_id=tran_id)
    else:
        # If request failed, return an error response
        return jsonify({'error': 'Failed to initialize SDK'}), response.status_code
    

if __name__ == '__main__':
    app.run(debug=False)
