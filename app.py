from flask import Flask, request, render_template, redirect, session
import psycopg2
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'

@app.route('/')
def login():
    name = request.args.get('name')
    email = request.args.get('email')

    conn = psycopg2.connect("dbname=app2kitchen")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = (%s)", [name])
    conn.commit()
    conn.close()
    return render_template('login.html', name=name)

@app.route('/login', methods=["POST"])
def login_action():

    name = request.form.get('name')
    email = request.form.get('email')

    conn = psycopg2.connect("dbname=app2kitchen")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    conn.commit()
    data = cur.fetchall()
    print(data)
    conn.close()

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup_action', methods=['GET', 'POST'])
def signup_action():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    print(email, name, password)
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = psycopg2.connect("dbname=app2kitchen")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    conn.commit()
    data = cur.fetchall()
    print(data)
    conn.close()
    
    if len(data) > 0:
        checkD = True
        print('already existing')
        return redirect('/signup')
    else:
        checkD = False
        conn = psycopg2.connect("dbname=app2kitchen")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",[email, name, password_hash]) 
        conn.commit()
        conn.close()
        return redirect('/')


app.run(debug=True)