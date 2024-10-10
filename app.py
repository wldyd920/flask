from flask import render_template, Flask, redirect, request
from datetime import datetime
import pandas as pd
from openai import OpenAI
from assi import chat

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./1.html')



# 프로젝트 4 (Chat-GPT-4o) =======================================================================
conversation_history = ''

@app.route('/project4/conversation/', methods=["GET", "POST"])
def conversation():
    global conversation_history
    if request.method == "POST":
        talk = request.form['talk']
        reply, nth = chat(talk)
        conversation_history += f'{nth-1}. 나 : {talk} <br><br>'
        conversation_history += f'{nth}. GPT-4o: {reply} <br><br>'
        
    return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>GPT-4o와의 대화</title>
        </head>
        <body>
            <a href="/">홈으로</a><br><br>
            <a href="/project4/conversation/architecture/">이 프로젝트 아키텍처 보기</a><br><br>

            <ul>
                {conversation_history}
            </ul>

            <form action="/project4/conversation/" method="POST">
                <p>대화창 : <textarea name="talk" placeholder="message"></textarea></p>
                <p><input type="submit" value="send"></p>
            </form>
        </body>
        </html>
        '''

@app.route('/project4/conversation/architecture/')
def architecture():
    return render_template('./conversation_architecture.html')
