from flask import render_template, Flask, redirect, request


@app.route('/')
def home():
    return render_template('1.html')
