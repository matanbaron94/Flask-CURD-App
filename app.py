import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'



#############################################
########### SQL DATABASE SECTION ############
#############################################

basedir = os.path.abspath(os.path.dirname(__file__))


# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    phone = db.Column(db.Integer)
    email = db.Column(db.Text)

    def __init__(self,name,email,phone) :
        self.name = name
        self.email = email
        self.phone = phone


@app.route('/')
def index():
    locations = Location.query.all()
    return render_template('index.html', locations=locations)


@app.route('/update', methods=['POST','GET'])
def update():
    
    if request.method == 'POST':
        id = request.form.get('id')
        print(id)
        my_data = Location.query.get(id)

        my_data.name = request.form['name']
        my_data.phone = request.form['phone']
        my_data.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        new_location= Location(name,email,phone)

        db.session.add(new_location)
        db.session.commit()

        flash('Location added successfully!')

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)