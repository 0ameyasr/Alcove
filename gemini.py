import google.generativeai as gemini
import configparser
import prompts
config = configparser.ConfigParser()
config.read("secrets.cfg")

gemini.configure(api_key=config['gemini']['api_key'])
model =gemini.GenerativeModel(model_name="gemini-pro")
dynamo = model.start_chat(history=[])

def fit_prompt(prompt):
    gemini.configure(api_key=config['gemini']['api_key'])
    model =gemini.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def config_dynamo(icebreaker):
    resp = dynamo.send_message(prompts.prompt_corpus([]).get_chat_config(icebreaker=icebreaker))
    return resp

def chat_dynamo(message):
    print(dynamo.history)
    return dynamo.send_message(message)