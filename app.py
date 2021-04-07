from flask import Flask, request, render_template, session, url_for, redirect
from markupsafe import escape
import mysql.connector, json
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = "(@*&#(283&$(*#"


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "*&#^$*&#^$*&#$^*@&^*&@^#&@^",
    database = "website"
)

class create_dict(dict): 

    def __init__(self): 
        self = dict() 
          
    def add(self, key, value): 
        self[key] = value

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("member"))
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    ruser = request.form['ruser']
    rpassword = request.form['rpassword']
    rname = request.form['rname']
    cursor = mydb.cursor(buffered=True)
    sql = "SELECT `username` FROM `user` WHERE `username` = %s ;"
    check_user = (ruser,)
    cursor.execute(sql, check_user)
    for check in cursor:
        if (check[0]==ruser):
            return redirect(url_for("error", message = "帳號已經被註冊"))
    
    sql = "INSERT INTO `user` (name, password, username) VALUES ( %s, %s, %s );"
    member_data = (rname, rpassword, ruser)
    cursor.execute(sql, member_data)
    mydb.commit()
    return redirect(url_for('index'))

@app.route("/signin", methods=["POST"])
def signin():
    user = request.form['user']
    password = request.form['password']
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT `username`,`password` FROM `user`;")
    for username, pw in cursor:
        if(username == str(user) and pw == str(password)):
            session['user'] = user
            sql = "SELECT `name` FROM `user` WHERE BINARY `username` = %s AND `password` = %s ;"
            check_data = (user, password)
            cursor.execute(sql, check_data)
            for name in cursor:
                session['name'] = name[0]
            return redirect(url_for('member'))   
            
    return redirect(url_for("error", message = "帳號或密碼輸入錯誤"))

@app.route("/member")
def member():
    if "user" in session:
        return render_template("member.html", name=session['name'])
    else:
        return redirect(url_for('index'))
    
@app.route("/error")
def error():
    data = request.args.get("message")
    return render_template("error.html", messages=data)

@app.route("/signout")
def signout():
    session.pop("user", None)
    session.pop("name", None)
    return redirect(url_for('index'))

@app.route("/api/users", methods=["GET"])
def api():
    user = request.args.get('username')
    cursor = mydb.cursor(buffered=True)
    mydict = create_dict()
    sql = "SELECT * FROM `user` WHERE BINARY `username` = %s ;"
    find_user = (user,)
    cursor.execute(sql, find_user)
    some_list=[]
    data = cursor.fetchall()
    if (some_list == data):
        mydict.add("data",None)
    else:
        for row in data:
            mydict.add("data",({"id":row[0],"name":row[1],"username":row[2]}))
    stud_json = json.dumps(mydict, indent=2, sort_keys=True, ensure_ascii=False)
    return stud_json


app.run(port=3000)
