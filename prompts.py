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
        
    def boredom_proverb(self):
        return "Generate a random proverb on boredom or being idle, like 'An empty mind is the Devil's Lair' [ONLY RETURN THE PROVERB]"
    
    def boredom_advice(self,proverb):
        return f"Based on the proverb {proverb}, generate 3-4 sentences of advice. [ONLY RETURN A PARAGRAPH]"

# from gemini import fit_prompt
# proverb = fit_prompt(prompt_corpus([]).boredom_proverb())
# print(f"{proverb}\n{fit_prompt(proverb)}")
