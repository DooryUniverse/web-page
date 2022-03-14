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
    
@app.route("/login/", methods=["POST"])
def login():
    # select 문을 사용-> index page input ID, PASSWORD 받아와서 
    # SELECT 문으로 조회 
    # 결과 값이 존재 하면 return "login" 존재하지 안흥면 return "Fail"
    _id = request.form["_id"]
    _password = request.form["_password"]
    # print(_id, _password) # 1번 완료
   
    sql ="""
            SELECT * FROM user_info 
            WHERE ID = %s AND password =%s
         """
    _values = [_id,_password]
    _db= mod_sql.Database()
    result = _db.executeAll(sql, _values)
    # result -> [{}, {}, {}, {}]
    # list gudxodptj [1,2,3,4]-> 1을 출력하려면? list[0] -> 1출력
    # dict
    print(result) #2번완료 #이름이랑 아이디 같이 보내야함. name을 적어서
    if result:
        return render_template("welcome.html",name =result[0]["name"],
                               id=result[0]["ID"])
    else:
        return redirect(url_for('index'))
# 회원정보 수정 페이지 만들기    
@app.route("/update/")
def update():
    id= request.args["_id"]
    sql="""
        SELECT * FROM user_info WHERE ID = %s
        """
    values=[id]
    
    _db =mod_sql.Database()
    result = _db.executeAll(sql,values)
    return render_template("update.html",info =result[0])

@app.route("/update/", methods=["POST"])
def update_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _ads = request.form["_ads"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    sql ="""
        UPDATE user_info SET 
        password=%s,
        name =%s,
        phone =%s,
        gender=%s,
        age = %s,
        ads= %s
        where ID =%s
        """
        #ID값은  프라이머리키라서 없음
    values =[_password,_name,_phone,_gender,_age,_ads,_id]
    _db=mod_sql.Database()
    _db.execute(sql,values)
    _db.commit()
    return redirect(url_for('index'))

    
    
    
    
    #DB에 접속해서 Select 문을 가지고 인덱스 페이지에 아이디와 
    # 패스워드값을 받아와서
    #Select 문으로 조회
    #결과가 존재하면 return "login"
    #존재하지 않으면 return "fail"
app.run(port=80)
