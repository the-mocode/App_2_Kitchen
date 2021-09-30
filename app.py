from db import sql_select, sql_write
from flask import Flask, request, render_template, redirect, session
import requests
import psycopg2
import bcrypt
import os
from models.fav import user_id
import json

SECRET_KEY = os.environ.get('SECRET_KEY', 'testkey')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

DB_URL = os.environ.get("DATABASE_URL", "dbname=app2kitchen")

@app.route('/')
def home():
    response = requests.get('https://www.themealdb.com/api/json/v1/1/categories.php/')
    data = response.json()
    # print(data)
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
    session['email'] = email
    # need to get login to accept password first 
    
    data1 = sql_select("SELECT * FROM users WHERE email = %s", [email])
    is_valid = bcrypt.checkpw(password.encode(), data1[0][3].encode())
    if is_valid:
        user_id = data1[0][0]
        session['user_id'] = user_id
        return redirect('/')
    else:
        print('invalid password or username, please try again')
        return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



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


@app.route('/favourites')
def favourites_list():

    user_id1 = session['user_id']
    meal_ids = sql_select("SELECT * FROM favourites WHERE user_id = %s", [user_id1])
    
    favourite_meals = []
    for ids in meal_ids:
        response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={ids[2]}')
        response_object = json.loads(response.text)
        for item in response_object["meals"]:
            meal = {
                'idMeal' : item['idMeal'],
                'strMeal' : item['strMeal'],
                'strMealThumb' : item['strMealThumb']
            }
            favourite_meals.append(meal)
   
    return render_template('favourites.html', favourite_meals=favourite_meals)

@app.route('/favourites_action', methods=['POST'])
def favourite():
    user_id1 = session['user_id']
    mealid = request.form.get('mealid')
    sql_write("INSERT INTO favourites (user_id, recipe_id) VALUES (%s, %s)", [user_id1, mealid])
    return redirect(f'/recipe/{mealid}')

@app.route('/unfavourites_action', methods=['POST'])
def unfavourite():
    user_id1 = session['user_id']
    mealid = request.form.get('mealid')
    sql_write("DELETE FROM favourites WHERE user_id=%s AND recipe_id=%s", [user_id1, mealid])
    return redirect('/favourites')


if __name__ == "__main__":
    app.run(debug=True)




#  get food id from form - get email from session  - get user id using email - insert new fav entry - redirect user


