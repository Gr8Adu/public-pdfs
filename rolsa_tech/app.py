from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


@app.route('/index')
def index():
    return render_template('index.html')


# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='sha256')

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'User already exists!'

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials!'

    return render_template('login.html')


# Dashboard Route (requires login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# Carbon Footprint Calculation Route (requires login)
@app.route('/carbon_calculator', methods=['GET', 'POST'])
def carbon_calculator():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    if request.method == 'POST':
        electricity = float(request.form['electricity'])
        gas = float(request.form['gas'])
        mileage = float(request.form['mileage'])

        total_carbon = electricity * 0.233 + gas * 0.184 + mileage * 0.411
        return render_template('carbonc.html', total_carbon=total_carbon)

    return render_template('carbonc.html', total_carbon=None)


# Schedule Consultation Route (requires login)
@app.route('/schedule_consultation', methods=['GET', 'POST'])
def schedule_consultation():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    if request.method == 'POST':
        consultation_date = request.form['consultation_date']
        consultation_time = request.form['consultation_time']

        # Save consultation request or process it here
        return render_template('schedule_consultation.html', confirmation=True)

    return render_template('schedule_consultation.html', confirmation=False)


# Main entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
