from flask import render_template, Flask, redirect, request
import pandas as pd


@app.route('/')
def home():
    return render_template('1.html')

app.run(port=5000, debug=True)
