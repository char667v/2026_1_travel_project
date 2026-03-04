from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time

from flask_session import Session

# 2i see the" bug icecreme is a library
from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True) # the dash Santi created it

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

##############################
@app.get("/signup")
def show_signup():
    try:
         user = session.get(user, "")
         return render_template("page_signup.html", user=user)
    except Exception as ex:
         ic(ex)
         return "ups.. system under maintenace", 500
    
##############################
@app.post("/api-create-user")
def api_create_user():
     try:
          user_first_name = 
     except Exception as ex:
          ic(ex)
          return "ups"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()
          