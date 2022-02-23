from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    return "Hello, world"

#url을 추가해서 def를 실행을 하려면? 어떻게??
@app.route('/second/')
def second():
    return "Second page" # 두번째 페이지 만들기
app.run

