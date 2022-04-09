from sqlite3 import Cursor
from flask import Flask, json,redirect,render_template,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import flask

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
local_server=True

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Mars2019@localhost/dbp'

db=SQLAlchemy(app)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mars2019'
app.config['MYSQL_DB'] = 'dbp'


theuser = 'none'

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test")
def show():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM LOGINDBP''')
    result = cursor.fetchall()
    for x in result:
        print(x)
    mysql.connection.commit()
    cursor.close()
    return "terminal"

@app.route("/logincorrect",methods=["GET","POST"])
def logcheck():
    uname = request.form['uname0']
    pswd = request.form['pswd0']
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM LOGINDBP WHERE USERNAME = %s AND PASSWORD = %s''',(uname,pswd))
    data=cursor.fetchall()
    if len(data)==0:
        print("Incorrect Username or Password")
        return 'Incorrect Username or Password'
    else:
        DAUSER = uname
        global theuser
        theuser = uname
        print("USER:"+uname)
        return DAUSER

@app.route("/login")
def loginpage():
    return render_template("login.html")

@app.route("/fregdone", methods=["GET","POST"])
def regdone():
    

    uname = request.form['uname0']
    pswd = request.form['pswd0']
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO LOGINDBP VALUES (%s,%s)''',(uname,pswd))
    #rgg = gg.fetchall()
    #for x in rgg:
    #    print(x)
    mysql.connection.commit()
    cursor.close()
    return 'succesfull'
@app.route("/signup")
def signuppage():
    return render_template("signup.html")

def var():
    return theuser

@app.route("/cardbuy",methods=["GET","POST"])
def buygame():
    uname = var()
    gamename = request.form['cardname']
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO CARD VALUES (%s,%s)''',(uname,gamename))
    mysql.connection.commit()
    cursor.close()
    return 'card requested'

app.run(debug=False)
        