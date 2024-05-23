class curate_web:
    def __init__(self) -> None:
        pass 

    def get_class_description(self,user_class:str) -> str:
        descriptions = {
            "shaman": "You may be restless, tired, or just stressed. Or perhaps, you just want to unwind and relax. Let go of your worries and find your peace.",
            "ace": "There's no such thing as free time for you. You're constantly planning ways to get things right and improve every day. Stay productive and organized to keep your momentum going.",
            "challenger": "You desire a constant need for using your brain. Sometimes, it just doesn't want to rest! Engage in puzzles and games to keep your mind active and entertained.",
            "generalist": "Looks like you're quite open-minded. You may want to discover new hobbies and interests, or are just outright confused. Explore a variety of activities to find what truly excites you.",
            "dynamo": "You eye the unassuming. You can never be sure! How about you just talk away your boredom? Engage in conversations to find clarity and direction.",
            "scholar": "You know a lot, or you think you do. Anyways, there's no harm in diving deeper! Immerse yourself in comprehensive reading and expand your knowledge further.",
            "seeker": "Many people don't put thought into their existence! Yet here you are, always thinking and asking. Embrace your philosophical curiosity and learn new things.",
            "wanderer": "'To live is to travel,' said someone wise. Maybe you! Whether exploring the world or your inner self, embark on a journey of discovery and adventure."
        }
        return descriptions[user_class]