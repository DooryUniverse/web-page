from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__) # name에는 내가 실행시키는 파일이 들어간다.

@app.route('/') # web: 주소->127.0.0.1:5000/ , localhost:500/

def index():
    return render_template("index.html")

# localhost/signup
@app.route('/signup/', methods=["GET"]) # web-> 주소 127.0.0.1:5000/signup/
def signup():
    return render_template("signup.html") # 두번째 페이지 만들기
@app.route("/signup", methods=["POST"])
def signup_2():
    _db = pymysql.connect(
    user = "root", # mysql 아이디
    passwd = "root", # mysql 비밀번호
    host ="localhost", # 내 컴퓨터
    db = "ubion"
    )
    cursor = _db.cursor(pymysql.cursors.DictCursor)
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _ads = request.form["_ads"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _regitdate = request.form["_regitdate"]
    sql = """ 
         INSERT INTO user_info VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
          """
    _values = [_id, _password, _name, _phone, _ads, _gender, _age, _regitdate]
    cursor.execute(sql, _values)
    _db.commit()
    _db.close()
    
    return redirect(url_for('index'))
    
    
app.run(port=80)
