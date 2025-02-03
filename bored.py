from flask import Flask, render_template,redirect,request,session,make_response,url_for,jsonify,flash,Response
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from gridfs import GridFS
from authlib.integrations.flask_client import OAuth
import dynaweb,engine,gemini,prompts,personalizer
from datetime import datetime
import configparser, time
import google.generativeai as gemini_model
from werkzeug.exceptions import NotFound,MethodNotAllowed,RequestTimeout,BadRequestKeyError,InternalServerError
import google.api_core.exceptions as geminiExceptions
import markdown2,models,os,base64,requests
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
socketio = SocketIO(app)
config = configparser.ConfigParser()
config.read("secrets.cfg")

app.config["MONGO_URI"] = config['mongodb']['uri']
app.config["SECRET_KEY"] = config['captcha']['secret_key']
app.config["SITE_KEY"] = config['captcha']['site_key']
app.config["UPLOADS"] = "static/uploads"
app.config["API_KEY"] = config["gemini"]["api_key"]
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
    return render_template("response.html",code=500)

@app.errorhandler(geminiExceptions.ResourceExhausted)
def resource_exhausted(error):
    return render_template("response.html",code=504)

@app.errorhandler(geminiExceptions.DeadlineExceeded)
def resource_exhausted(error):
    return render_template("response.html",code=504)

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

        tags = home_engine.build_tags(session["nickname"])
        rec_prompts = prompts.prompt_corpus()
        recommendations = [tag.capitalize() for tag in gemini.fit_prompt(rec_prompts.get_sentiment_corpus(tags,True)).split()]
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
            Prompts = prompts.prompt_corpus()
            user_class = gemini.fit_prompt(Prompts.get_sentiment_corpus(tags=home_engine.build_tags(session["nickname"])))
            data["user_class"] = user_class.capitalize()
            mongo.db.user_classes.insert_one({"nickname":session["nickname"],"class":user_class})
    return response

@app.route("/dynamo")
def dynamo():
    try:
        user = session["nickname"]
        mongo.db.users.update_one({"nickname":user},{"$inc":{"dynamo":1}})
        session["opted_users%"] = home_engine.opted_users_p()
        session["is_opted"] = home_engine.is_opted(session["nickname"])

        session["mask"],session["is_default_mask"] = personalizer.get_mask_details(session["nickname"])
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        topics_list = None
        if opted_in_user:
            history = personalizer.get_dynamo_history(session["nickname"])
            topics_list = gemini.fit_prompt(prompts.prompt_corpus().get_dynamo_highlights(history)).split('#')
            if not history or history == "":
                icebreaker = dynamic_web.get_dynamo_icebreaker()
                session["icebreaker"] = icebreaker
                session["tip"] = dynamic_web.no_history_response(opted=True)
            else:
                if not session["mask"]:
                    icebreaker = gemini.fit_prompt(prompts.prompt_corpus().get_relevant_icebreaker(session["nickname"],history))
                else:
                    icebreaker = gemini.fit_prompt(prompts.prompt_corpus().get_relevant_icebreaker(session["nickname"],history,instructions=session["mask"]))
                session["tip"] = gemini.fit_prompt(prompts.prompt_corpus().get_tip(history))
                session["icebreaker"] = icebreaker    
            gemini.config_dynamo(session["icebreaker"],user,history,instructions=session["mask"])
        else:
            icebreaker = dynamic_web.get_dynamo_icebreaker()
            session["icebreaker"] = icebreaker
            session["tip"] = dynamic_web.no_history_response(opted=False)
            gemini.config_dynamo(session["nickname"],user,history=None,instructions=session["mask"])
        return render_template("dynamo.html",talk=session["icebreaker"],data=data,topics=topics_list,error=False)
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
        return jsonify(talk=markdown2.markdown(response.text), error=False)
    except Exception as e:
        print(e)
        return jsonify(talk=markdown2.markdown(response.text), error=False)
    
@app.route("/create_mask",methods=["POST"])
def create_mask():
    instructions = request.form.get("mask")
    status = False
    try:
        status = dynamic_web.get_instruction_status(gemini.fit_prompt(prompts.prompt_corpus().get_dynamo_mask(instructions)))
    except:
        status = False
    
    if status:
        session["mask"] = instructions
        session["is_default_mask"] = False
        session["default_mask"] = None
        existing_user = mongo.db.masks.find_one({"nickname":session["nickname"]})
        if existing_user:
            mongo.db.masks.update_one({"nickname":session["nickname"]},{"$set":{"default_mask":None,"mask":instructions}})
        else:
            mongo.db.masks.insert_one({"nickname":session["nickname"],"default_mask":None,"mask":instructions})
        return redirect("/dynamo")
    else:
        return render_template("response.html",code=500)

