from pymongo import MongoClient
import configparser
import random
import libs
import re

def clean_message(message):
    message = re.sub(r'\\(.)', r'\1', message)
    message = message.replace('\\"', '"')
    message = message.replace('\\n', '\n')
    message = re.sub(r'\s+', ' ', message).strip()
    return message

def build_history(conversation_history,latest_message:str,user_message:str,model="Dynamo"):
    trace='role: "model"'
    latest_message = f"{model}: "+latest_message.replace("text: ","").replace("parts {","").replace("}","").replace(trace,"").strip() + "~"
    user_message = "User: "+user_message
    return conversation_history +"\n"+user_message+"\n"+latest_message

def build_project_history(nickname,conversation_history,latest_message:str,user_message:str,model="Dynamo"):
    trace='role: "model"'
    latest_message = f"{model}: "+latest_message.replace("text: ","").replace("parts {","").replace("}","").replace(trace,"").strip() + "~"
    user_message = f"{nickname}: "+user_message+"\n"
    latest_message = clean_message(latest_message)
    user_message = clean_message(user_message)
    return conversation_history +"\n"+user_message+"\n"+latest_message

def get_dynamo_history(nickname):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")

    mongo = MongoClient(config["mongodb"]["uri"])
    chats = mongo["credentials"]["chats"]
    user = chats.find_one({"nickname":nickname})
    
    if user:
        history = str(user["history"])
        history = history.replace("\\n","").replace("\\","").strip()
        return history
    else:
        return ""
    
def get_shaman_history(nickname):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")

    mongo = MongoClient(config["mongodb"]["uri"])
    chats = mongo["credentials"]["shaman"]
    user = chats.find_one({"nickname":nickname})
    
    if user:
        history = str(user["history"])
        history = history.replace("\\n","").replace("\\","").strip()
        return history
    else:
        return ""

def get_seeker_history(nickname):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")

    mongo = MongoClient(config["mongodb"]["uri"])
    chats = mongo["credentials"]["seeker"]
    user = chats.find_one({"nickname":nickname})
    
    if user:
        history = str(user.get("history",""))
        if history != "":
            history = history.replace("\\n","").replace("\\","").strip()
        return history
    else:
        return ""

def get_random_topics(nickname):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")

    mongo = MongoClient(config["mongodb"]["uri"])
    seeker = mongo["credentials"]["seeker"]
    user = seeker.find_one({"nickname":nickname})
    return random.sample(user["topics"],k=3 if len(user["topics"]) >=3 else 1) if user else None

def get_journal_data(token):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")

    mongo = MongoClient(config["mongodb"]["uri"])
    journals = mongo["credentials"]["journals"]
    journal = journals.find_one({"token": token})
    if not journal:
        return None
    return {
        "token": journal["token"],
        "title": journal["title"],
        "date": journal["date"],
        "entry": journal["entry"]
    }

def get_journal_prompt():
    return libs.journal_prompt_lib()
    
def get_question_set(mood,mode):
    if mode == "sun":
        sets = {
            "positive":[
                "What do you look forward to do today?#What inspires you to work hard today?#How are you feeling about the progress you've made today?#How do you plan to keep yourself happy today?#What moments have made you smile today?"
            ],
            "neutral":[
                "What is the first thought that comes to your mind?#How are you navigating through your tasks today?#What has been occupying your thoughts today?#How would you describe your energy levels today?#What has been your focus during the day?"
            ],
            "negative": [
                "What has been troubling you?#What challenges have you faced today?#How have you been coping with stress or difficulties today?#Who or what has been a source of frustration today?#How do you plan to improve your day?"
            ]
        }
        return sets[mood]
    elif mode == "moon":
        sets = {
            "positive":[
                "What was good about your day today?#Why was it good and how did it make you feel?#Who or what made your day special today?#What inspired you today?#How did you make your day better?"
            ],
            "neutral":[
                "How was your day today?#What stands out about your day as it comes to a close?#How are you feeling as the day winds down?#What are your reflections on the day's events?#What are you looking forward to tomorrow?"
            ],
            "negative": [
                "What was bad about your day today?#What disappointed you today?#How did today fall short of your expectations?#What events or interactions left you feeling down today?#What would you like to change about today if you could?"
            ]
        }
        return sets[mood]
    else:
        print("Invalid mode.")
        return None

