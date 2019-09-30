"""mainapp.py: this script POSTs a payment object in JSON format to STACC API and retrieves a payment
breakdown plan. The payment plan is processed to a workable format and represented in a table through a simple
web application running on bootstrap"""

__author__      = "Andreas Iden"

import json
import requests
from flask_table import Table, Col
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


# STACC API
api_url = 'https://visningsrom.stacc.com/dd_server_laaneberegning/rest/laaneberegning/v1/nedbetalingsplan'

# Takes several paramteres as input  to create a JSON object, which is used in a POST request to server
# Had to set variable "ukjentVerdi"'s value to 0 to make http request work
def postPayload(loan_amount, nominal_interest, term_fee, expiration_date, balance_date, first_payment):
    payload_object = {
        "laanebelop": loan_amount,
        "nominellRente": nominal_interest,
        "terminGebyr": term_fee,
        "utlopsDato": expiration_date,
        "saldoDato": balance_date,
        "datoForsteInnbetaling": first_payment,
        "ukjentVerdi": 0
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(api_url, json = payload_object, data=json.dumps(payload_object), headers=headers)
    #response = requests.post(api_url, data=json.dumps(payload_object), headers=headers)
    #print("leif", requests.head(api_url))
    #print(response)
    return response

payload = postPayload(2000000, 3, 30, "2021-01-01", "2020-01-01", "2020-02-01")
payment_plan = json.dumps(payload.json(), indent=3)

# Processes the returned JSON file to a more workable format
payment_plan = payment_plan[(payment_plan.find("["))+1:]
payment_plan = payment_plan[:payment_plan.find("]")-1]

payment_list = []

# Extracts all internal dictionaries, which are represented as strings, in the string returned from the stringified
# JSON object and passes them into a list - as strings
def list_parser(plan_as_sting):
    global payment_list
    start = 0
    pos = 0
    for char in plan_as_sting:
        pos += 1
        if char == "}":
            payment_list.append(plan_as_sting[start:pos])
            start = pos + 3

list_parser(payment_plan)
payment_dictlist = []

# Iterates over payment_list and transforms the elements to dictionaries, so that the payment_diclist only contains
# a list with dicts
for elem in payment_list:
    json_acceptable_string = elem.replace("'", "\"")
    tempvar = json.loads(json_acceptable_string)
    payment_dictlist.append(tempvar)

# Class that creates the sceleton for a payment-breakdown table
class ItemTable(Table):
    restgjeld = Col('Remaining debt')
    dato = Col('Date')
    innbetaling = Col('Payment')
    gebyr = Col('Fee')
    renter = Col('Interest')
    total = Col('Total')

# Opens html file in read/write mode and writes ready html code from table variable
table = ItemTable(payment_dictlist)
fhand = open("index.html", "w+")
if fhand.mode == "w+":
    for line in fhand:
        line = line.split()
        if "<table class=" in line:
            fhand.write(table.__html__())


# flask and bootstrap connections
app = Flask(__name__)
Bootstrap(app)

# function that returns index.html through render module
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()









