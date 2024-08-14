import google.generativeai as gemini
import configparser
import numpy
import torch
import prompts
import personalizer
config = configparser.ConfigParser()
config.read("secrets.cfg")

gemini.configure(api_key=config['gemini']['api_key'])

modelDynamo =gemini.GenerativeModel(model_name="gemini-1.5-flash",safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "HIGH",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "HIGH",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "MEDIUM",
    },
])
dynamo = modelDynamo.start_chat(history=[])

modelShaman =gemini.GenerativeModel(model_name="gemini-1.5-flash",safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "HIGH",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "HIGH",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
])
shaman = modelShaman.start_chat(history=[])

modelRadar =gemini.GenerativeModel(model_name="gemini-1.5-flash",safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
])
radar = modelRadar.start_chat(history=[])

modelAce =gemini.GenerativeModel(model_name="gemini-1.5-flash",safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "HIGH",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "HIGH",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "MEDIUM",
    },
])
ace = modelAce.start_chat(history=[])

projectModelAce =gemini.GenerativeModel(model_name="gemini-1.5-flash",safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "HIGH",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "HIGH",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
        ])
project_ace = modelAce.start_chat(history=[])

def fit_prompt(prompt):
    gemini.configure(api_key=config['gemini']['api_key'])
    model=gemini.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def config_dynamo(icebreaker,nickname,history,instructions):
    resp = dynamo.send_message(prompts.prompt_corpus([]).get_chat_config(icebreaker,nickname,history,mode="dynamo",mask=instructions))
    return resp

def config_shaman(icebreaker,nickname,history):
    resp = shaman.send_message(prompts.prompt_corpus([]).get_chat_config(icebreaker,nickname,history,mode="shaman"))
    return resp

def config_ace(nickname):
    resp = ace.send_message(prompts.prompt_corpus([]).get_chat_config("How can I help you?",nickname,history="",mode="ace"))
    return resp

def reset_project_ace_history():
    return projectModelAce.start_chat(history=[])

def config_project_ace(nickname,project_title,project_details,project_tasks,context):    
    global project_ace
    project_ace = reset_project_ace_history()
    config = prompts.prompt_corpus([]).get_ace_project_config(nickname,project_title,project_details,project_tasks,context)
    _ = project_ace.send_message(config)
    return project_ace
    
def chat_dynamo(message):
    return dynamo.send_message(message),dynamo.history[-1]

def chat_shaman(message):
    return shaman.send_message(message),shaman.history[-1]

def chat_ace(message):
    return ace.send_message(message)

def chat_project_ace(message):
    return project_ace.send_message(message),project_ace.history[-1]

def radar_config():
    response = radar.send_message(prompts.prompt_corpus([]).get_radar_prompt())
    return response.text.strip()

def chat_radar(message):
    return radar.send_message(message)

def get_clean_radar_history():
    history = str(radar.history)
    return str([s.replace('\n','').replace('\"','').replace("text:","").replace("}role: model","").replace("}role: user","").replace("]","").replace("\\n","").strip() for s in history.split(', parts {')[1:]])

def get_radar_concerns(history):
    return fit_prompt(prompts.prompt_corpus().get_radar_concerns(history))

def chat_ace(message):
    return ace.send_message(message)