@app.route("/create_mask/<token>",methods=["POST"])
def default_mask(token):
    try:
        instructions = prompts.prompt_corpus().get_default_mask(token)
        session["default_mask"] = token
        session["is_default_mask"] = True
        session["mask"] = instructions
        existing_user = mongo.db.masks.find_one({"nickname":session["nickname"]})
        if existing_user:
            mongo.db.masks.update_one({"nickname":session["nickname"]},{"$set":{"default_mask":token,"mask":instructions}})
        else:
            mongo.db.masks.insert_one({"nickname":session["nickname"],"default_mask":token,"mask":instructions})
        return redirect("/dynamo")
    except:
        return render_template("response.html",code=500)

@app.route("/clear_mask",methods=["POST"])
def clear_mask():
    session["mask"] = None
    session["default_mask"] = None
    session["is_default_mask"] = False
    mongo.db.masks.delete_one({"nickname":session["nickname"]})
    return redirect("/dynamo")
    
@app.route("/shaman")
def shaman():
    try:
        user = session["nickname"]
        mongo.db.users.update_one({"nickname":user},{"$inc":{"shaman":1}})
        session["opted_users%"] = home_engine.opted_users_p()
        session["is_opted"] = home_engine.is_opted(session["nickname"])
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        if opted_in_user:
            history = personalizer.get_shaman_history(session["nickname"])
            if not history or history == "":
                icebreaker = dynamic_web.get_shaman_icebreaker()
                session["icebreaker"] = icebreaker
                session["tip"] = dynamic_web.no_history_response(opted=True)
            else:
                icebreaker = gemini.fit_prompt(prompts.prompt_corpus().get_relevant_icebreaker(session["nickname"],history))
                session["tip"] = gemini.fit_prompt(prompts.prompt_corpus().get_tip(history))
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
        return jsonify(talk=markdown2.markdown(response.text), error=False)
    except Exception as e:
        print(e)
        return jsonify(talk=markdown2.markdown(response.text), error=False)

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
    jprompt = personalizer.get_journal_prompt()
    return jsonify(prompt=f'{jprompt}',error="False")

@app.route("/reflection")
def reflect():
    return render_template("reflection.html")

@app.route("/influence_mood",methods=["POST"])
def do_reflection():
    mood = request.form["mood"]
    mode = request.form["mode"]
    question_set = personalizer.get_question_set(mood,mode)[0].split("#")
    return jsonify({
        "status":"success",
        "questionSet":question_set
    })

@app.route("/timeline")
def timeline():
    if not session:
        return redirect("/")
    
    timelineData = {}
    now = datetime.now().strftime(f"%d/%m/%Y")
    existing_user = mongo.db.timeline.find_one({"nickname":session["nickname"]})
    timelineData["timeline"] = []
    timelineData["timeline_entry_done"] = False
    if existing_user and existing_user.get("last_interacted") and existing_user.get("last_interacted") == now:
        timelineData["timeline_entry_done"] = True
    elif existing_user and existing_user.get("last_interacted") and existing_user.get("last_interacted") != now:
        timelineData["timeline_entry_done"] = False
    
    if not existing_user:
        mongo.db.timeline.insert_one({
            "nickname":session["nickname"],
            "corpus":"",
            "history":""
        })

    if existing_user and (existing_user["corpus"] != "" or existing_user["history"] != ""):
        timelineData["timeline"] = personalizer.get_timeline(session["nickname"])
    elif existing_user and (existing_user["corpus"] == "" or existing_user["history"] == ""):
        timelineData["timeline"] = []
    return render_template("timeline.html",timelineData=timelineData)

@app.route("/mood_timeline_update",methods=["POST"])
def update_mood():
    date = datetime.now().strftime(f"%d/%m/%Y")
    existing_user = mongo.db.timeline.find_one({"nickname":session["nickname"]})
    corpus = request.form["corpus"]

    mood_prompt = prompts.prompt_corpus().get_mood_prompt(corpus)
    detected_mood = gemini.fit_prompt(mood_prompt)
    if existing_user and existing_user["last_interacted"] != date: 
        mongo.db.timeline.update_one({
            "nickname":session["nickname"]
        },
        {
            "$set":{
                "last_interacted":date,
                "corpus": personalizer.build_corpus_history(session["nickname"],date,corpus),
                "history": personalizer.build_timeline_history(session["nickname"],date,detected_mood)
            }
        })
    else:
        return jsonify({"status":"error","flash":"Cannot submit another note today."})
    return jsonify({"status":"success","flash":"Save successful! Come back again tommorrow!"})

