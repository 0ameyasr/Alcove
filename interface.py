import google.generativeai as gemini
import configparser
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

def chat_radar(message):
    return dynamo.send_message(message)

def main():
    print("Welcome to the LLM Chat REPL! Type your messages below.")
    print("Type 'exit' or 'quit' to end the chat.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting the chat. Goodbye!")
            break
        
        try:
            response = chat_radar(user_input)
            print(f"LLM: {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
