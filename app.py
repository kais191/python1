from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

#  database /
users = [
    {'name': 'John Doe', 'email': 'john@example.com', 'username': 'john', 'password': generate_password_hash('password'), 'age': 30},
    {'name': 'Jane Doe', 'email': 'jane@example.com', 'username': 'jane', 'password': generate_password_hash('password'), 'age': 25}
]

# Routes/
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        age = request.form['age']

        # Check  username /
        for user in users:
            if user['username'] == username:
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect(url_for('signup'))

        # Check  passwords /
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('signup'))

        
        hashed_password = generate_password_hash(password)

        # Add new user /
        users.append({'name': name, 'email': email, 'username': username, 'password': hashed_password, 'age': age})

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #  if username there and passwords match /
        for user in users:
            if user['username'] == username and check_password_hash(user['password'], password):
                session['username'] = username
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('home'))

        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/payment/<int:card_id>', methods=['GET', 'POST'])
def payment(card_id):
    if request.method == 'POST':
        quantity = request.form['quantity']
        card_number = request.form['card-number']
        expiration_date = request.form['expiration-date']
        cvv = request.form['cvv']

        #  payment /
        flash('Payment processed successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('payment.html', card_id=card_id)

if __name__ == '__main__':
   # app.run(debug=True)
     app.run()

