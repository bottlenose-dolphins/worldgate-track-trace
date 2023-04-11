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
CORS(app, resources={r"/*": {"origins": ["http://www.worldgatetracktrace.click", "http://127.0.0.1", "http://worldgatetracktrace.click", "localhost"]}})

prod = getenv("prod")
print("prod type: ", type(prod))

def function_to_call():
    status=invoke_http2("core_notification_complex","/sendsms",prod,method="POST")
    t=threading.Timer(24*60*60, function_to_call)
    t.daemon = True
    t.start()


t = threading.Timer(0, function_to_call)
t.daemon = True
t.start()

# def call_function_every_24_hours():
#     # Schedule the function_to_call() to run every 24 hours
#     schedule.every(10).seconds.do(invoke_http2("core_complex_scraper","complex_scraper/sendsms",prod,method="POST"))

#     while True:
#         # Run the scheduled jobs
#         schedule.run_pending()
#         # Sleep for 1 second to avoid excessive CPU usage
#         time.sleep(1)

# # Start the scheduling in a separate thread
# t = threading.Thread(target=call_function_every_24_hours)
# t.daemon = True
# t.start()




if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5017, debug=True)
    app.run(host='0.0.0.0', debug=True)




    