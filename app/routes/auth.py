from flask import request,redirect,url_for,Blueprint,render_template,flash
from werkzeug.security import check_password_hash,generate_password_hash
from app import db
from app.models import User 
from flask_login import login_user ,login_required,logout_user


auth=Blueprint('auth',__name__)

@auth.route('/',methods=['GET'])
def home():
    
    return render_template("home.html")



@auth.route('/register',methods=['POST','GET'])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        section=request.form.get("section")
        existing_user=User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists")
            return redirect(url_for("auth.register"))
        hashed_password=generate_password_hash(password)
        new_user=User(username=username,password=hashed_password,section=section)

        db.session.add(new_user)
        db.session.commit()
        flash(f"registration successfully {username} now u can login successfully 🎉 ")

        return redirect(url_for("auth.login"))
    
    return(render_template('register.html'))

@auth.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if not username:
            return "username required "
        if not password:
            return " password required "
        user=User.query.filter_by(username=username).first()

        if user is None:
            flash ("username does not exist ❌ ", "danger ")
            return redirect(url_for("auth.login"))
        if not check_password_hash(user.password,password):
            flash("Wrong password! ❌", "danger")
            return redirect(url_for("auth.login"))
        
        login_user(user)
        flash(f"welcome , {user.username.capitalize()}! 🎉", "success")
        return redirect(url_for("auth.home"))
           
    return render_template("login.html")

@auth.route("/logout",methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out! 👋", "info")
    return redirect(url_for("auth.home"))