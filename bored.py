from flask import Flask, render_template,redirect,request,session,make_response,url_for,jsonify,flash,Response
from flask_pymongo import PyMongo
from gridfs import GridFS
from authlib.integrations.flask_client import OAuth
import dynaweb,engine,gemini,prompts,personalizer
from datetime import datetime
import configparser
import google.generativeai as gemini_model
from werkzeug.exceptions import NotFound,MethodNotAllowed,RequestTimeout,BadRequestKeyError,InternalServerError
import google.api_core.exceptions as geminiExceptions
import markdown
import os,binascii

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("secrets.cfg")

app.config["MONGO_URI"] = config['mongodb']['uri']
app.config["SECRET_KEY"] = config['captcha']['secret_key']
app.config["SITE_KEY"] = config['captcha']['site_key']
mongo = PyMongo(app)
oauth = OAuth(app)

home_engine = engine.engine_client(app.config["MONGO_URI"])
dynamic_web = dynaweb.curate_web()
data = {}

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

@app.errorhandler(NotFound)
def not_found(error):
    return render_template("response.html",code=404)

@app.errorhandler(MethodNotAllowed)
def method_not_allowed(error):
    return render_template("response.html",code=405)

@app.errorhandler(RequestTimeout)
def method_not_allowed(error):
    return render_template("response.html",code=408)

@app.errorhandler(BadRequestKeyError)
def bad_request_key_error(error):
    return render_template("response.html",code=410)

@app.errorhandler(InternalServerError)
def internal_server_error(error):
    return render_template("response.html",code=500)

@app.errorhandler(geminiExceptions.InternalServerError)
def internal_server_error(error):
    return redirect("/dynamo")

@app.errorhandler(geminiExceptions.ResourceExhausted)
def resource_exhausted(error):
    return redirect("/dynamo")

@app.route("/")
def intro():
    if not session:
        return render_template("login.html",SITE_KEY=app.config["SITE_KEY"])
    else:
        return redirect("/home")
    
@app.route("/logout")
def clear_session():
    session.clear()
    return redirect("/clear_cookies")

@app.route("/clear_cookies")
def clear_cookies():
    response = make_response(redirect("/"))
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
        return render_template("response.html",code=200)
    else:
        mongo.db.users.insert_one(user_creds)
        return render_template("response.html",code=250)

@app.route("/login",methods=["POST"])
def login():
    nickname = request.form.get('nickname')
    safeword = request.form.get('safeword')
    existing_user = mongo.db.users.find_one({"nickname":nickname})
    if not existing_user:
        return render_template("response.html",code=100)
    if existing_user and existing_user["safeword"] == safeword:
        session["nickname"] = nickname
        session["recovery"] = existing_user["recovery"]
        response = make_response(redirect("/home"))
        response.set_cookie("first_visit","true")
        return response
    elif existing_user and existing_user["safeword"] != safeword:
        return render_template("response.html",code=150)
    
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
        session["recovery"] = valid_user["recovery"]
        response = make_response(redirect("/home"))
        response.set_cookie("first_visit","true")
        return response
    else:
        return render_template("response.html",code=100)
    
@app.route("/home",methods=["GET","POST"])
def home():
    session["year"] = str(datetime.now().year)
    if session:    
        user_class = mongo.db.user_classes.find_one({"nickname":session["nickname"]})
        data["first_visit"] = False

        if user_class:
            data["desc"] = dynamic_web.get_class_description(user_class["class"])
        
        if not (mongo.db.survey.find_one({"nickname":session["nickname"]})):
            return redirect("/survey")
        
        for cookie in request.cookies:
            if cookie == "first_visit":
                data["first_visit"] = True
        
        rec_prompts = prompts.prompt_corpus(home_engine.build_tags(session["nickname"]))
        recommendations = [tag.capitalize() for tag in gemini.fit_prompt(rec_prompts.get_sentiment_corpus(True)).split()]
        data["top1"] = recommendations[0]
        data["top2"] = recommendations[1]
        data["top3"] = recommendations[2]
        data["top1_desc"] = dynamic_web.get_tag_tooltip(data["top1"])
        data["top2_desc"] = dynamic_web.get_tag_tooltip(data["top2"])
        data["top3_desc"] = dynamic_web.get_tag_tooltip(data["top3"])
    
        response = make_response(render_template("home.html",data=data))
        response.set_cookie("first_visit",expires=0)
        return response
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
        if "first_visit" in cookie:
            response.set_cookie("survey","true")
            mongo.db.survey.insert_one(survey_det)
            Prompts = prompts.prompt_corpus(home_engine.build_tags(session["nickname"]))
            user_class = gemini.fit_prompt(Prompts.get_sentiment_corpus())
            data["user_class"] = user_class.capitalize()
            mongo.db.user_classes.insert_one({"nickname":session["nickname"],"class":user_class})
    return response

