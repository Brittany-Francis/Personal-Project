from app import app
from flask import Flask, render_template, redirect, request, session, flash
from app.models.user_model import User
from app.models.book_model import Book
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



@app.route('/')          
def login_page():
    return render_template("login_registration.html")


@app.route('/register', methods=['POST'])
def register_user():
    form_data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "username": request.form["username"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    if not User.validate_user(form_data):
        return redirect('/')
    hash_pw= bcrypt.generate_password_hash(request.form['password'])
    hash_confirm_pw= bcrypt.generate_password_hash(request.form["confirm_password"])
    data= {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "username": request.form["username"],
        "password": hash_pw,
        "confirm_password": hash_confirm_pw
    }
    user=User.insert_user(data)
    session["user_id"]=user
    return redirect("/home")


@app.route('/login', methods=["POST"])
def login_user():
    data={
        "email":request.form["email"]
    }
    user_in_db=User.find_user_by_email(data)
    if not user_in_db:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid email/password", "login")
        return redirect('/')

    session["user_id"]=user_in_db.id

    return redirect("/home")

@app.route('/home')          
def home_page():
    if not "user_id" in session:
        return redirect("/")
    
    data={
        "id": session["user_id"]
    }
    user=User.get_user_by_id(data)
    all_books=Book.get_all_books_with_user()
        
    return render_template("home.html", user=user, all_books=all_books )



@app.route('/logout')
def logout():
    session.clear()
    return redirect ("/")







