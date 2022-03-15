from flask import Flask, render_template, request, redirect, url_for
import pymysql
from modules import mod_sql
import pandas as pd
app = Flask(__name__)

#localhost로 접속했을때
@app.route("/")
def index():
    return render_template("index.html")

#localhost/signup으로 접속했을 때
@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_2():
    _db = pymysql.connect(
    user = "root",
    passwd = "root",
    host ="localhost",
    db = "ubion"
    )
    cursor = _db.cursor(pymysql.cursors.DictCursor)
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]
    _ads = request.form["_ads"]
    _regitdate = request.form["_regitdate"]

    sql = """
            INSERT INTO user_info VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s)
        """
    _values = [_id, _password, _name, _phone, _ads, _gender, _age, _regitdate]
    cursor.execute(sql, _values)
    _db.commit()
    _db.close()

    return redirect(url_for('index'))

@app.route('/login', methods=["POST"])
def login():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _db = pymysql.connect(
        user = "root",
        passwd = "root",
        host ="localhost",
        db = "ubion"
    )
    #pymysql.cursors.DictCursor는 데이터를 Dict로 받음. default는 튜플
    cursor = _db.cursor()
    sql = """
        SELECT * FROM user_info
        WHERE ID = %s AND password = %s
    """
    _values = [_id, _password]
    cursor.execute(sql, _values)
    result = cursor.fetchall()
    _db.close()
    if result:
        return "Login"
    else:   
        return "Fail"

@app.route('/login2', methods = ["POST"])
def login2():
    _id = request.form["_id"]
    _password = request.form["_pw"]
    _db = mod_sql.Database()
    sql = """SELECT ID, name, phone FROM user_info
            WHERE ID = %s AND password = %s"""
    _values = [_id, _password]
    result = _db.executeAll(sql, _values)
    print(result)
    if result:
        return render_template("welcome.html", 
                            name=result[0]["name"],
                            id=result[0]["ID"])
    else:
        return redirect(url_for('index'))
    
    #return redirect(url_for('index'))
# 회원 정보 업데이트 웹 만들기
@app.route("/update", methods=["GET"])
def update():
    id = request.args["_id"]
    sql = """
            SELECT * FROM user_info WHERE ID = %s
    """
    values = [id]
    _db = mod_sql.Database()
    result = _db.executeAll(sql, values)
    return render_template("update.html", info = result[0])

@app.route("/update", methods=["POST"])
def update_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _name = request.form["_name"]
    _phone = request.form["_phone"]
    _ads = request.form["_ads"]
    _gender = request.form["_gender"]
    _age = request.form["_age"]

    sql = """
            UPDATE user_info SET 
            password=%s,
            name=%s,
            phone=%s,
            ads=%s,
            gender=%s,
            age=%s
            WHERE ID=%s
        """
    values = [_password,_name,_phone,_ads,_gender,_age,_id]
    _db = mod_sql.Database()
    _db.execute(sql,values)
    _db.commit()
    return redirect(url_for('index'))
# 회원 정보 삭제 웹 만들기
@app.route("/delete", methods=["GET"])
def delete():
    _id=request.args["_id"]
    return render_template("delete.html", id=_id)

@app.route("/delete", methods=["POST"])
def delete_2():
    _id = request.form["_id"]
    _password = request.form["_password"]
    _db=mod_sql.Database()
    s_sql = """
        SELECT * FROM user_info WHERE ID = %s AND password = %s
            """
    d_sql = """
        DELETE FROM user_info WHERE ID = %s AND password = %s
            """
    _values = [_id, _password]
    result = _db.executeAll(s_sql, _values)
    if result:
        _db.execute(d_sql,_values)
        _db.commit()
        return redirect(url_for('index'))
    else:
        return "패스워드가 맞지 않습니다."
    
    
# sql문 -> user_info left join ads_ info 가져오기
@app.route("/view2", methods=["GET"])
def views():
    sql = """
        SELECT user_info.name, user_info.ads, user_info.age, ads_info.Register_count 
        FROM user_info LEFT JOIN ads_info 
        ON user_info.ads=ads_info.ads
            """
    _db = mod_sql.Database()
    result = _db.executeAll(sql)
    key = list(result[0].keys())
    return render_template("view2.html", result=result, keys=key)

app.run(port=80, debug=True)
 
