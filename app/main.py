from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'userdb')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

STATES = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
    'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim',
    'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
    'West Bengal', 'Delhi', 'Jammu and Kashmir', 'Ladakh'
]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    company_role = db.Column(db.String(100))

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            address=request.form['address'],
            state=request.form['state'],
            phone=request.form['phone'],
            company_role=request.form['company_role']
        )
        db.session.add(user)
        db.session.commit()
        data = {
            'name': user.name,
            'address': user.address,
            'state': user.state,
            'phone': user.phone,
            'company_role': user.company_role
        }
        return render_template('form.html', states=STATES, data=data, submitted=True)
    return render_template('form.html', states=STATES, submitted=False)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        company_role = request.form.get('company_role', '').strip()
        query = User.query
        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))
        if company_role:
            query = query.filter(User.company_role.ilike(f"%{company_role}%"))
        results = query.all()
    return render_template('search.html', results=results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
