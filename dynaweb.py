import random
import libs
from datetime import datetime, timedelta
import binascii, os
import requests
from urllib.parse import urlparse
import re

class curate_web:
    def __init__(self) -> None:
        pass 

    def get_class_description(self,user_class:str) -> str:
        cleanString = ""
        for char in user_class:
            if char.isalpha():
                cleanString += char
        user_class = cleanString.lower()
        descriptions = {
            "shaman": "Restless, tired, or stressed? Try unwinding and relaxing to let go of your worries and find peace.",
            "ace": "Keep up your productivity and organize yourself to maintain your momentum. Constantly plan and find ways to improve.",
            "challenger": "Engage in puzzles and games to keep your mind active and entertained, especially when your brain feels restless.",
            "generalist": "Explore a variety of activities to discover new hobbies and interests, or to find what truly excites you.",
            "dynamo": "Talk away your boredom by engaging in conversations to find clarity and direction.",
            "seeker": "Embrace your philosophical curiosity and learn new things to satisfy your quest for meaning.",
            "wanderer": "Embark on a journey of discovery and adventure, whether it is exploring the world or your inner self."
        }
        return descriptions[user_class.lower()]
    
    def no_history_response(self,opted):
        return "Once you start interacting with Alcove, results will be reflected. Get started!" if opted else "You are not using Personalization (Turn it on). Once you Opt-In, results will be reflected."
    
    def get_tag_tooltip(self,user_class:str) -> str:
        tooltips = {
            "Shaman": 
                """Relax and engage in mindfulness activities,
                whether it be guided meditation, seeking therapy
                or doing things your way.
                """
            ,
            "Ace": 
                """Utilise your time by planning your routine,
                organizing your schedule or using various tools
                to enhance efficiency. Or, just get some advice.
                """
            ,
            "Challenger":
                """Brainstorm over tricky riddles, challenging
                puzzles or go against an unbeatable opponent
                in various strategy games.
                """
            ,
            "Generalist": 
                """Find a new hobby for yourself, and learn 
                   how to approach it. Or, discover new ways
                   to enrich those you already enjoy!
                """
            ,
            "Dynamo":
                """Engage in quick and dynamic conversations with 
                Dynamo, your AI-chat companion on Alcove"""
            ,
            "Seeker":
                """Debate on various philosophies and paradoxes, or
                just discover something you'd like to learn or know
                about.
                """
            ,
            "Wanderer":
                """Plan your next vacation or discover various points
                of interests and places that you might like. Or, virtually
                explore the world!
                """
        }
        return tooltips[user_class]

    def get_dynamo_icebreaker(self):
        icebreakers = [
        "What's your favorite hobby?",
        "Have you watched any good movies lately?",
        "What's your go-to comfort food?",
        "Do you have any pets?",
        "What's a book that you couldn't put down?",
        "What's your favorite way to spend a weekend?",
        "Do you enjoy any sports or outdoor activities?",
        "What's the best place you've ever traveled to?",
        "What's a skill you'd love to learn?",
        "Do you have a favorite type of music?",
        "What's something you're passionate about?",
        "Do you prefer coffee or tea?",
        "What's a fun fact about yourself?",
        "Do you have a favorite TV show?",
        "What's your dream job?",
        "What's the most interesting thing you've read recently?",
        "Do you enjoy cooking or baking?",
        "What's your favorite season and why?",
        "Have you ever tried a new hobby and stuck with it?",
        "What's a place you'd love to visit someday?",
        "What's your favorite holiday and why?",
        "Do you have a favorite quote or saying?",
        "What's the most memorable concert you've been to?",
        "Do you like to play video games? If so, which ones?",
        "What's your favorite way to relax after a long day?",
        "What's a talent or skill you have that not many people know about?",
        "Do you have a favorite type of cuisine?",
        "What's your favorite board game or card game?",
        "If you could have dinner with any historical figure, who would it be?",
        "What's a recent accomplishment you're proud of?",
        "What's your favorite app on your phone?",
        "Do you enjoy any creative activities, like drawing or writing?",
        "What's a goal you're currently working towards?",
        "What's your favorite animal and why?",
        "If you could instantly master any skill, what would it be?",
        "Do you have a favorite podcast?",
        "What's the best piece of advice you've ever received?",
        "Do you enjoy any outdoor activities, like hiking or camping?",
        "What's your favorite childhood memory?",
        "If you could live in any time period, which would you choose?",
        "Want to talk?",
        "What's up?",
        "How's it going?",
        "Got any plans for today?",
        "How are you feeling right now?",
        "What’s on your mind?",
        "Anything exciting happening lately?",
        "How’s your day been so far?",
        "What are you up to?",
        "Have you done anything fun recently?",
        "What’s new with you?",
        "Feeling bored? Let’s chat!",
        "Got any good stories to share?",
        "What’s the highlight of your day?",
        "Want to share something interesting?",
        "Anything you feel like talking about?",
        "What’s something cool you’ve discovered lately?",
        "Any random thoughts you’d like to share?",
        "Have you seen anything funny online recently?",
        "What’s something that made you smile today?"]
        return random.choice(icebreakers)
    
    def get_shaman_icebreaker(self):
        icebreakers = [
            "What's something you're currently excited about in your life?",
            "If you could travel anywhere in the world right now, where would you go and why?",
            "What's a hobby or activity you enjoy that most people don't know about?",
            "What's one book or movie that has significantly impacted you?",
            "What's a recent accomplishment that you're proud of?",
            "What's one thing you do to relax after a long day?",
            "If you could instantly learn any skill or talent, what would it be?",
            "What's a positive habit you've developed recently?",
            "What's one piece of advice you would give to your younger self?",
            "What's something small that brings you joy on a regular basis?",
            "If you had to describe yourself in three words, what would they be?",
            "What's one thing you're looking forward to in the next few months?",
            "What's a quote or mantra you find particularly inspiring?",
            "What's one thing you wish people understood about you?",
            "What's been on your mind a lot lately?",
            "Is there something you're currently finding challenging or difficult?",
            "What's one thing that's been stressing you out recently?",
            "How have you been feeling about your current work or school situation?",
            "What's one thing you wish you could change about your daily routine?",
            "Have you noticed any changes in your sleep patterns lately?",
            "What's one thing that feels overwhelming for you right now?",
            "Is there something you're currently worried about?",
            "How do you usually cope when you're feeling down or stressed?",
            "Have you been able to find time for yourself recently?",
            "What's one thing that has been bothering you that you'd like to share?",
            "Have you experienced any significant changes in your mood lately?",
            "What's one thing you're struggling with that you'd like some support on?",
            "Is there something you're avoiding that you'd like to address?",
            "How have your relationships been affecting you recently?",
            "What's one fear or concern that's been on your mind?",
            "How have you been managing your time and responsibilities lately?",
            "What's one thing you feel uncertain about right now?",
            "Is there something you wish you could talk about more openly?",
            "How do you feel about the balance between your personal and professional life?",
            "How have you been feeling lately?",
            "Is there something on your mind that's been bothering you?",
            "What do you do when you're feeling overwhelmed?",
            "Who do you usually turn to for support when you're having a tough time?",
            "Have you experienced any changes in your sleep or appetite recently?",
            "What's one thing that's been stressing you out recently?",
            "Are there any changes or decisions in your life that you're currently struggling with?",
            "How do you usually cope with stressful situations?",
            "Is there something you wish you could talk about more openly?",
            "What's one thing that could make your day a little better right now?",
            "How do you usually take care of yourself when you're feeling down?",
            "Is there something you feel proud of handling well recently?",
            "What's been your biggest challenge this week?",
            "How do you feel about the balance between your work and personal life?",
            "Are there any relationships in your life that you're currently concerned about?",
            "How do you usually unwind after a tough day?"
        ]
        return random.choice(icebreakers)
    
    def get_seeker_icebreaker(self):
        icebreakers = [
            "What is a philosophical idea that has deeply influenced your worldview?",
            "If you could have a conversation with any philosopher, past or present, who would it be and why?",
            "What do you think is the purpose of life, or do you believe life has no inherent purpose?",
            "How do you define 'happiness,' and do you think it's achievable for everyone?",
            "What role do you believe free will plays in our lives, if any?",
            "Do you think humans are inherently good, evil, or neutral? Why?",
            "What is one moral or ethical dilemma that you find particularly challenging?",
            "How do you approach the concept of truth? Do you believe in absolute truths or that truth is subjective?",
            "What's a philosophical or existential question you find yourself pondering often?",
            "Do you believe that we have control over our own destiny, or is it predetermined?",
            "What is your stance on the existence of a higher power or the concept of God?",
            "How do you balance individual freedom with societal responsibility?",
            "What does 'justice' mean to you, and do you think it is ever truly attainable?",
            "Do you think the ends justify the means, or is the process more important than the outcome?",
            "How do you make decisions when faced with a moral or ethical dilemma?",
            "What is your view on the nature of reality? Do you believe we can truly know anything?",
            "What do you think is the most important question humanity should be asking right now?",
            "How do you interpret the concept of 'the good life'? What does it look like for you?",
            "Do you believe that people can change, or are we fundamentally the same throughout our lives?",
            "How do you reconcile the idea of suffering with the existence of a just world?",
            "Do you believe in fate, coincidence, or neither? Why?",
            "What is one philosophical book or essay that has had a profound impact on you?",
            "What are your thoughts on the concept of time? Do you think it is linear, cyclical, or something else?",
            "How do you define 'wisdom,' and do you think it's different from knowledge?",
            "What do you believe happens after we die, and how does that belief influence your life?",
            "How do you approach the idea of self-identity? Do you think we create it, or is it something inherent?",
            "What are your thoughts on the relationship between mind and body? Do you believe they are separate or one?",
            "How do you view the concept of freedom? Is it something we truly possess, or is it an illusion?",
            "Do you think it's possible to live a fully authentic life? Why or why not?",
            "What is your perspective on the meaning of existence? Do we create our own meaning, or is it given to us?",
            "What role do you think emotions should play in decision-making?",
            "How do you think technology is influencing our understanding of humanity and existence?",
            "What is your opinion on the idea of moral relativism versus moral absolutism?",
            "How do you interpret the concept of 'beauty'? Is it objective or subjective?",
            "What are your thoughts on the idea of altruism? Do you believe true altruism exists?",
            "How do you navigate the balance between reason and emotion in your life?",
            "What is one philosophical idea you find difficult to accept or understand?",
            "Do you believe that language shapes our thoughts and reality, or is it merely a tool for communication?",
            "How do you approach the concept of mortality, and does it influence the way you live?",
            "What are your thoughts on the idea of universal ethics? Do you believe certain morals apply to everyone?",
            "Do you think there is a distinction between knowledge and belief? If so, how do you define it?",
            "How do you view the relationship between the individual and the collective in society?",
            "What is your perspective on the role of art in understanding the human experience?",
            "Do you think it's more important to seek truth or to seek happiness? Can they coexist?",
            "What is one paradox or contradiction you find intriguing or perplexing?",
            "How do you interpret the concept of love? Is it a feeling, a choice, or something else?",
            "What do you think is the role of suffering in personal growth or development?"
        ]
        return random.choice(icebreakers)
    
    def token16b(self):
        return str(binascii.hexlify(os.urandom(16)))[2:-1]

    def token8b(self):
        return str(binascii.hexlify(os.urandom(8)))[2:-1]

    def today(self):
        today = datetime.now()
        return str(today.strftime("%A"))+", "+str(today.strftime("%d"))+" "+str(today.strftime("%B"))+" "+str(today.strftime("%Y"))
    
    def yesterday(self):
        yesterday = datetime.now() - timedelta(days=1)
        return str(yesterday.strftime("%A"))+", "+str(yesterday.strftime("%d"))+" "+str(yesterday.strftime("%B"))+" "+str(yesterday.strftime("%Y"))

    def now(self):
        today = datetime.now()
        return str(today.strftime("%H:%M"))
    
    def get_radar_questions(self):
        return libs.get_radar_question_set()

    def get_instruction_status(self,response):
        if int(response) != 0:
            return False
        else:
            return True
        
    def wiki_extract(self,url):
        try:
            parsed_url = urlparse(url)
            path = parsed_url.path
            title = path.split('/wiki/')[-1]
            endpoint = 'https://en.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'format': 'json',
                'prop': 'extracts',
                'titles': title,
                'explaintext': True,
                'formatversion': 2
            }
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            pages = data['query']['pages']
            for page in pages:
                page_info = {page["extract"]}
                return page_info.pop()
        except Exception as e:
            return ""
    
    def wiki_split(self,corpus):
        splits = corpus.split("=== ")
        topics = {}
        stop_phrases = ["== See also ==", "== Notes ==", "== References ==", "== External links =="]
        
        for phrase in stop_phrases:
            if phrase in corpus:
                corpus = corpus.split(phrase)[0]
                break
        
        splits = re.split(r'\n==+ (.*?) ==+\n', corpus)
        splits = ['Introduction']+splits
        for i in range(0, len(splits), 2):
            topic_name = splits[i].strip()
            topic_desc = splits[i + 1].strip()

            topic_desc = re.sub(r'\s+', ' ', topic_desc)
            topic_desc = topic_desc.replace('\n', ' ').replace('\r', ' ').strip()

            if topic_desc.strip() != '':
                topics[topic_name] = topic_desc

        return topics
    
    def get_context(self,context):
        duplets = context.split("n\"~")
        for i,dup in enumerate(duplets):
            duplets[i] = re.sub("\"",'',dup)
        return '\n'.join(duplets)

    def issue_catchup(self,last_recorded,now):
        time_since_last = now - last_recorded
        return time_since_last >= timedelta(minutes=1)