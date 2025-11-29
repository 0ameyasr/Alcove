"""
personalizer.py

This is a dynamic user content fetcher program that manages the interactions of the system
and the MongoDB backend.

"""

from pymongo import MongoClient
import configparser
import random
import libs
import re


def mongo_client():
    config = configparser.ConfigParser()
    config.read("secrets.cfg")
    return MongoClient(config["mongodb"]["uri"])


def clean_message(message):
    message = re.sub(r"\\(.)", r"\1", message)
    message = message.replace('\\"', '"')
    message = message.replace("\\n", "\n")
    message = re.sub(r"\s+", " ", message).strip()
    return message


def build_history(
    conversation_history, latest_message: str, user_message: str, model="Dynamo"
):
    trace = 'role: "model"'
    latest_message = (
        f"{model}: "
        + latest_message.replace("text: ", "")
        .replace("parts {", "")
        .replace("}", "")
        .replace(trace, "")
        .strip()
        + "~"
    )
    user_message = "User: " + user_message
    return conversation_history + "\n" + user_message + "\n" + latest_message


def build_project_history(
    nickname,
    conversation_history,
    latest_message: str,
    user_message: str,
    model="Dynamo",
):
    trace = 'role: "model"'
    latest_message = (
        f"**{model}**:<br>"
        + latest_message.replace("text: ", "")
        .replace("parts {", "")
        .replace("}", "")
        .replace(trace, "")
        .strip()
        + "<br>"
    )
    user_message = f"**{nickname}**:<br>" + user_message + " <br>"
    return (
        conversation_history + "<br>" + user_message + "<br>" + latest_message + "<br>"
    )


def get_dynamo_history(nickname):
    mongo = mongo_client()
    chats = mongo["credentials"]["chats"]
    user = chats.find_one({"nickname": nickname})

    if user:
        history = str(user["history"])
        history = history.replace("\\n", "").replace("\\", "").strip()
        return history
    else:
        return ""


def get_shaman_history(nickname):
    mongo = mongo_client()
    chats = mongo["credentials"]["shaman"]
    user = chats.find_one({"nickname": nickname})

    if user:
        history = str(user["history"])
        history = history.replace("\\n", "").replace("\\", "").strip()
        return history
    else:
        return ""


def get_seeker_history(nickname):
    mongo = mongo_client()
    chats = mongo["credentials"]["seeker"]
    user = chats.find_one({"nickname": nickname})

    if user:
        history = str(user.get("history", ""))
        if history != "":
            history = history.replace("\\n", "").replace("\\", "").strip()
        return history
    else:
        return ""


def get_random_topics(nickname):
    mongo = mongo_client()
    seeker = mongo["credentials"]["seeker"]
    user = seeker.find_one({"nickname": nickname})
    return (
        random.sample(user["topics"], k=3 if len(user["topics"]) >= 3 else 1)
        if user
        else None
    )


def get_journal_data(token):
    mongo = mongo_client()
    journals = mongo["credentials"]["journals"]
    journal = journals.find_one({"token": token})
    if not journal:
        return None
    return {
        "token": journal["token"],
        "title": journal["title"],
        "date": journal["date"],
        "entry": journal["entry"],
    }


def get_journal_prompt():
    return libs.journal_prompt_lib()


def get_question_set(mood, mode):
    if mode == "sun":
        sets = {
            "positive": [
                "What do you look forward to do today?#What inspires you to work hard today?#How are you feeling about the progress you've made today?#How do you plan to keep yourself happy today?#What moments have made you smile today?"
            ],
            "neutral": [
                "What is the first thought that comes to your mind?#How are you navigating through your tasks today?#What has been occupying your thoughts today?#How would you describe your energy levels today?#What has been your focus during the day?"
            ],
            "negative": [
                "What has been troubling you?#What challenges have you faced today?#How have you been coping with stress or difficulties today?#Who or what has been a source of frustration today?#How do you plan to improve your day?"
            ],
        }
        return sets[mood]
    elif mode == "moon":
        sets = {
            "positive": [
                "What was good about your day today?#Why was it good and how did it make you feel?#Who or what made your day special today?#What inspired you today?#How did you make your day better?"
            ],
            "neutral": [
                "How was your day today?#What stands out about your day as it comes to a close?#How are you feeling as the day winds down?#What are your reflections on the day's events?#What are you looking forward to tomorrow?"
            ],
            "negative": [
                "What was bad about your day today?#What disappointed you today?#How did today fall short of your expectations?#What events or interactions left you feeling down today?#What would you like to change about today if you could?"
            ],
        }
        return sets[mood]
    else:
        print("Invalid mode.")
        return None


