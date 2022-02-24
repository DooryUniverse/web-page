from flask import Flask

app = Flask(__name__)

@app.route('/') # web: 주소->127.0.0.1:5000/ , localhost:500/

def index():
    return "Hello, world"

#url을 추가해서 def를 실행을 하려면? 어떻게??
@app.route('/second/') # web-> 주소 127.0.0.1:5000/second/
def second():
    return "Second page" # 두번째 페이지 만들기
app.run

