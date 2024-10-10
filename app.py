from flask import render_template, Flask, redirect, request
from datetime import datetime
import pandas as pd
from openai import OpenAI
import assi.py

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./1.html')
