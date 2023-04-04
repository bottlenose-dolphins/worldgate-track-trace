from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from invokes import invoke_http, invoke_http2
from os import getenv
from dotenv import load_dotenv
import json
import os
import time
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

schedule.every(24).hours.do(invoke_http2("core_complex_scraper","complex_scraper/sendsms",prod,method="POST"))

while True:
    schedule.run_pending()
    time.sleep(1)
