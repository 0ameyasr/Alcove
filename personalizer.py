from pymongo import MongoClient
import configparser

def build_history(conversation_history,latest_message:str,user_message:str):
    trace='role: "model"'
    latest_message = "Dynamo: "+latest_message.replace("text: ","").replace("parts {","").replace("}","").replace(trace,"").strip() + "~"
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
