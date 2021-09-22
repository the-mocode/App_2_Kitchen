from db import sql_select, sql_write
from flask import Flask, request, render_template, redirect, session
import requests
import psycopg2
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'

@app.route('/')
def home():
    response = requests.get('https://www.themealdb.com/api/json/v1/1/categories.php/')
    data = response.json()
    print(data)
    categ = data['categories']
    return render_template('home.html', categ=categ)

@app.route('/meals/<category>')
def categ_action(category):
    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}')
    data = response.json()
    categ_type = data['meals']
    return render_template('meals.html', categ_type=categ_type)

@app.route('/recipe/<meal_id>')
def recipe(meal_id):
    # categ_type = request.get.args("catDescript")
    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}')
    data = response.json()
    meal = data['meals'][0]
    return render_template('recipe.html', meal=meal)


@app.route('/login')
def login():
    name = request.args.get('name')
    return render_template('login.html', name=name)

@app.route('/login_action', methods=["POST"])
def login_action():

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    # need to get login to accept password first 
    data1 = sql_select("SELECT * FROM users WHERE email = %s", [email])
    return redirect('/login')

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

    data = sql_select("SELECT * FROM users WHERE email = %s", [email])
    print(data)
    
    if len(data) > 0:
        checkD = True
        print('already existing')
        return redirect('/signup')
    else:
        checkD = False
        sql_write("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",[email, name, password_hash])
        return redirect('/login')


app.run(debug=True)