def build_corpus_history(nickname, date, corpus, mode=0):
    if mode == 1:
        return f"({date}):{corpus}"

    mongo = mongo_client()
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname": nickname})
    return user["corpus"] + f"({date}):{corpus}\n"


def build_timeline_history(nickname, date, mood, mode=0):
    mood = mood.replace("\\n", "").replace("\\", "").strip()
    if mode == 1:
        return f"({date}):{mood}"

    mongo = mongo_client()
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname": nickname})
    return user["history"] + f"({date}):{mood}\n"


def get_timeline(nickname):
    mongo = mongo_client()
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname": nickname})

    if not user:
        return []

    mongo = mongo_client()
    timelines = mongo["credentials"]["timeline"]
    user = timelines.find_one({"nickname": nickname})

    corpus = [entry[13:] for entry in user["corpus"].split("\n") if entry != ""]
    moods = [entry[13:] for entry in user["history"].split("\n") if entry != ""]
    dates = [entry[:12][1:-1] for entry in user["corpus"].split("\n") if entry != ""]

    items = list(zip(dates, corpus, moods))
    return items[::-1]


def get_scores(scores):
    sleepIndex = sum(scores[0:4])
    anxietyIndex = sum(scores[4:9])
    depressionIndex = sum(scores[9:15])
    abnormalcyIndex = sum(scores[15:17])

    pSleep = int((sleepIndex / 12) * 100)
    pDepression = int((depressionIndex / 18) * 100)
    pAnxiety = int((anxietyIndex / 15) * 100)
    pAbnormal = int((abnormalcyIndex / 6) * 100)
    riskFactor = scores[-1]

    title = {
        "NONE": "All Good",
        "MILD": "Mild Indication of troubled Mental Health",
        "MODERATE": "Moderate Indication of troubled Mental Health",
        "SEVERE": "Severe Indication of troubled Mental Health",
    }

    return {
        "pSleep": pSleep,
        "pDepression": pDepression,
        "pAbnormal": pAbnormal,
        "pAnxiety": pAnxiety,
        "verdict": riskFactor,
        "title": title[riskFactor],
    }


def get_mask_details(nickname):
    mongo = mongo_client()
    masks = mongo["credentials"]["masks"]
    user = masks.find_one({"nickname": nickname})
    if user:
        mask = user["mask"]
        default_mask = user["default_mask"]
        is_default = False if not default_mask else True
        return mask, is_default
    else:
        return None, False


def get_tasks(nickname):
    mongo = mongo_client()
    plans = mongo["credentials"]["plans"]
    user = plans.find_one({"nickname": nickname})
    if user:
        num_tasks = user.get("num_tasks", 0)
        tasks = {key: value for key, value in user.items() if key.startswith("Task ")}
        return num_tasks, tasks
    else:
        return None, None


def update_fact_history(nickname, fact, fact_topic):
    mongo = mongo_client()
    seeker = mongo["credentials"]["seeker"]
    try:
        user = seeker.find_one({"nickname": nickname})
        seeker.update_one(
            {"nickname": nickname},
            {
                "$set": {
                    "facts_history": user.get("facts_history", "")
                    + f"[{fact_topic}]:{fact}"
                }
            },
        )
        return True
    except Exception:
        return False


def get_philosopher_icebreaker(philosopher):
    philosopher_icebreakers = {
        "socrates": "What insights from questioning the world around you are you seeking today?",
        "nietzsche": "What strength do you want to build by overcoming challenges in your life?",
        "confucius": "What lessons of balance and harmony do you hope to find today?",
        "plato": "What truths about the world beyond what we see are you looking to discover?",
        "aristotle": "What virtues are you hoping to cultivate in yourself today?",
        "descartes": "What thoughts or doubts are you wrestling with to find clarity today?",
    }
    return philosopher_icebreakers[philosopher]


def get_top_tools(nickname):
    mongo = mongo_client()
    users = mongo["credentials"]["users"]
    user = users.find_one({"nickname": nickname})

    tool_hits = {
        "dynamo": user["dynamo"],
        "ace": user["ace"],
        "seeker": user["seeker"],
        "shaman": user["shaman"],
    }

    sorted_tools = dict(
        sorted(tool_hits.items(), key=lambda item: item[1], reverse=True)
    )
    return [item.capitalize() for i, item in enumerate(sorted_tools) if i <= 2]
