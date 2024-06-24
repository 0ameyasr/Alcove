from pymongo import MongoClient
import urllib.parse
import configparser
import requests
import random

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
    prompts = [
    "What are three things you're grateful for today?",
    "Describe a moment when you felt truly at peace.",
    "Write about a time you overcame a significant challenge.",
    "What are your top five personal values?",
    "Who has been the most influential person in your life and why?",
    "What are your goals for the next year?",
    "Describe a perfect day from start to finish.",
    "What are your favorite hobbies and why do you enjoy them?",
    "Write a letter to your future self.",
    "What does success mean to you?",
    "Reflect on a recent dream you had and what it might mean.",
    "What is your earliest childhood memory?",
    "Describe a place where you feel most comfortable and at ease.",
    "What are some ways you can practice self-care?",
    "Write about a time you helped someone else.",
    "What are your strengths and how do you use them?",
    "What is something you've always wanted to learn and why?",
    "How do you handle stress and what are some effective coping mechanisms for you?",
    "Write about a book that had a profound impact on you.",
    "Describe a time when you felt proud of yourself.",
    "What are some of your favorite family traditions?",
    "What does happiness look like to you?",
    "How do you define love?",
    "What are your thoughts on failure and how do you handle it?",
    "Describe a time when you stepped out of your comfort zone.",
    "What are some of your long-term dreams and aspirations?",
    "Write about a memorable trip or vacation.",
    "What qualities do you value most in a friend?",
    "How do you stay motivated when working towards a goal?",
    "What role does creativity play in your life?",
    "Describe a person you admire and why.",
    "What is one habit you want to break and why?",
    "How do you express gratitude in your daily life?",
    "What are some of the most important lessons you've learned in life?",
    "Describe your ideal work environment.",
    "Write about a time when you had to make a difficult decision.",
    "What are some of your favorite ways to relax?",
    "What does your ideal future look like?",
    "How do you balance work and personal life?",
    "Write about a time when you felt truly happy.",
    "What are some of your favorite childhood memories?",
    "How do you deal with negative emotions?",
    "What are your thoughts on change and how do you adapt to it?",
    "Describe a moment when you felt inspired.",
    "What are your favorite ways to spend your free time?",
    "What are some of your biggest fears and how do you confront them?",
    "How do you define success in your personal life?",
    "Write about a time when you experienced a random act of kindness.",
    "What are some goals you have for improving your physical health?",
    "Describe a skill you would like to develop and why.",
    "What are some of your favorite quotes and why do they resonate with you?",
    "Write about a time when you felt misunderstood.",
    "What are your favorite ways to connect with nature?",
    "Describe a moment when you felt a strong sense of community.",
    "What are some of your favorite childhood activities?",
    "How do you practice mindfulness in your daily life?",
    "Write about a time when you made a new friend.",
    "What are some of your favorite things about yourself?",
    "Describe a moment when you felt truly independent.",
    "What are your thoughts on forgiveness and how do you practice it?",
    "What is one thing you would like to change about the world?",
    "How do you stay organized and manage your time effectively?",
    "Write about a time when you felt overwhelmed and how you handled it.",
    "What are some of your favorite memories with your family?",
    "Describe a moment when you felt a deep connection with someone.",
    "What are some of your favorite ways to practice self-love?",
    "What is a lesson you've learned from a difficult experience?",
    "How do you celebrate your achievements?",
    "Write about a time when you felt disappointed and how you coped with it.",
    "What are some of your favorite creative outlets?",
    "Describe a person who has had a positive impact on your life.",
    "What are some of your favorite things to do on a rainy day?",
    "How do you handle criticism and what have you learned from it?",
    "Write about a time when you felt a sense of accomplishment.",
    "What are some of your favorite ways to stay active?",
    "Describe a moment when you felt proud of someone else.",
    "What are your thoughts on taking risks and how do you approach them?",
    "How do you stay connected with loved ones who are far away?",
    "Write about a time when you felt a strong sense of purpose.",
    "What are some of your favorite ways to give back to your community?",
    "Describe a moment when you felt a deep sense of gratitude.",
    "What are your thoughts on personal growth and how do you pursue it?",
    "Write about a time when you learned something new about yourself.",
    "What are some of your favorite ways to unwind after a long day?",
    "How do you stay positive during challenging times?",
    "Write about a time when you felt a sense of belonging.",
    "What are some of your favorite ways to express your creativity?",
    "Describe a moment when you felt truly heard and understood.",
    "What are your thoughts on lifelong learning and how do you embrace it?",
    "Write about a time when you felt a strong sense of empathy.",
    "What are some of your favorite ways to stay mentally healthy?",
    "Describe a moment when you felt a sense of adventure.",
    "What are your thoughts on setting boundaries and how do you practice it?",
    "Write about a time when you felt a sense of peace in nature.",
    "What are some of your favorite ways to celebrate special occasions?",
    "Describe a moment when you felt a strong sense of hope.",
    "What are your thoughts on gratitude and how do you practice it?",
    "Write about a time when you felt a sense of wonder.",
    "What are some of your favorite ways to stay grounded?",
    "Describe a moment when you felt a sense of joy.",
    "What are your thoughts on compassion and how do you practice it?",
    "Write about your biggest fear and how it affects you.",
    "Describe a time when you felt completely lost.",
    "What is a bad habit you struggle to break and why?",
    "Write about a time when you felt deeply disappointed.",
    "What are some of your insecurities and how do they impact you?",
    "Describe a moment when you felt betrayed.",
    "What is a recurring negative thought you have and how do you deal with it?",
    "Write about a time when you felt like a failure.",
    "What are some of the biggest challenges you face in your life right now?",
    "Describe a moment when you felt overwhelmed by stress.",
    "What are some of your fears about the future?",
    "Write about a time when you experienced rejection.",
    "What is something you regret and how does it affect you?",
    "Describe a moment when you felt deep sadness.",
    "What are some negative patterns you notice in your behavior?",
    "Write about a time when you felt isolated.",
    "What are some of your fears related to your personal relationships?",
    "Describe a moment when you felt powerless.",
    "What are some of your fears related to your career or professional life?",
    "Write about a time when you struggled with self-doubt.",
    "What are some of your fears related to your health?",
    "Describe a moment when you felt ashamed.",
    "What are some of your fears about failure?",
    "Write about a time when you felt deeply hurt by someone close to you.",
    "What is something you wish you could change about your past?",
    "Describe a moment when you felt anxious.",
    "What are some of your fears about taking risks?",
    "Write about a time when you felt a lack of control in your life.",
    "What are some of your fears related to your financial situation?",
    "Describe a moment when you felt completely misunderstood.",
    "What are some of your fears about being vulnerable?",
    "Write about a time when you felt judged.",
    "What are some of your fears about the unknown?",
    "Describe a moment when you felt overwhelmed by negative emotions.",
    "What are some of your fears related to change?",
    "Write about a time when you felt like giving up.",
    "What are some of your fears about being alone?",
    "Describe a moment when you felt deep frustration.",
    "What are some of your fears related to social situations?",
    "Write about a time when you felt deeply unmotivated.",
    "What are some of your fears about not meeting expectations?",
    "Describe a moment when you felt extreme guilt.",
    "What are some of your fears about losing control?",
    "Write about a time when you felt consumed by anger.",
    "What are some of your fears about being judged by others?",
    "Describe a moment when you felt completely helpless.",
    "What are some of your fears about being unsuccessful?",
    "Write about a time when you felt deeply conflicted.",
    "What are some of your fears about not being good enough?",
    "Describe a moment when you felt a deep sense of regret."
]
    return random.choice(prompts)