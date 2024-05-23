from flask import Flask, render_template,redirect,request,session,make_response,url_for
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
from prompts import prompt_corpus
from gemini import fit_prompt
from engine import engine_client
from dynaweb import curate_web
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "[REDACTED]"
app.config["SECRET_KEY"] = "[REDACTED]"
app.config["SITE_KEY"] = "[REDACTED]"
mongo = PyMongo(app)
oauth = OAuth(app)
home_engine = engine_client(app.config["MONGO_URI"])
dynamic_web = curate_web()

google = oauth.register(
    name='google',
    client_id='953946004284-uofaq8ej75e9l0vfkb3o2mdl2gdpc6q7.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope':'email'},
)

try:
    mongo.db.command('ping')
    print("MongoDB connection established.")
except Exception as e:
    print("Error connecting to MongoDB:", e)

@app.route("/")
def intro():
    if not session:
        return render_template("login.html",SITE_KEY=app.config["SITE_KEY"])
    else:
        return redirect("/home")
    
@app.route("/logout")
def clear_session():
    session.clear()
    return redirect("/")

@app.route("/clear_cookies")
def clear_cookies():
    response = make_response("Cookies cleared.")
    for cookie in request.cookies:
        response.set_cookie(cookie, expires=0)
    return response
    
@app.route("/register",methods=["POST"])
def register():
    nickname = request.form.get('nickname')
    safeword = request.form.get('safeword')
    recovery = request.form.get('recovery')

    user_creds = {
        "nickname": nickname,
        "safeword": safeword,
        "recovery": recovery 
    }
    
    existing_user = mongo.db.users.find_one({"nickname":nickname})
    existing_mail = mongo.db.users.find_one({"recovery":recovery})
    if existing_user or existing_mail:
        return render_template("response.html",code=200) #Duplicate user
    else:
        mongo.db.users.insert_one(user_creds)
        return render_template("response.html",code=250) #Successful
    
@app.route("/login",methods=["POST"])
def login():
    nickname = request.form.get('nickname')
    safeword = request.form.get('safeword')
    existing_user = mongo.db.users.find_one({"nickname":nickname})
    if not existing_user:
        return render_template("response.html",code=100) #Not registered
    if existing_user and existing_user["safeword"] == safeword:
        session["nickname"] = nickname
        response = make_response(redirect("/home"))
        response.set_cookie("visited","true")
        return response
    elif existing_user and existing_user["safeword"] != safeword:
        return render_template("response.html",code=150) #Invalid safeword
    
@app.route('/reset')
def reset():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize',_external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    response = google.get('userinfo',token=token)
    user_info = response.json()
    valid_user = mongo.db.users.find_one({"recovery":user_info['email']})
    if valid_user:
        session["nickname"] = valid_user["nickname"]
        response = make_response(redirect("/home"))
        response.set_cookie("visited","true")
        return response
    else:
        return render_template("response.html",code=100)
    
@app.route("/home",methods=["GET","POST"])
def home():
    year = str(datetime.now().year)
    if session:    
        user_class = mongo.db.user_classes.find_one({"nickname":session["nickname"]})
        if user_class:
            desc = dynamic_web.get_class_description(user_class["class"])
        display_result = False
        if not (mongo.db.survey.find_one({"nickname":session["nickname"]})):
            return redirect("/survey")
        for cookie in request.cookies:
            if cookie == "survey":
                display_result = True
                response = make_response(render_template("home.html",year=year,desc=desc,display_result=display_result))
                response.set_cookie("survey",expires=0)
                return response
        else:
            return render_template("home.html",year=year,desc=desc,display_result=display_result)
    else:
        return redirect("/")
    
@app.route("/survey")
def survey():
    if not session:
        return redirect("/")
    elif not (mongo.db.survey.find_one({"nickname":session["nickname"]})):
        return render_template("survey.html")
    else:
        return redirect("/home")

@app.route("/survey/submit",methods=["POST"])
def survey_submit():
    response = make_response(redirect("/home"))
    survey_det = dict(request.form)
    survey_det["nickname"] = session["nickname"]
    for cookie in request.cookies:
        if "visited" in cookie:
            response.set_cookie("survey","true")
            mongo.db.survey.insert_one(survey_det)
            prompts = prompt_corpus(home_engine.build_tags(session["nickname"]))
            user_class = fit_prompt(prompts.get_sentiment_corpus())
            mongo.db.user_classes.insert_one({"nickname":session["nickname"],"class":user_class})
    return response