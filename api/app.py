#https://github.com/Azure/azure-functions-python-library/pull/45
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from nacl.signing import VerifyKey, SignedMessage
from nacl.encoding import HexEncoder, URLSafeBase64Encoder
from nacl.exceptions import BadSignatureError
from datetime import datetime, timedelta
from .auth import refrein

import azure.functions as func
import os
import azure.functions as func

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/list.db'
application.config['SECRET_KEY'] = os.environ['SECRET_KEY']
application.config['SESSION_COOKIE_SECURE'] = True
application.config['REMEMBER_COOKIE_SECURE'] = True
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Local development
#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\youruser\\Documents\\code\\tnl-list\\list.db'
db = SQLAlchemy(application)

class Shitlist(db.Model):
    __tablename__ = 'shitlist'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    votes = db.Column(db.Integer)

class Litlist(db.Model):
    __tablename__ = 'litlist'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    votes = db.Column(db.Integer)

@application.route("/shit")
def shitlist():
    current_url = request.url
    auth = request.args.get('auth', None)

    if auth:
        if not refrein(auth):
            return render_template('failure.html', msg="Your auth token did not verify"), 401

    try:
        cookie = session['name']
    except:
        cookie = False

    if not cookie:
        return render_template('index.html', current_url=current_url), 401
          
    shitlist = Shitlist.query.all()
    return render_template('shitlist.html', shitlist=shitlist)    


@application.route("/lit")
def litlist():
    current_url = request.url
    auth = request.args.get('auth', None)

    if auth:
        if not refrein(auth):
            return render_template('failure.html', msg="Your auth token did not verify"), 401

    try:
        cookie = session['name']
    except:
        cookie = False

    if not cookie:
        return render_template('index.html', current_url=current_url), 401
            
    litlist = Litlist.query.all()
    return render_template('litlist.html', litlist=litlist) 