def build_corpus_history(nickname,date,corpus,mode=0):
    if mode == 1:
        return f"({date}):{corpus}"
    config = configparser.ConfigParser()
    config.read("secrets.cfg")

    mongo = MongoClient(config["mongodb"]["uri"])
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname":nickname})
    return user["corpus"]+f"({date}):{corpus}\n"
   
def build_timeline_history(nickname,date,mood,mode=0):
    mood = mood.replace("\\n","").replace("\\","").strip()
    if mode == 1:
        return f"({date}):{mood}"
    config = configparser.ConfigParser()
    config.read("secrets.cfg")

    mongo = MongoClient(config["mongodb"]["uri"])
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname":nickname})
    return user["history"]+f"({date}):{mood}\n"

def get_timeline(nickname):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")
    mongo = MongoClient(config["mongodb"]["uri"])
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname":nickname})

    if not user:
        return []
    mongo = MongoClient(config["mongodb"]["uri"])
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname":nickname})

    corpus = [entry[13:] for entry in user["corpus"].split("\n") if entry != '']
    moods = [entry[13:] for entry in user["history"].split("\n") if entry != '']
    dates = [entry[:12][1:-1] for entry in user["corpus"].split("\n") if entry != '']
    
    items = list(zip(dates,corpus,moods))
    return items[::-1]

def get_scores(scores):
    sleepIndex = scores['sleepIndex']
    depressionIndex = scores['depressionIndex']
    anxietyIndex = scores['anxietyIndex'] 
    overallMentalHealth = scores['overallMentalHealth'] 
    abnormalcyIndex = scores['abnormalcyIndex']

    pSleep = int((sleepIndex / 21) * 100)
    pDepression = int((depressionIndex / 63) * 100)
    pAnxiety = int((anxietyIndex / 21) * 100)
    pOverall = int((overallMentalHealth / 27) * 100)
    pRisk = int((overallMentalHealth / 11) * 100)
    riskFactor = scores['verdict']

    title = {
        "NONE": "All Good",
        "MILD": "Mild Indication of troubled Mental Health",
        "MOD": "Moderate Indication of troubled Mental Health",
        "SEV": "Severe Indication of troubled Mental Health"
    }

    userScores = {
        "pSleep": pSleep,
        "pDepression": pDepression,
        "pOverall": pOverall,
        "pAnxiety": pAnxiety,
        "pRisk": pRisk,
        "verdict":riskFactor,
        "title": title[riskFactor]
    }
    return userScores

def get_mask_details(nickname):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")
    mongo = MongoClient(config["mongodb"]["uri"])
    masks = mongo["credentials"]["masks"]
    user = masks.find_one({"nickname":nickname})
    if user:
        mask = user["mask"]
        default_mask = user["default_mask"]
        is_default = False if not default_mask else True
        return mask,is_default
    else:
        return None,False

def get_tasks(nickname):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")
    mongo = MongoClient(config["mongodb"]["uri"])
    plans = mongo["credentials"]["plans"]
    user = plans.find_one({"nickname":nickname})
    if user:
        num_tasks = user.get("num_tasks", 0)
        tasks = {key: value for key, value in user.items() if key.startswith("Task ")}
        return num_tasks,tasks
    else:
        return None,None
    
def update_fact_history(nickname,fact,fact_topic):
    config = configparser.ConfigParser()
    config.read("secrets.cfg")
    mongo = MongoClient(config["mongodb"]["uri"])
    seeker = mongo["credentials"]["seeker"]
    try:
        user = seeker.find_one({"nickname":nickname})
        seeker.update_one({"nickname":nickname},{"$set":{"facts_history":user.get("facts_history","")+f"[{fact_topic}]:{fact}"}})
        return True
    except Exception:
        return False
        