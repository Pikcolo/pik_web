from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf import CSRFProtect
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('user/register.html', form=form) 

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now login', 'success')
        return redirect(url_for('login'))

    return render_template('user/register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect(url_for('Home'))
        else:
            flash('Invalid Email or Password', 'danger')

    return render_template('user/login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'email' in session:  
        user = User.query.filter_by(email=session['email']).first()
        return render_template('user/dashboard.html', user=user)  
    else:
        return redirect(url_for('login')) 

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('Home'))

@app.route("/About")
def About():
    services =['ให้อาหารปลา', 'ทำความสะอาดบ้าน', 'รับจ้างฟาร์มเลเวลในเกม' ,'สอนการบ้าน', 'ขับรถรับ-ส่ง' , 'รับจ้างพาไปต่างโลก']
    return render_template("about.html", my_services = services )

@app.route("/Features")
def Features():
    return render_template("features.html")

@app.route("/Features/Fish")
def Fish():
    return render_template("fish.html")

@app.route("/Admin")
def Admin():
    return render_template("admin.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
