from pymongo import MongoClient
import urllib.parse
import configparser
import requests
import random
import libs

def build_history(conversation_history,latest_message:str,user_message:str,model="Dynamo"):
    trace='role: "model"'
    latest_message = "{model}: "+latest_message.replace("text: ","").replace("parts {","").replace("}","").replace(trace,"").strip() + "~"
    user_message = "User: "+user_message

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

def get_clean_history(nickname,mode="dynamo"):
    history = get_dynamo_history(nickname) if mode=="dynamo" else get_shaman_history(nickname)
    count_chats = history.count("[CHAT]")
    duplex_pairs = history.split("~")

    if count_chats > 30:
        duplex_pairs = duplex_pairs[29:]
        config = configparser.ConfigParser()
        config.read("secrets.cfg")
        mongo = MongoClient(config["mongodb"]["uri"])
        chats = mongo["credentials"]["chats"] if mode=="dynamo" else mongo["credentials"]["shaman"]
        updated_history = ''.join(duplex_pairs)
        chats.update_one({"nickname":nickname},{"$set":{"history":updated_history}})
        return updated_history
    else:
        return history

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
    return random.choice(libs.journal_prompt_lib())