from flask import render_template, Flask, redirect, request
from datetime import datetime
import pandas as pd
import math

app = Flask(__name__)


# 홈 ============================================================================================
@app.route('/')
def home():
    return render_template('1.html')
# ===============================================================================================





# 프로젝트 5 (욕하기 웹사이트) ====================================================================

@app.route('/project5/', methods=["GET", "POST"])
def swear():
    return render_template('swear.html')
    




# 프로젝트 4 (Chat-GPT-4o) =======================================================================
from assi import chat
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
    return render_template('conversation_architecture.html')




# 프로젝트 3 (게시판) ==========================================================================
articles = pd.read_csv("articles.csv")

@app.route('/project3/')
def project3():
    if len(articles)==0: 
        article_hrefs = '게시글 없음'
    else:
        article_hrefs = ''
        for i in range(len(articles)):
            title = articles.loc[i, "title"]
            href = f'<a href="/project3/read/{i}/">{str(i+1)}. {title}</a><br><br>'
            article_hrefs += href
    return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>게시판</title>
            </head>
            <body>
                <a href="/">홈으로</a><br><br>
                <a href="/project3/write/">새 게시글 작성</a><br><br><br><br>
                <ul>
                    <h2>게시글 목록</h2>
                    {article_hrefs}
                </ul>
            </body>
            </html>
            '''

@app.route('/project3/write/', methods=['GET', 'POST'])
def write():
    if request.method == "GET":
        return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>글쓰기</title>
            </head>
            <body>
                <a href="/">홈으로</a><br><br>
                <a href="/project3/">게시판으로</a><br><br><br><br>

                <form action="/project3/write/" method="POST">
                    <p>제목 : <input type="text" name="title" placeholder="title"></p>
                    <p>내용 : <textarea name="body" placeholder="body"></textarea></p>
                    <p><input type="submit" value="글 남기기"></p>
                </form>
            </body>
            </html>
            '''
    
    elif request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        new_article = [title, body]
        new_id = len(articles)
        print(new_id)
        articles.loc[new_id] = new_article
        articles.to_csv("articles.csv", index=False)
        url = '/project3/read/'+str(new_id)+'/'
        return redirect(url)

@app.route('/project3/read/<int:id>/')
def read(id):
    title = articles.loc[id, "title"]
    body = articles.loc[id, "body"]
    return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>게시판 {id+1}번째 글</title>
            </head>
            <body>
                <a href="/">홈으로</a><br><br>
                <a href="/project3/">게시판으로</a><br><br><br><br>
                <ul>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <a href="/project3/edit/{id}/">수정</a>&nbsp;&nbsp; 
                    <a href="/project3/delete/{id}/">삭제</a>
                    <h3>제목</h3>
                    {title}
                    <h3>본문</h3>
                    {body}<br><br>
                
                </ul>
            </body>
            </html>
            '''

@app.route('/project3/delete/<int:id>/')
def delete(id):
    articles.drop(id, inplace=True)
    articles.set_index([list(range(len(articles)))], inplace=True)
    articles.to_csv("articles.csv", index=False)
    return redirect('/project3/')

@app.route('/project3/edit/<int:id>/', methods=["GET", "POST"])
def edit(id):
    title = articles.loc[id, "title"]
    body = articles.loc[id, "body"]
    if request.method == "GET": 
        return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>글 수정</title>
            </head>
            <body>
                <a href="/">홈으로</a><br><br>
                <a href="/project3/">게시판으로</a><br><br><br><br>

                <form action="/project3/edit/{id}" method="POST">
                    <p>제목 : <input type="text" name="title" placeholder="title" value="{title}"></p>
                    <p>내용 : <textarea name="body" placeholder="body">{body}</textarea></p>
                    <p><input type="submit" value="수정"></p>
                </form>
            </body>
            </html>
            '''
    elif request.method == "POST":
        articles.loc[id, "title"] = request.form["title"]
        articles.loc[id, "body"] = request.form["body"]
        articles.to_csv("articles.csv", index=False)
        return redirect(f'/project3/read/{id}/')


# 프로젝트 2 (로그인) ===============================================================================
@app.route('/project2/')
def project2():
    return render_template('login.html')

# 프로젝트 1 (주피터 노트북) =========================================================================
@app.route('/project1/', methods=['GET', 'POST'])
def project1():
    if request.method == "GET":
        return render_template('project1.html')

