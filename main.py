from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


with open('config.json','r')  as c:
    parameter = json.load(c)["parameter"]

local_server = True

app = Flask(__name__)


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri']





db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=True)
    phone_number = db.Column(db.String(12),  nullable=False)
    massage = db.Column(db.String(200),  nullable=False)
    date = db.Column(db.String(12),  nullable=True)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(500),  nullable=False)
    img_file = db.Column(db.String(12), nullable=True)
    date = db.Column(db.String(10),  nullable=True)


@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:5]
    return render_template('index.html', parameter=parameter, posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', parameter=parameter)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()


    return render_template('post.html', parameter=parameter, post=post)


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

    return render_template('contact.html', parameter=parameter)

app.run(debug=True)
