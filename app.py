from flask import Flask, render_template, redirect,request,flash
import psycopg2
import time

app = Flask(__name__)
app.secret_key = 'some_secret'
def empfield(Field=str):
    FP="Error. Surely you mustn`t leave field '"
    MP="' empty. Ошибка. Пожалуйста повторите попытку. Поле '"
    LP="' не должно быть пустым."
    error=FP+Field+MP+Field+LP
    error.encode('utf-8')
    return error

@app.route('/',methods=['GET'])
def ref():
    return redirect("/login/")

@app.route('/account/', methods=['GET', 'POST'])
def acc():
    if request.method == 'POST':
        return redirect("/login/")
    return render_template('account.html')

@app.route('/login/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        if request.form.get("login"):
            login = request.form.get('username')
            password = request.form.get('password')
            conn = psycopg2.connect(database = "service",
                                user="postgres",
                                password="123456",
                                host="localhost",
                                port="5432")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM userdb.testpage WHERE login=%s and password=%s",
            (str(login), str(password)))
            records = list(cursor.fetchall())
            conn.commit()
            if len(records)==0:
                error = 'Invalid credentials'
            else:
                return render_template('account.html', full_name = records[0][0])
        if request.form.get("registration"):
            return redirect("/registration/")
        if request.form.get("change"):
            return redirect("/chpas/")
    return render_template('login.html',error=error)

@app.route('/registration/', methods=['GET', 'POST'])
def bas():
    if request.method == 'POST':
        if request.form.get("Reg"):
            login = request.form.get('login')

            if login=='':
                error=empfield("Login")
                flash(error)
                return render_template('registration.html')
            password = request.form.get('password')
            if password=='':
                error=empfield("Password")
                flash(error)
                return render_template('registration.html')
            name = request.form.get('name')
            if name=='':
                error=empfield("Your name")
                flash(error)
                return render_template('registration.html')
            try:
                conn = psycopg2.connect(database = "service",
                                    user="postgres",
                                    password="123456",
                                    host="localhost",
                                    port="5432")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO userdb.testpage (name,login,password) VALUES (%s, %s, %s)",
                (str(name), str(login), str(password)))
                conn.commit()
                flash('Thank you for registering')
                return redirect("/login/")
            except:
                flash('Login is not unique')
                return render_template('registration.html')
        if request.form.get("return"):
            return redirect("/login/")
    return render_template('registration.html')

@app.route('/chpas/', methods=['GET', 'POST'])
def pas():
    if request.method == 'POST':
        if request.form.get("change"):
            login = request.form.get('login')
            if login=='':
                error=empfield("Login")
                flash(error)
                return render_template('chpas.html')
            password = request.form.get('password')
            if password=='':
                error=empfield("Password")
                flash(error)
                return render_template('chpas.html')
            conn = psycopg2.connect(database = "service",
                                    user="postgres",
                                    password="123456",
                                    host="localhost",
                                    port="5432")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM userdb.testpage WHERE login=%s",[login])
            records = list(cursor.fetchall())
            if len(records)!=0:
                cursor.execute("UPDATE userdb.testpage SET password = %s WHERE login = %s;",
                (str(password), str(login)))
                conn.commit()
                flash('Password was successfully changed')
                return redirect("/login/")
            else:
                conn.commit()
                flash('Login is not correct')
                return render_template('chpas.html')
        if request.form.get("return"):
            return redirect("/login/")
    return render_template('chpas.html')
