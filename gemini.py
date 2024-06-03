import google.generativeai as gemini
import configparser
config = configparser.ConfigParser()
config.read("secrets.cfg")

def fit_prompt(prompt):
    gemini.configure(api_key=config['gemini']['api_key'])
    model =gemini.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content(prompt)
    return response.text