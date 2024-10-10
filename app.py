from flask import render_template, Flask, redirect, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./1.html')
