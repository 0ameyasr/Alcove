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