from flask import Flask, request
from flask import jsonify
import requests


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency']
    amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]


    cf=fetch_conversion_factor(source_currency,target_currency)

    if cf:
        final_amount = amount*cf
        response_text="{} {} is {:.2f} {}".format(amount,source_currency,final_amount,target_currency)
    else:
        response_text = "Conversion rate not available for {} to {}".format(source_currency,target_currency)

    response={
        'fulfillmentText': response_text
    }
    print("Response to Dialogflow:",response)
    return jsonify(response)

def fetch_conversion_factor(source,target):

    url=f'https://v6.exchangerate-api.com/v6/c976cf1376e2ab79cc198c4d/latest/{source}'
    response= requests.get(url)
    if response.status_code==200:
        response=response.json()
        conversion_rates= response.get('conversion_rates',{})
        return conversion_rates.get(target)

    return None


if __name__ == "__main__":
    app.run(debug=True)