@app.route("/zen")
def zen():
    if not session:
        return redirect("/")
    return render_template("zen.html")

@app.route("/choose_zen",methods=["POST"])
def choose_zen():
    if not session:
        return redirect("/")
    return jsonify({"status":"success","choice":request.form["zenChoice"]})

@app.route("/radar")
def radar():
    if not session:
        return redirect("/")
    session["question"] = gemini.radar_config()
    return render_template("radar.html",question=session["question"])

@app.route("/radar_response",methods=["POST"])
def radar_response():
    user_response = request.form["response"]
    gemini_response = gemini.chat_radar(user_response).text
    response = gemini_response.strip()
    status,score = 1,0
    verdict = ""
    concerns= ""
    if "[" in response or "]" in response:
        status = 0
        score = [int(_) for _ in response[1:-1].split(',')]
        response = "END"
        status = 0
        verdict = models.make_radar_verdict(score)
        history = gemini.get_clean_radar_history()
        concerns = gemini.get_radar_concerns(history)
    return jsonify(question=response,status=status,score=score,concerns=str(concerns),verdict=verdict,success=True)

@app.route("/get_radar_analysis",methods=["POST"])
def get_radar_analysis():
    scores = personalizer.get_scores(request.json)
    analysis = gemini.fit_prompt(prompts.prompt_corpus().get_analysis_prompt(scores))
    return jsonify(success=True,title=scores["title"],scores=scores,analysis=analysis,safeword="Analysis")

@app.route("/ace")
def ace():
    session["today"] = dynamic_web.today()
    icebreaker = "How can I help you?"
    user = session["nickname"]
    mongo.db.users.update_one({"nickname":user},{"$inc":{"ace":1}})
    gemini.config_ace(user)

    session["modified_habits"] = {}
    session["completed_habits"] = {}
    session["missed_habits"] = {}

    session["completed_habits_list"] = []
    session["ongoing_habits_list"] = []
    
    session["n_completed_habits"] = 0

    habits = mongo.db.habits.find_one({"nickname": session["nickname"]})
    if habits:
        habits = dict(habits).get("tracked_habits", [])
        for habit in habits:
            habit_name = habit["habit_name"]
            if habit.get("interacted") == dynamic_web.today():
                session["modified_habits"][habit_name] = 1
            else:
                session["modified_habits"][habit_name] = 0
            
            if habit.get("score") == habit.get("max_score"):
                session["completed_habits"][habit_name] = 1
                session["n_completed_habits"] += 1
                session["completed_habits_list"].append(habit)
            else:
                session["ongoing_habits_list"].append(habit)
            
            if habit.get("score") != 0 and habit.get("check_next") > 0:
                if habit.get("interacted") ==  dynamic_web.yesterday() or habit.get("interacted") == dynamic_web.today():
                    session["missed_habits"][habit_name] = 0
                else:
                    session["missed_habits"][habit_name] = 1
                    
            else:
                session["missed_habits"][habit_name] = 0
    return render_template("ace.html",talk=icebreaker,tracked_habits=habits,completed_habits=session["completed_habits_list"],ongoing_habits=session["ongoing_habits_list"])