@app.route("/dynamo")
def dynamo():
    try:
        user = session["nickname"]
        session["opted_users%"] = home_engine.opted_users_p()
        session["is_opted"] = home_engine.is_opted(session["nickname"])
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        if opted_in_user:
            history = personalizer.get_clean_history(session["nickname"],mode="dynamo")
            if not history or history == "":
                icebreaker = dynamic_web.get_dynamo_icebreaker()
                session["icebreaker"] = icebreaker
                session["tip"] = dynamic_web.no_history_response(opted=True)
            else:
                icebreaker = gemini.fit_prompt(prompts.prompt_corpus([]).get_relevant_icebreaker(session["nickname"],history))
                session["tip"] = gemini.fit_prompt(prompts.prompt_corpus([]).get_tip(history))
                session["icebreaker"] = icebreaker    
            gemini.config_dynamo(session["icebreaker"],user,history)
        else:
            icebreaker = dynamic_web.get_dynamo_icebreaker()
            session["icebreaker"] = icebreaker
            session["tip"] = dynamic_web.no_history_response(opted=False)
            gemini.config_dynamo(session["nickname"],user,None)
        return render_template("dynamo.html",talk=session["icebreaker"],data=data,error=False)
    except KeyError:
        return redirect("/")

@app.route("/chat",methods=["POST"])
def chat():
    try:
        message = request.form["message"]
        response, latest_message = gemini.chat_dynamo(message)
        user_message = message
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        if opted_in_user:
            user_in_chats = mongo.db.chats.find_one({"nickname":session["nickname"]})
            if not user_in_chats:
                mongo.db.chats.insert_one({"nickname":session["nickname"],"history":""})
            user_in_chats = mongo.db.chats.find_one({"nickname":session["nickname"]})
            previous_history = user_in_chats["history"]
            if previous_history == "" or previous_history[-1] == "~":
                previous_history += "\n[CHAT] "+session["icebreaker"]
            current_history = personalizer.build_history(previous_history,str(latest_message),user_message,model="Dynamo")
            updated_history = mongo.db.chats.update_one({"nickname":session["nickname"]},{"$set":{"nickname":session["nickname"],"history":current_history}})
        return jsonify(talk=markdown.markdown(response.text), error=False)
    except Exception as e:
        print(e)
        return jsonify(talk=markdown.markdown(response.text), error=False)
    
@app.route("/seeker")
def seeker():
    if not session:
        return redirect("/")
    user = mongo.db.seeker.find_one({"nickname":session["nickname"]})
    if not user or not user["survey"]:
        mongo.db.seeker.insert_one({"nickname":session["nickname"],"survey":"False"})
        session["askTopics"] = True
    
    if user and user["survey"] == "True":
        session["askTopics"] = False
    return render_template("seeker.html")

@app.route("/shaman")
def shaman():
    try:
        user = session["nickname"]
        session["opted_users%"] = home_engine.opted_users_p()
        session["is_opted"] = home_engine.is_opted(session["nickname"])
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        if opted_in_user:
            history = personalizer.get_clean_history(session["nickname"],mode="shaman")
            if not history or history == "":
                icebreaker = dynamic_web.get_shaman_icebreaker()
                session["icebreaker"] = icebreaker
                session["tip"] = dynamic_web.no_history_response(opted=True)
            else:
                icebreaker = gemini.fit_prompt(prompts.prompt_corpus([]).get_relevant_icebreaker(session["nickname"],history))
                session["tip"] = gemini.fit_prompt(prompts.prompt_corpus([]).get_tip(history))
                session["icebreaker"] = icebreaker    
            gemini.config_shaman(session["icebreaker"],user,history)
        else:
            icebreaker = dynamic_web.get_shaman_icebreaker()
            session["icebreaker"] = icebreaker
            session["tip"] = dynamic_web.no_history_response(opted=False)
            gemini.config_shaman(session["nickname"],user,None)
        return render_template("shaman.html",talk=session["icebreaker"],data=data,error=False)
    except KeyError:
        return redirect("/")

