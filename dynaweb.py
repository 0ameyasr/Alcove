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
        return descriptions[user_class]