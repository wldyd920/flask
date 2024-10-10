from flask import render_template, Flask, redirect, request
from datetime import datetime
import pandas as pd
import math

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('./index.html')