@app.route("/chat_shaman",methods=["POST"])
def chat_shaman():
    try:
        message = request.form["message"]
        response, latest_message = gemini.chat_shaman(message)
        user_message = message
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        if opted_in_user:
            user_in_chats = mongo.db.shaman.find_one({"nickname":session["nickname"]})
            if not user_in_chats:
                mongo.db.shaman.insert_one({"nickname":session["nickname"],"history":""})
            user_in_chats = mongo.db.shaman.find_one({"nickname":session["nickname"]})
            previous_history = user_in_chats["history"]
            if previous_history == "" or previous_history[-1] == "~":
                previous_history += "\n[CHAT] "+session["icebreaker"]
            current_history = personalizer.build_history(previous_history,str(latest_message),user_message,model="Dynamo")
            updated_history = mongo.db.shaman.update_one({"nickname":session["nickname"]},{"$set":{"nickname":session["nickname"],"history":current_history}})
        return jsonify(talk=markdown.markdown(response.text), error=False)
    except Exception as e:
        print(e)
        return jsonify(talk=markdown.markdown(response.text), error=False)

@app.route("/seeker/intro",methods=["POST"])
def seeker_intro():
    topics = list(dict(request.form).keys())
    session["askTopics"] = False
    mongo.db.seeker.update_one({"nickname":session["nickname"],"survey":"False"},{"$set":{"survey":"True","topics":topics}})
    return redirect("/seeker")

@app.route("/personalize",methods=["POST"])
def doPersonalize():
    existing_user = mongo.db.opted_users.find_one({"nickname":session["nickname"]})
    if not existing_user:
        mongo.db.opted_users.insert_one({"nickname":session["nickname"]})
        return redirect(request.referrer)
    else:
        return redirect(request.referrer)

@app.route("/depersonalize",methods=["POST"])
def dontPersonalize():
    mongo.db.opted_users.delete_one({"nickname":session["nickname"]})
    mongo.db.chats.delete_one({"nickname":session["nickname"]})
    return redirect(request.referrer)

@app.route("/journal")
def journal():
    session["today"] = dynamic_web.today()
    existing_journals = mongo.db.journals.find({"nickname":session["nickname"]},{"_id":False})
    session["list_journals"] = list(existing_journals)
    session["journals"] = True if session["list_journals"] != [] else False
    print(session["list_journals"])
    return render_template("journal.html")

@app.route("/blank",methods=["POST"])
def blank_journal():
    token = dynamic_web.token16b()
    title = request.form["title"]
    date = session["today"]
    mongo.db.journals.insert_one({"nickname":session["nickname"],"token":token,"title":title, "date":session["today"], "entry":""})
    return redirect(url_for("get_journal",token=token))

@app.route("/entry/<token>")
def get_journal(token):
    if not mongo.db.journals.find_one({"token":token}):
        return redirect("/")
    else:
        journal_data = personalizer.get_journal_data(token)
        return render_template("blank.html",journal=journal_data)

@app.route("/saves/<token>",methods=["POST"])
def save_journal(token):
    message = request.form["jtext"]
    mongo.db.journals.update_one({"token":token},{"$set":{"entry":message}})
    now = dynamic_web.now()
    return jsonify(status=f'({now}) Changes have been saved!',error=False)

@app.route("/delete/<token>",methods=["POST"])
def delete_journal(token):
    mongo.db.journals.delete_one({"token":token})
    return redirect("/journal")

@app.route("/prompt",methods=["POST"])
def get_prompt():
    return jsonify(prompt=f'{personalizer.get_journal_prompt()}',error="False")