# 컨퍼런스 ==========================================================================================
@app.route('/conferences/<int:id>/')
def conferences(id):
    if id == 2:
        iframe_tag = "https://drive.google.com/file/d/1G17Dp7xq42NcIRVHEvIip4TpZ0Wkd6Jm"
    elif id == 3:
        iframe_tag = "https://drive.google.com/file/d/1OfcuUq-1r8_e27CDyzqxbIVJecvoFMWz"
    elif id == 4: 
        iframe_tag = "https://drive.google.com/file/d/1xhqrMA1kcnrtIzApqWSs1-lhbE7Cyphn"
    elif id == 5:
        iframe_tag = "https://drive.google.com/file/d/1kSk-XNJpksVIuzJOKX8C8yl_DSqEdQz1"
    return  f'''<!doctype html>
                <iframe src={iframe_tag+'/preview'} width="900" height="507"></iframe>'''


# 나이 계산기 ========================================================================================
@app.route('/age_cal/', methods=['GET', 'POST'])
def age_cal():
    if request.method == "GET":
        return  '''
                <!doctype html>
                <a href="/">홈으로</a><br><br>
                생년월일을 입력해주십시오.<br><br>
                <form action="/age_cal/" method="POST">
                    <input type="text" name="birth" placeholder="예시: 20240101" maxlength="8"><br><br>
                    <input type="submit" value="확인"></form>
                </form>
                '''

    elif request.method == "POST":
        try:
            if request.form['birth'] == 'my': birth = '19920920'
            else : birth = request.form['birth']

            birth = datetime.strptime(birth, "%Y%m%d")
            today = datetime.now()

            userBirthYear = birth.year
            userBirthMonth = birth.month
            userBirthDay = birth.day

            thisYear = today.year
            thisMonth = today.month
            thisDay = today.day

            isBirthdayPassed = False
            if(thisMonth > userBirthMonth) :
                isBirthdayPassed = True
            elif(thisMonth == userBirthMonth) :
                if(thisDay >= userBirthDay) :
                    isBirthdayPassed = True
                else :
                    isBirthdayPassed = False
            else :
                isBirthdayPassed = False;

            Korean_age = thisYear - userBirthYear + 1
            International_age = (thisYear - userBirthYear) if isBirthdayPassed == True else (thisYear - userBirthYear - 1)
            age_table = '''<table border='1'>
                            <tr>
                                <th scope="col">&nbsp;&nbsp;연도&nbsp;&nbsp;</td>
                                <th scope="col">&nbsp;&nbsp;한국 나이&nbsp;&nbsp;</td>
                                <th scope="col">&nbsp;&nbsp;만 나이 (생일 전)&nbsp;&nbsp;</td>
                                <th scope="col">&nbsp;&nbsp;만 나이 (생일 후)&nbsp;&nbsp;</td>
                            </tr>
                        '''
            for i in range(thisYear, userBirthYear-1, -1):
                한국나이 = i - userBirthYear + 1
                생일전 = i-userBirthYear-1
                생일후 = i-userBirthYear
                age_table += f'''
                            <tr>
                            <td style="text-align:center">{i}</td>
                            <td style="text-align:center">{한국나이}</td>
                            <td style="text-align:center">{생일전}</td>
                            <td style="text-align:center">{생일후}</td>
                            </tr>
                            '''
                if i == userBirthYear: age_table+='</table>'

            return f'''<!doctype html>
                    <a href="/">홈으로</a><br><br>
                    생년월일을 입력해주십시오.<br><br>
                    <form action="/age_cal/" method="POST">
                        <input type="text" name="birth" placeholder="예시: 20240101" maxlength="8"><br><br>
                        <input type="submit" value="확인"></form>
                    </form><br>
                    현재 만 나이 : {International_age} 살 입니다.</br>
                    현재 한국 나이 : {Korean_age} 살 입니다.</br>
                    </br>
                    {age_table}
                    '''

        except Exception as e:
            if ValueError(): 
                ErrorMessage = '출생년도 네 자리, 생일 네 자리를 공백없이 8자리로 작성해 주십시오.'
            else: 
                ErrorMessage = str(e)

            print(type(e))
            print(e)  # 어떤 에러가 발생했는지는 콘솔창으로 확인
            return f'''
                <!doctype html>
                <a href="/">홈으로</a> <br><br>
                생년월일을 입력해주십시오. <br><br>
                {ErrorMessage}<br><br>
                <form action="/age_cal/" method="POST">
                    <input type="text" name="birth" placeholder="예시: 20240101" maxlength="8"><br><br>
                    <input type="submit" value="확인"></form>
                </form>
                '''

# 실행 ====================================================================================================

app.run(port=5001, debug=True)
