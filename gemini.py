import google.generativeai as gemini
import configparser
import numpy
import tensorflow
import prompts
import personalizer
config = configparser.ConfigParser()
config.read("secrets.cfg")

gemini.configure(api_key=config['gemini']['api_key'])
model = tensorflow.keras.saving.load_model("model/RADAR_F1_92")

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

def fit_prompt(prompt):
    gemini.configure(api_key=config['gemini']['api_key'])
    model =gemini.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def config_dynamo(icebreaker,nickname,history):
    resp = dynamo.send_message(prompts.prompt_corpus([]).get_chat_config(icebreaker,nickname,history,mode="dynamo"))
    return resp

def config_shaman(icebreaker,nickname,history):
    resp = shaman.send_message(prompts.prompt_corpus([]).get_chat_config(icebreaker,nickname,history,mode="shaman"))
    return resp

def config_ace(nickname):
    print("Ace talk")
    resp = ace.send_message(prompts.prompt_corpus([]).get_chat_config("How can I help you?",nickname,history="",mode="ace"))
    return resp
    
def chat_dynamo(message):
    return dynamo.send_message(message),dynamo.history[-1]

def chat_shaman(message):
    return shaman.send_message(message),shaman.history[-1]

def radar_config():
    response = radar.send_message(prompts.prompt_corpus([]).get_radar_prompt())
    return response.text.strip()

def chat_radar(message):
    return radar.send_message(message)

def manually_scale_score(score, mean, variance):
    scaled_score = (score - mean) / numpy.sqrt(variance)
    return scaled_score

def get_clean_radar_history():
    history = str(radar.history)
    return str([s.replace('\n','').replace('\"','').replace("text:","").replace("}role: model","").replace("}role: user","").replace("]","").replace("\\n","").strip() for s in history.split(', parts {')[1:]])

def make_radar_verdict(score):
    mean = numpy.array([13.51438053, 10.51106195, 19.08960177, 10.33517699, 5.35066372])
    variance = numpy.array([64.8117401, 42.55961215, 147.59042285, 43.71398382, 12.14584027])
    score = manually_scale_score([score],mean,variance)
    p = list(list(model.predict(score))[0])
    risks = ["NONE","MILD","MOD","SEV"]
    max,maxi = float("-inf"),0
    for i in range(len(p)):
        if p[i] > max:
            max = p[i]
            maxi = i
    return risks[maxi]

def get_radar_concerns(history):
    return fit_prompt(prompts.prompt_corpus().get_radar_concerns(history))

def chat_ace(message):
    return ace.send_message(message)