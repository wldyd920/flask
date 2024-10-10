from flask import render_template, Flask, redirect, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./1.html')

app.run(port=5000, debug=True)
