from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dipali@localhost:3306/registration1'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'  # Set the table name to match the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
   
    def __repr__(self) ->str:
        return f"{self.username}-{self.email}"

@app.route('/')
def home():
    return redirect(url_for('Login'))

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('Login'))
    return render_template('Register.html')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            return redirect(url_for('Welcome'))
        else:
            flash('Login failed. Check your email and/or password.', 'danger')
    return render_template('Login.html')

@app.route('/Welcome')
def Welcome():
    return "Welcome to the home page!"
@app.route('/AboutUs')
def AboutUs():
    return "Information regarding our website"

if __name__ == '__main__':
    app.run(debug=True,port=8000)
