# Flask middleware example
from flask import Flask, request
import logging

app = Flask(__name__)

@app.before_request
def scrub_pii():
    if 'password' in request.json:
        request.json['password'] = '***REDACTED***'