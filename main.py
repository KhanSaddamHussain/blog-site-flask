from flask import Flask, render_template,request

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/saddamblog'
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=True)
    phone_number = db.Column(db.String(12),  nullable=False)
    massage = db.Column(db.String(200),  nullable=False)
    date = db.Column(db.String(12),  nullable=True)



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method == 'POST'):
        name = request.form.get("name")
        emailAdd = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("msg")

        entry = Contacts(name=name,email=emailAdd,phone_number=phone,massage=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

app.run(debug=True)
