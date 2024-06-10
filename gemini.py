import google.generativeai as gemini
import configparser
import prompts
import personalizer
config = configparser.ConfigParser()
config.read("secrets.cfg")

gemini.configure(api_key=config['gemini']['api_key'])
model =gemini.GenerativeModel(model_name="gemini-1.5-flash",safety_settings = [
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
dynamo = model.start_chat(history=[])

def fit_prompt(prompt):
    gemini.configure(api_key=config['gemini']['api_key'])
    model =gemini.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def config_dynamo(icebreaker,nickname,history):
    resp = dynamo.send_message(prompts.prompt_corpus([]).get_chat_config(icebreaker,nickname,history))
    return resp

def chat_dynamo(message):
    return dynamo.send_message(message),dynamo.history[-1]