from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http, invoke_http2
from os import getenv
from dotenv import load_dotenv
import json
import os
import time
import threading
import schedule
from twilio.rest import Client

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, origins="http://localhost:3000",
     supports_credentials=True, expose_headers="Set-Cookie")

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(getenv('SQLALCHEMY_DATABASE_URI'))

prod = getenv("prod")
print("prod type: ", type(prod))

print("********")

db = SQLAlchemy(app)

def call_function_every_24_hours():
    # Schedule the function_to_call() to run every 24 hours
    schedule.every(10).seconds.do(invoke_http2("core_complex_scraper","complex_scraper/sendsms",prod,method="POST"))

    while True:
        # Run the scheduled jobs
        schedule.run_pending()
        # Sleep for 1 second to avoid excessive CPU usage
        time.sleep(1)

# Start the scheduling in a separate thread
t = threading.Thread(target=call_function_every_24_hours)
t.daemon = True
t.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014, debug=True)
    # app.run(host='0.0.0.0', debug=True)




    