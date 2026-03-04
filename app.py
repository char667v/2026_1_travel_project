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

ic(int(time.time()))



##############################
# creating a form
@app.get("/signup")
def show_signup():
    try:
        return render_template("page_signup.html", x=x)
    except Exception as ex:
        print(ex, flush = True)
        return "ups ..."

##############################
@app.post("/check-username")
def check_username():
    try:
        user_username = x.validate_user_username()
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_username = %s"
        cursor.execute(q, (user_username,))
        row = cursor.fetchone()
        if not row:
            return f"""
                <browser mix-update="span">
                    Username available
                </browser>
            """
        return f"""
            <browser mix-update="span">
                Username taken
            </browser>
        """        
    
    except Exception as ex:
        # print(ex, flush = True)
        ic(ex)

        if "--error-- user_username" in str(ex):
            return f"""<browser mix-update="span">{ex.args[0]}</browser>""", 400 # 400 because it is somehting the USER DID

        # Worst case, something unexpected
        return f"""<browser mix-update="span">System under maintenance</browser>""", 500 # worse case scenario 500 cus it is something WE DID. {str(ex)} has been substituted with System under maintenance

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  


##############################
@app.post("/api-create-user")
def create_user():
    try:
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_pk = uuid.uuid4().hex
        user_create_at = int(time.time()) # epoch generation / time.time() = giver decimaltal
        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_username, user_first_name, user_create_at))
        db.commit()

        tip = render_template("___tip.html", message="User created", status="ok") #ok is name of the class

        return f"""
            <browser mix-update="#tooltip">{tip}</browser>
        """

    except Exception as ex:
        # print(ex, flush = True)
        ic(ex)

        if "--error-- user_username" in str(ex):
            return f"""<browser mix-update="span">{ex.args[0]}</browser>""", 400 # 400 because it is somehting the user did
        
        if "--error-- user_first_name" in str(ex):
            tip = render_template("___tip.html", message="Invalid first name", status="error") #error is name of the class
            return f"""<browser mix-update="#tooltip">{tip}</browser>""", 400 # 400 because it is somehting the user did
        
        if "Duplicate entry" in str(ex) and "user_username" in str(ex):
            return f"""<browser mix-update="span">Username taken</browser>""", 400

        # Worst case, something unexpected
        return f"""<browser mix-update="span">System under maintenance</browser>""", 500 # worse case scenario 500 cus it is something we did

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  


##############################
# page_login.html
@app.get("/login")
def login():
    try:
        return render_template("page_login.html")
    except Exception as ex:
         ic(ex)
         return "ups", 500


##############################
@app.post("/login")
def user_login():
    try:
        # TODO: validate
        # TODO: check if email and password exist in the db
        user = {
            "name":"Santiago"
        }
        session["user"] = user
        return "you are logged in"
    except Exception as ex:
         ic(ex)
         return str(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()  

##############################
#page_profile.html
@x.no_cache 
@app.get("/profile")
def profile():
    try:
        user = session.get("user", "")
        if not user: return redirect("/login")
        ic(user)
        return render_template("page_profile.html", user=user)
    except Exception as ex:
        ic(ex)
        return "error"
    

##############################
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as ex:
         ic(ex)
         return "system under maintenace"
