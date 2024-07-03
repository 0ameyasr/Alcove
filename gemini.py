import google.generativeai as gemini
import configparser
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
    
def chat_dynamo(message):
    return dynamo.send_message(message),dynamo.history[-1]

def chat_shaman(message):
    return shaman.send_message(message),shaman.history[-1]

def radar_config():
    response = radar.send_message(prompts.prompt_corpus([]).get_radar_prompt())
    return response.text

def chat_radar(message):
    return radar.send_message(message)

# if __name__ == "__main__":
#     resp = radar.send_message(prompts.prompt_corpus([]).get_radar_prompt())
#     print(resp.text.strip())
#     while "END" not in resp:
#         msg = input("Message: ")
#         resp = radar.send_message(msg)
#         if "$" in resp.text:
#             print(resp.text)
#             break
#         print(resp.text.strip())