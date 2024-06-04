import random
class curate_web:
    def __init__(self) -> None:
        pass 

    def get_class_description(self,user_class:str) -> str:
        descriptions = {
            "shaman": "Restless, tired, or stressed? Try unwinding and relaxing to let go of your worries and find peace.",
            "ace": "Keep up your productivity and organize yourself to maintain your momentum. Constantly plan and find ways to improve.",
            "challenger": "Engage in puzzles and games to keep your mind active and entertained, especially when your brain feels restless.",
            "generalist": "Explore a variety of activities to discover new hobbies and interests, or to find what truly excites you.",
            "dynamo": "Talk away your boredom by engaging in conversations to find clarity and direction.",
            "scholar": "You know a lot, or you think you do. Anyways, there's no harm in diving deeper! Immerse yourself in comprehensive learning and expand your knowledge further.",
            "seeker": "Embrace your philosophical curiosity and learn new things to satisfy your quest for meaning.",
            "wanderer": "Embark on a journey of discovery and adventure, whether it is exploring the world or your inner self."
        }
        return descriptions[user_class.lower()]
    
    def get_tag_tooltip(self,user_class:str) -> str:
        tooltips = {
            "Shaman": [
                "Find your inner peace.",
                "Unwind and let go of worries.",
                "Relax and destress.",
                "Practice mindfulness exercises.",
                "Relax to nature sounds.",
                "Introspect daily.",
                "Grow your first plant.",
                "Meditate for clarity.",
                "Take care of a plant.",
                "Connect with nature."
            ],
            "Ace": [
                "Boost your productivity.",
                "Organize with calendars.",
                "Find your passion.",
                "Organize your week.",
                "Analyze your strengths and weaknesses.",
                "Plan your daily routine.",
                "Utilize your time with the pomodoro technique.",
                "Prepare for interviews.",
                "Set achievable goals.",
                "Track your progress."
            ],
            "Challenger": [
                "Engage in mind puzzles.",
                "Answer a quiz on any topic.",
                "Play a memory game.",
                "Solve a daily challenge.",
                "Brainstorm over riddles.",
                "Challenge an unbeatable opponent.",
                "Test your limits.",
                "Compete in online games.",
                "Enhance your problem solving.",
                "Solve complex riddles."
            ],
            "Generalist": [
                "Explore new activities.",
                "Discover new hobbies.",
                "Find what excites you.",
                "Explore a new hobby.",
                "Try something new.",
                "Find your new pass-time.",
                "Sample diverse interests.",
                "Experiment with crafts.",
                "Learn a new skill.",
                "Discover a new hobby."
            ],
            "Dynamo": [
                "Engage in conversations.",
                "Talk to find clarity.",
                "Discuss anything.",
                "Talk away boredom.",
                "Have a chat.",
                "Improve your soft-skills.",
                "Join discussion groups.",
                "Make a new friend",
                "Debate topics of interest.",
                "Enhance communication skills."
            ],
            "Scholar": [
                "Dive into deep learning.",
                "Expand your knowledge.",
                "Immerse in comprehensive study.",
                "Dive deeper into anything.",
                "Find the best references.",
                "Consolidate what you know.",
                "Research thoroughly.",
                "Study advanced topics.",
                "Read academic papers.",
                "Master complex subjects."
            ],
            "Seeker": [
                "Satisfy your curiosity.",
                "Learn new philosophies.",
                "Embrace your quest for meaning.",
                "Explore philosophy.",
                "Discuss various theories.",
                "Explore metaphysical concepts.",
                "Question life's big ideas.",
                "Debate ethical dilemmas.",
                "Reflect on existential questions.",
                "Contemplate spiritual beliefs."
            ],
            "Wanderer": [
                "Embark on an adventure.",
                "Explore the world.",
                "Journey into discovery.",
                "Plan your next vacation.",
                "Find a new point of interest.",
                "Travel to unknown places.",
                "Discover hidden gems.",
                "Create a travel itinerary.",
                "Experience different cultures.",
                "Navigate new territories."
            ]
        }
        return random.choice(tooltips[user_class])
    
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
