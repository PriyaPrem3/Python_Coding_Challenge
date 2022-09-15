import requests
import csv
import time
import json

CURRENCIES_URL = 'https://api.coinbase.com/v2/currencies'
EXCHANGE_RATES_URL = 'https://api.coinbase.com/v2/exchange-rates?currency='
PRICES_URL = 'https://api.coinbase.com/v2/prices/BTC-'

def filterCurrency(currencies_dict, crncy_code):
    crncy_obj = [crncy for crncy in currencies_dict['data'] if crncy['id'].encode("ascii", "ignore") == crncy_code]
    return crncy_obj

def execute():
    crncy_code = str(raw_input("Please enter a valid currency:"))
    # client = Client('','')
    currencies_response = requests.get(CURRENCIES_URL)
    currencies_dict = currencies_response.json()
    # print("this step passed",currencies_dict)
    crncy_obj = filterCurrency(currencies_dict,crncy_code)
    if(bool(crncy_obj)):
        print "Currency Name:",crncy_obj[0]['name'].encode("ascii", "ignore")
        print "Currency Code:",crncy_obj[0]['id'].encode("ascii", "ignore")
    else:
        print "Unable to find the entered currency"
    
    crncy_code = str(raw_input("Please enter a valid currency to fetch exchange rates:"))
    exchange_rate_response = requests.get(EXCHANGE_RATES_URL+crncy_code)
    exch_rates_dict = exchange_rate_response.json()
    if(bool(exch_rates_dict)):
        fileName = crncy_code+'-exchange_output.'+str(time.time())+'.csv'
        output_file = open(fileName, 'w')
        csv_writer = csv.writer(output_file)
        exchange_rate_data = exch_rates_dict["data"]["rates"]
        header = ["base_currency_code", "base_currency", "currency_code", "currency", "exchange_rate"]
        csv_writer.writerow(header)
        for key in exchange_rate_data:
            curr_resp=filterCurrency(currencies_dict,key)
            currencyVal = curr_resp[0]['name'].encode("ascii", "ignore") if len(curr_resp) else ""
            output = ['USD','United States Dollar',key.encode(),currencyVal,exchange_rate_data[key].encode()]
            csv_writer.writerow(output)
        output_file.close()
        print "Output file generated successfully"
    else:
        print "Invalid Currency Specified"
    
    options = ["buy","sell","spot"]
    print "1. Buy BTC"
    print "2. Sell BTC"
    print "3. Spot BTC"
    selectedOption = int(raw_input("Please provide an option from above:"))
    selected_currency = str(raw_input("Please provide the currency to buy BTC in:"))
    if(selectedOption>3):
        print 'Invalid option selected.'
    else:
        filtered_curr_resp = filterCurrency(currencies_dict, selected_currency)
        if len(filtered_curr_resp):
            print PRICES_URL+selected_currency+'/'+options[selectedOption-1]
            priceResponse = requests.get(PRICES_URL+selected_currency+'/'+options[selectedOption-1])
            priceResponseVal = priceResponse.json()
            if len(priceResponseVal):
                print "This price of BTC in "+selected_currency+" is "+priceResponseVal['data']['amount']
            else:
                print "Sorry! No data is available"
            
        else:
            print "Invalid Currency provided"

execute()
