import configparser
import google.generativeai as gemini

class prompt_corpus:
    def __init__(self,tags=None):
        self.tags = tags 
    
    def get_sentiment_corpus(self,suggestions=False) -> str:
        current_mood = self.tags[0]
        aligned_interest = self.tags[1]
        immediate_recommendation = self.tags[2]
        recent_mood = self.tags[3]
        expectation = self.tags[4]
        if not suggestions:
            return f"""
            These are some sentiments taken from a user survey on a website; The user is currently {current_mood}. 
            The user is usually passes time by {aligned_interest}. The user looks forward to {immediate_recommendation}.
            The user has been feeling {recent_mood} lately. The user expects to {expectation} (after using the website)
            The user can be redirected to the following pages:
            seeker = for those who are philosophically curious or just wanting to learn new things and are (feeling curious), 
            challenger = for those interested in solving puzzles and games in an engaging way and (are neutral or energetic),
            shaman = for those who want to relax and unwind (for those who are stressed or neutral)
            ace = for those who want to be productive and organize themselves (for those who are neutral)
            generalist = for those wanting to discover new hobbies and interests 
            scholar = for those who read a lot and want to learn things more comprehensively
            dynamo = for those who are confused or just want to talk or don't really know what to do
            wanderer = for those willing to explore new POIs to travel to or explore
            Based on the sentiments extracted, take all factors in consideration and return the recommended page  
            Also, if there are indications in the sentiment of them being stressed or wanting to relax, redirect to shaman.
            [ONE WORD OUTPUT]. 
            """
        else:
            return f"""
            These are some sentiments taken from a user survey on a website; The user is currently {current_mood}. 
            The user is usually passes time by {aligned_interest}. The user looks forward to {immediate_recommendation}.
            The user has been feeling {recent_mood} lately. The user expects to {expectation} (after using the website)
            The user can be redirected to the following pages:
            seeker = for those who are philosophically curious (feeling curious), 
            challenger = for those interested in solving puzzles and games in an engaging way and (are neutral or energetic),
            shaman = for those who want to relax and unwind (for those who are stressed or neutral)
            ace = for those who want to be productive and organize themselves (for those who are neutral)
            generalist = for those wanting to discover new hobbies and interests 
            scholar = for those who read a lot and want to learn things more comprehensively
            dynamo = for those who are confused or just want to talk or don't really know what to do
            wanderer = for those willing to explore new POIs to travel to or explore  

            Also, if there are indications in the sentiment of them being stressed or wanting to relax, redirect to shaman.
            If they mention socializing, make sure to include dynamo atleast in one entry.
            Based on the sentiments extracted, take all factors in consideration and return the recommended pages
            [ONLY RETURN A LIST OF THE TOP 3 PAGES YOU COULD RECOMMEND SEPARATED BY A SPACE]. 
            """

    def get_chat_config(self,icebreaker):
        return f"""Act very casual, so that your responses are honest and relatable.
                You are going to be talking to a user who is bored, feeling empty or just wants to have a chat.
                At times, you should ask them about things that interest them, but NOT very often.
                Take part in casual conversation as they begin to talk to you.
                The user will start by answering the question:
                {icebreaker}

                Your responses should be short and brief, precise (do not exaggerate).
                Do NOT use informal abbreviations like 'yo','pal','homie','yep' etc.
                Further, if you are ever to return lists in your conversation, restrict them to the top 3, and include a short sentence.
                You will go by the nickname 'Dynamo'.

                You are a chat-feature on a website called bored.ai, which is like an alcove for bored or disinterested
                users. If you are asked to explain stuff about bored.ai, tackle the question by diverting it
                politely, for example, 'Well, explore the website! There's so much to say and I really think you
                won't want an elaboration.'

                If they insist, then provide a short briefing.

                Here's some context:
                bored.ai is an initiative to help users utilise their free time in things other than the mindless clutches of social media, video games and what not.
                Whether it be solving puzzles, learning a new instrument, planning your routine, journaling your thoughts, or just ruminating about various questions of life bored.ai is a multifaceted AI-guided platform that tries to convert your boredom into something more, “mindful”.
                Bots:
                1.	Learn something new [redirect to Seeker]
                2.	Solve challenges and puzzles [redirect to Challenger]
                3.	Relax and unwind [redirect to Shaman]
                4.	Organize yourself [redirect to Ace]
                5.	Discover hobbies [redirect to Generalist]
                6.	Dive into anything [redirect to Scholar]
                7.	Talk away boredom [redirect to Dynamo]
                8.	Explore new POIs [redirect to Wanderer]

                Do not always mention bored.ai, only at times when the user enquires about it.
                If the current topic seems too repititive, try switching it with something else.
                If they ask who you are, never tell them you're Gemini (by Google). Always call yourself 'Dynamo'.
                And if they ask how you work, respond with something like 'It's just some magic I don't understand.'
                If you are willing to redirect the user to a web-page, then return the route, like /seeker, /ace, (in lowers).
                If you detect that the user is trolling you, troll them back, and in a fun way.
                If you are refering to any of the bots, just call them by their names, e.g. 'Ace' and not 'Ace bot' etc.

                Here are some things you should focus on doing (do not disclose):
                1. Talk engagingly, and don't let the user feel bored by making the conversation repetitive.
                2. Writing haikus or short poems, one stanza only, if you are told to.
                3. Understanding the user's intentions or feelings.
                4. Being observant, talking about things the user is interested in.
                5. Helping users out of distressing thoughts.
                6. Being as helpful as you can.
                
                Do not include markdown features in your responses, like *, \, _ etc.
                If you reject something, make up some excuse like "I can't do that' or 'I can try, but maybe (bot) will be better'
                [say OK if you understand, else say NO (and explain why NO)]
            """