@app.route("/chat_ace",methods=["POST"])
def chat_ace():
    try:
        message = request.form["message"]
        response = gemini.chat_ace(message)
        html_content = markdown2.markdown(response.text, extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
        return jsonify(talk=html_content, error=False)
    except Exception as e:
        return jsonify(talk="Ace could not respond to your request.", error=True)

@app.route("/pomodoro")
def pomodoro():
    return render_template("pomodoro.html")

@app.route("/tasksempty")
def empty():
    session["tasks"] = {}
    session["num_tasks"] = 0
    return redirect("/outline")

@app.route("/outline")
def outline():
    try:
        existing_user = mongo.db.plans.find_one({"nickname":session["nickname"]})
        if not existing_user:
            mongo.db.plans.insert_one({"nickname":session["nickname"],"num_tasks":0})
        else:
            num_tasks,tasks = personalizer.get_tasks(session["nickname"]) 
            pass
        return render_template("outline.html",num_tasks=num_tasks,tasks=tasks)
    except:
        return redirect("/outline")

@app.route("/create_task",methods=["POST"])
def create_task():
    existing_user = mongo.db.plans.find_one({"nickname":session["nickname"]})
    if existing_user:
        num_tasks,tasks = personalizer.get_tasks(session["nickname"])
        task_index = num_tasks
        task_name = "Task " + str(task_index+1)
        task_desc = request.form.get("taskDesc")
        task_index = 1
        try:
            mongo.db.plans.update_one({"nickname":session["nickname"]},{"$set":{"num_tasks":existing_user["num_tasks"]+1,task_name:task_desc}})
            tasks[task_name] = task_desc
            num_tasks = task_index
        except Exception as e:
            return e
    return jsonify(num_tasks=len(tasks),tasks=tasks)

@app.route("/delete_task/<token>",methods=["POST"])
def delete_task(token):
    existing_user = mongo.db.plans.find_one({"nickname":session["nickname"]})
    if existing_user:
        updated_num_tasks =  existing_user["num_tasks"]-1 if existing_user["num_tasks"] > 0 else 0
        mongo.db.plans.update_one({"nickname":session["nickname"]},{"$unset":{token:""},"$set":{"num_tasks":updated_num_tasks}})
        task_name = str(token).replace("%20"," ")
        tasks = session.get("tasks",None)
        if tasks:
            session["tasks"].pop(task_name,"")
    return redirect("/outline")

@app.route("/collaborate")
def progress():
    projects = mongo.db.projects.count_documents({"nickname": session["nickname"]})
    if projects > 0:
        return redirect("/projects")
    return render_template("collaborate.html")

@app.route("/projects")
def projects():
    page = int(request.args.get('page', 1))
    per_page = 5
    existing_user = mongo.db.projects.find_one({"nickname":session["nickname"]})
    if existing_user:
        session["projects"] = True
        all_projects = mongo.db.projects.count_documents({"nickname": session["nickname"]})
        projects_ = mongo.db.projects.find({"nickname": session["nickname"]}, {"_id": False}).skip((page - 1) * per_page).limit(per_page)
        session["list_projects"] = list(projects_)
        total_pages = (all_projects + per_page - 1) // per_page
    else:
        session["projects"] = False
        total_pages = 0
    return render_template("hub.html",page=page,total_pages=total_pages)

@app.route("/create_project",methods=["POST"])
def create_project():
    project_title = request.form["projectTitle"] 
    project_desc = request.form["projectDesc"]
    projects = mongo.db.projects.find({"nickname": session["nickname"]}, {"_id": False})
    if projects and len(list(projects)) == 25:
        flash("You cannot create more than 25 projects.","warning")
        return redirect("/projects")

    existing_title_count = mongo.db.projects.count_documents({"nickname": session["nickname"], "project_title": project_title})
    if existing_title_count > 0:
        flash("A project with the same name already exists.", "error")
        return redirect("/projects")
    
    token = dynamic_web.token16b()
    mongo.db.projects.insert_one({
        "nickname":session["nickname"],
        "project_id":token,
        "project_title":project_title,
        "project_desc":project_desc,
        "created":dynamic_web.today(),
        "init":False,
        "context":""
    })
    flash("Project created successfully.","success")
    return redirect("/projects")

@app.route("/project/<token>")
def new_project(token):
    project_id = token
    project = dict(mongo.db.projects.find_one({"nickname": session["nickname"],"project_id":token}, {"_id": False}))
    conv = None
    marked_catchup,marked_history,marked_tip = None,None,None
    tip = None
    catchup = None
    if project["init"] == True:
        project_details = project["project_details"]
        project_tasks = project["project_tasks"]

        if not project["context"] or project["context"] == "":
            gemini.config_project_ace(session["nickname"],project["project_title"],project_details,project_tasks,context="",catchup=None)
            conv = None
        else:
            if project["active"] != 0:
                history = dynamic_web.get_context(project["context"]).split("$$$BREAK$$$")[-1]
                catchup_context = prompts.prompt_corpus().get_discussion_icebreaker(project["context"])
                catchup = gemini.fit_prompt(catchup_context)
                tip = gemini.fit_prompt(prompts.prompt_corpus().get_tip(project["context"]))
                marked_history = markdown2.markdown(history,extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])    
                marked_catchup = markdown2.markdown(catchup,extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
                marked_tip = markdown2.markdown(tip,extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
            gemini.config_project_ace(session["nickname"],project["project_title"],project_details,project_tasks,context=project["context"],catchup=catchup)
    return render_template("project.html",project_id=project_id,project=project,conversation=conv,history=marked_history,talk=None,tip=marked_tip,catchup=marked_catchup)

@app.route("/delete_project/<token>",methods=["POST"])
def delete_project(token):
    existing_user = mongo.db.projects.find_one({"nickname":session["nickname"]})
    if existing_user:
        mongo.db.projects.delete_one({"nickname":session["nickname"],"project_id":token})
    else:
        session["projects"] = False
    flash(f"Project deleted successfully.")
    return redirect("/projects")

@app.route("/project_init/<token>",methods=["POST"])
def brief_project(token):
    project = mongo.db.projects.find_one({"nickname":session["nickname"],"project_id":token})
    project_details = request.form["projectDescription"]
    project_tasks = request.form["assistanceDetails"]

    if not project["context"] or project["context"] == "":
        gemini.config_project_ace(session["nickname"],project["project_title"],project_details,project_tasks,context="",catchup=None)
    else:
        gemini.config_project_ace(session["nickname"],project["project_title"],project_details,project_tasks,context=project["context"],catchup=None)

    mongo.db.projects.update_one(
        {
            "nickname":session["nickname"],
            "project_id":token
        },
        {
            "$set":{
                "init":True,
                "project_details":project_details,
                "project_tasks":project_tasks,
                "active":1,
                "discussions": [
                    {
                        "discussion_title":"Discussion",
                        "discussion_history":""
                    }
                ]
            }
        }
    )
    return redirect(f"/project/{token}")

@app.route("/chat_project_ace/<token>",methods=["POST"])
def chat_project_ace(token):
    project = mongo.db.projects.find_one({"nickname":session["nickname"],"project_id":token})
    message = request.form["usermsg"]
    
    if "attachment" in request.files:
        file = request.files["attachment"]
        if file.filename == "":
            return jsonify(talk="No file selected.", catchup=None, error=False)

        allowed_text_extensions = {"txt", "py", "js", "cpp", "java", "html", "css", "c", "csv", "md", "json", "xml", "sql", "go", "rb", "php", "swift", "yaml", "toml", "log", "docx", "pdf"}
        allowed_image_extensions = {"jpg", "jpeg", "png"}
        
        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1][1:].lower()

        if (file_extension not in allowed_text_extensions) and (file_extension not in allowed_image_extensions):
            return jsonify(talk="ERROR: Invalid file type. Ace only serves text, code or image types.", catchup=None, error=False)
        elif file_extension in allowed_text_extensions:
            file_content = file.read().decode("utf-8")
            message = f"""FILE CONTENT: {file_content} \n INSTRUCTIONS: {request.form['usermsg']}"""

        if file_extension in allowed_image_extensions:
            path = os.path.join(app.config['UPLOADS'], filename)
            file.save(path)
            file_url = url_for('static', filename=f'uploads/{filename}', _external=False)
            response, latest_message = gemini.chat_project_ace(message,image=path)
            current_history = personalizer.build_project_history(session["nickname"],project["context"],str(latest_message),message,model="Ace")
            mongo.db.projects.update_one({"nickname":session["nickname"],"project_id":token},{"$set":{"context":current_history}})
            talk=markdown2.markdown(response.text, extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
            return jsonify(talk=talk,catchup=None,error=False,file_link=file_url)

    response, latest_message = gemini.chat_project_ace(message)
    current_history = personalizer.build_project_history(session["nickname"],project["context"],response.text,message,model="Ace")
    talk=markdown2.markdown(response.text, extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
    mongo.db.projects.update_one({"nickname":session["nickname"],"project_id":token},{"$set":{"context":current_history}})
    return jsonify(talk=talk,catchup=None,error=False)

@app.route("/new_discussion/<token>",methods=["POST"])
def new_discussion(token):
    query = {
        "discussions.discussion_title": request.form["title"]
    }
    document = mongo.db.projects.find_one(query,{"_id":1})
    if document:
        flash("A discussion with the same title already exists.","error")
        return redirect(f"/project/{token}")
        
    project = mongo.db.projects.find_one({"nickname":session["nickname"],"project_id":token})
    if not document and project["active"] != 1:
        mongo.db.projects.update_one(
            {
                "nickname":session["nickname"],
                "project_id":token
            },
            {
                "$set":{
                    "active":project["active"]+1,
                    "discussions": project["discussions"]+ [
                        {
                            "discussion_title":request.form["title"].strip(),
                            "discussion_history":""
                        }
                    ]
                }
            }
        )
        flash(f"Successfully created a discussion titled '{request.form['title']}'")
    elif not document and project["active"] == 1:
        flash(f"Cannot create a new discussion. Please conclude existing ones.","error")
    return redirect(f"/project/{token}")

@app.route("/conclude_discussion/<token>/<title>",methods=["POST"])
def conclude_discussion(token,title):
    project = mongo.db.projects.find_one({"nickname":session["nickname"],"project_id":token})
    query = {
        "discussions.discussion_title": title
    }
    document = mongo.db.projects.find_one(query,{"_id":1})
    if not document:
        flash(f"A discussion titled '{title}' does not exist.","error")
        return redirect(f"/project/{token}")
    
    latest_discussion = dynamic_web.get_context(str(project["context"]).split("$$$BREAK$$$")[-1])
    marked_history = markdown2.markdown(latest_discussion,extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
    mongo.db.projects.update_one(
        {
            "nickname": session["nickname"],
            "project_id": token,
            "discussions.discussion_title": title
        },
        {
            "$set": {
                "active": project["active"] - 1,
                "context": project["context"]+"\n$$$BREAK$$$\n",
                "discussions.$.closed": True,
                "discussions.$.discussion_history": marked_history
            },
        }
    )
    flash(f"Closed discussion titled '{title}'")
    return redirect(f"/project/{token}")

@app.route("/delete_discussion/<token>",methods=["POST"])
def delete_discussion(token):
    project = mongo.db.projects.find_one({"nickname": session["nickname"], "project_id": token})
    
    if not project:
        flash("Project not found.", "error")
        return redirect(f"/project/{token}")
    
    discussion_to_delete = None
    discussion_index = -1

    for index, discussion in enumerate(project.get("discussions", [])):
        if discussion["discussion_title"] == request.form["title"]:
            discussion_to_delete = discussion
            discussion_index = index
            break

    if discussion_to_delete is None:
        flash(f"A discussion titled '{request.form['title']}' does not exist.", "error")
        return redirect(f"/project/{token}")

    contexts = project["context"].split("$$$BREAK$$$")
    new_context = "$$$BREAK$$$".join(contexts[:discussion_index] + contexts[discussion_index + 1:])

    mongo.db.projects.update_one(
        {
            "nickname": session["nickname"],
            "project_id": token
        },
        {
            "$set": {
                "active": project["active"] - 1 if project["active"] != 0 else 0,
                "context": new_context,
            },
            "$pull": {
                "discussions": {
                    "discussion_title": request.form["title"]
                }
            }
        }
    )

    flash(f"Successfully deleted discussion titled '{request.form['title']}'")
    return redirect(f"/project/{token}")

@app.route("/edit_discussion/<token>",methods=["POST"])
def edit_discussion(token):
    project = mongo.db.projects.find_one({"nickname":session["nickname"],"project_id":token})

    prev_title = request.form.get("prevtitle")
    new_title = request.form.get("newtitle")
    discussion_exists = any(discussion["discussion_title"] == prev_title for discussion in project["discussions"])
    if not discussion_exists:
        flash(f"Discussion title '{prev_title}' not found.")
        return redirect(f"/project/{token}")
    
    mongo.db.projects.update_one(
        {
            "nickname": session["nickname"],
            "project_id": token,
            "discussions.discussion_title": prev_title
        },
        {
            "$set": {
                "discussions.$.discussion_title": new_title
            }
        }
    )
    return redirect(f"/project/{token}")

@app.route("/create_habit",methods=["POST"])
def create_habit():
    exists = mongo.db.habits.find_one({"nickname":session["nickname"]})
    if not exists:
        mongo.db.habits.insert_one({"nickname":session["nickname"],"tracked_habits":[]})
        exists = True
    
    habit_name = request.form["habitName"]
    habit_desc = request.form["habitDescription"]
    max_score = int(request.form["habitTarget"])
    query = {
        "nickname": session["nickname"],
        "tracked_habits.habit_name": habit_name
    }
    document = mongo.db.habits.find_one(query,{"_id":1})
    if exists and not document:
        mongo.db.habits.update_one({"nickname": session["nickname"]}, {
            "$push": {
                "tracked_habits": {
                    "habit_name": habit_name.strip(),
                    "habit_desc": habit_desc.strip(),
                    "score": 0,
                    "max_score": max_score,
                    "check_next": max_score,
                }
            }
        })
        flash(f"Now tracking habit '{habit_name}'","success")
    else:
        flash("A habit with the same name already exists.","error")
    return redirect("/ace")

@app.route("/update_habit/<nickname>/<habit>", methods=["POST"])
def update_habit(nickname, habit):
    query = {
        "nickname": str(nickname),
        "tracked_habits.habit_name": str(habit),
    }
    habit_doc = mongo.db.habits.find_one(query, {"tracked_habits.$": 1})
    if habit_doc:
        habit_data = habit_doc["tracked_habits"][0]
        
        if habit_data.get("interacted") == dynamic_web.today():
            return jsonify(success=False, error="Habit already updated today"), 400
        
        if habit_data["score"] != 0 and habit_data["check_next"] > 0:
            if not(habit_data.get("interacted") ==  dynamic_web.yesterday() or habit_data.get("interacted") == dynamic_web.today()):
                return jsonify(success=False,missed=True)
        
        update = {
            "$inc": {
                "tracked_habits.$.score": 1,
                "tracked_habits.$.check_next": -1
            },
            "$set": {
                "tracked_habits.$.interacted": dynamic_web.today()
            }
        }
        result = mongo.db.habits.update_one(query, update)

        updated_habit = mongo.db.habits.find_one(query, {"tracked_habits.$": 1})
        new_score = updated_habit["tracked_habits"][0]["score"] if updated_habit else 0
        
        if result.modified_count > 0:
            return jsonify(success=True, max_score=habit_data["max_score"], score=new_score)
        else:
            return jsonify(success=False)
    else:
        return jsonify(success=False, error="Habit not found"), 404

@app.route("/delete_habit/<nickname>/<habit>", methods=["POST"])
def delete_habit(nickname, habit):
    query = {
        "nickname": str(nickname),
        "tracked_habits.habit_name": str(habit),
    }
    
    habit_doc = mongo.db.habits.find_one(query, {"tracked_habits.$": 1})
    if habit_doc:
        result = mongo.db.habits.update_one(
            {"nickname": str(nickname)},
            {"$pull": {"tracked_habits": {"habit_name": str(habit)}}}
        )
        
        if result.modified_count > 0:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Habit not deleted")
    else:
        return jsonify(success=False, error="Habit not found"), 404

@app.route("/seeker/intro",methods=["POST"])
def seeker_intro():
    topics = list(dict(request.form).keys())
    session["askTopics"] = False
    mongo.db.seeker.update_one({"nickname":session["nickname"],"survey":"False"},{"$set":{"survey":"True","topics":topics,"history":""}})
    return redirect("/seeker")

@app.route("/seeker")
def seeker():
    if not session:
        return redirect("/")
    
    user = mongo.db.seeker.find_one({"nickname": session["nickname"]})
    mongo.db.users.update_one({"nickname":session["nickname"]},{"$inc":{"seeker":1}})

    last_fact = user["fotd_last"]
    last_fact_content = user["fotd_last_content"]
    last_fact_topic = user["fotd_last_topic"]

    session["fact_topic"] = str(last_fact_topic).capitalize()
    session["fact"] = last_fact_content

    philosopher_talks = {
        "aristotle":personalizer.get_philosopher_icebreaker("aristotle"),
        "nietzsche":personalizer.get_philosopher_icebreaker("nietzsche"),
        "plato":personalizer.get_philosopher_icebreaker("plato"),
        "socrates":personalizer.get_philosopher_icebreaker("socrates"),
        "confucius":personalizer.get_philosopher_icebreaker("confucius"),
        "descartes":personalizer.get_philosopher_icebreaker("descartes")
    }

    session["philosopher_icebreakers"] = philosopher_talks

    date = datetime.now().strftime(f"%d/%m/%Y")
    if last_fact != date:
        exclude = user.get("facts_history","")
        fact_topic, fact = gemini.get_fotd(user["topics"],exclude)

        session["fact_topic"] = str(fact_topic).capitalize()
        session["fact"] = fact

        personalizer.update_fact_history(session["nickname"],fact,fact_topic)
        mongo.db.seeker.update_one({"nickname":session["nickname"]},{"$set":{"fotd_last":date,"fotd_last_topic":fact_topic,"fotd_last_content":fact}})
        
    if user:
        if not user or not user.get("survey"):
            mongo.db.seeker.insert_one({"nickname": session["nickname"], "survey": "False"})
            session["askTopics"] = True
        
        if user and user.get("survey") == "True":
            session["askTopics"] = False
            user_topics = [str(x).capitalize() for x in user.get("topics", [])]
    else:
        user_topics = []
    
    try:
        user = session["nickname"]
        session["opted_users%"] = home_engine.opted_users_p()
        session["is_opted"] = home_engine.is_opted(session["nickname"])
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        if opted_in_user:
            history = personalizer.get_seeker_history(session["nickname"])
            if not history or history == "":
                icebreaker = dynamic_web.get_seeker_icebreaker()
                session["icebreaker"] = icebreaker
                session["tip"] = dynamic_web.no_history_response(opted=True)
            else:
                icebreaker = gemini.fit_prompt(prompts.prompt_corpus().get_relevant_icebreaker(session["nickname"],history))
                session["tip"] = gemini.fit_prompt(prompts.prompt_corpus().get_tip(history))
                session["icebreaker"] = icebreaker    
            gemini.config_seeker(session["icebreaker"],user,history)
        else:
            icebreaker = dynamic_web.get_seeker_icebreaker()
            session["icebreaker"] = icebreaker
            session["tip"] = dynamic_web.no_history_response(opted=False)
            gemini.config_seeker(session["nickname"],user,None)
        return render_template("seeker.html",talk=session["icebreaker"],philosopher_talks=philosopher_talks,data=data,error=False, user_topics=user_topics, fact=session.get("fact",""),fact_topic = session.get("fact_topic",""))
    except Exception as error:
        print(error)
        return redirect("/")
    
@app.route("/condense_wiki", methods=["POST"])
def condense_wiki():
    data = request.get_json()
    url = data.get('url')
    title = f"wiki/"+url.split('/wiki/')[-1]
    corpus = dynamic_web.wiki_extract(url)
    topics = dynamic_web.wiki_split(corpus)
    
    if corpus == "":
        return jsonify(success="False")
    
    summary = gemini.condense_wiki(title,topics)
    gemini.config_context_seeker(session["nickname"],corpus=summary)
    return jsonify(success=True, title=title, summary=markdown2.markdown(summary))

@app.route("/lift_ban", methods=["POST"])
def lift_ban():
    mongo.db.seeker.update_one({"nickname": session["nickname"]}, {"$set": {"active": 0, "ban_duration": 0, "ban_expiry": None}})
    return redirect("/logout")

@app.route("/chat_seeker",methods=["POST"])
def chat_seeker():
    try:
        message = request.form["message"]
        response, latest_message = gemini.chat_seeker(message)
        user_message = message
        opted_in_user =  mongo.db.opted_users.find_one({"nickname":session["nickname"]})
        if opted_in_user:
            user_in_chats = mongo.db.seeker.find_one({"nickname":session["nickname"]})
            if not user_in_chats:
                mongo.db.seeker.insert_one({"nickname":session["nickname"],"history":""})
            user_in_chats = mongo.db.seeker.find_one({"nickname":session["nickname"]})
            previous_history = user_in_chats["history"]
            if previous_history == "" or previous_history[-1] == "~":
                previous_history += "\n[CHAT] "+session["icebreaker"]
            current_history = personalizer.build_history(previous_history,str(latest_message),user_message,model="Seeker")
            updated_history = mongo.db.seeker.update_one({"nickname":session["nickname"]},{"$set":{"nickname":session["nickname"],"history":current_history}})
        return jsonify(talk=markdown2.markdown(response.text), error=False)
    except Exception as e:
        return jsonify(talk="Seeker could not respond to your request.",error=True)

@app.route("/chat_wiki",methods=["POST"])
def chat_wiki():
    try:
        message = request.form["message"]
        response = gemini.chat_wiki(message)
        html_content = markdown2.markdown(response.text, extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
        return jsonify(talk=html_content, error=False)
    except Exception as e:
        return jsonify(talk="Seeker could not respond to your request.", error=True)

@app.route("/config_philosopher/<token>",methods=["POST"])
def philosopher_mask(token):
    try:
        resp = gemini.config_philosopher(session["nickname"],token,icebreaker=session["philosopher_icebreakers"][token])
        return jsonify(success=True,resp=resp.text)
    except Exception as error:
        print(error)
        return jsonify(success=False,resp=None)
    
@app.route("/chat_philosopher",methods=["POST"])
def philosopher_chat():
    try:
        message = request.form["message"]
        response = gemini.chat_philosopher(message)
        return jsonify(success=True,resp=markdown2.markdown(response.text))
    except Exception as error:
        print(error)
        return jsonify(success=False,resp=None)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=7000)