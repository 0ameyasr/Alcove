""" 
engine.py

Specifically made for extracting information from the database.
"""

from pymongo import MongoClient
from gemini import fit_prompt
from prompts import prompt_corpus

class engine_client:
    def __init__(self,conn_uri:str) -> None:
        self.client = MongoClient(conn_uri)
        self.q1_tags = {
            '1':"curious",
            '2':"productive",
            '3':"bored",
            '4':"disturbed",
            '5':"eager",
            '6':"stressed",
        }
        self.q2_tags = {
            '1':"learning new things",
            '2':"reading articles (infotainment)",
            '3':"solving challenges and puzzles",
            '4':"productivity tools and organizing themselves",
            '5':"exploring new hobbies and interests",
            '6':"ruminating of philosophy and deep thoughts",
            '7':"mindfulness activities",
        }
        self.q3_tags = {
            '1':"learning new things or philosophies",
            '2':"playing games or watching videos",
            '3':"practicing mindfulness",
            '4':"planning or organizing themselves",
            '5':"discover new hobbies and interests",
            '6':"improve their knowledge",
            '7':"chat or talk",
            '8':"discover and explore new POIs for travel"
        }
        self.q4_tags = {
            '1':"energetic",
            '2':"neutral",
            '3':"restless",
            '4':"curious",
            '5':"stressed",
            '6':"neutral",
        }
        self.q5_tags = {
            '1':"relax",
            '2':"discover new things",
            '3':"organize themselves",
            '4':"learn something new",
            '5':"be engaged in challenges",
            '6':"is open to anything",
        }
        
        try:
            self.client.db.command('ping')
        except Exception as e:
            print("[ERROR] engine_client > __init__(): ",e)

    def build_tags(self,nickname:str) -> list[str]:
        survey = self.client["credentials"]["survey"]
        user_response = survey.find_one({"nickname":nickname})
        if user_response:
            qs_r = [user_response["q1"],user_response["q2"],user_response["q3"],user_response["q4"],user_response["q5"]]
            return [
                self.q1_tags[qs_r[0]],
                self.q2_tags[qs_r[1]],
                self.q3_tags[qs_r[2]],
                self.q4_tags[qs_r[3]],
                self.q5_tags[qs_r[4]],
            ]
        else:
            print("[ERROR] engine_client > build_tags(): No associated survey response found.")
            return None
    
    def opted_users_p(self):
        opted_users = self.client["credentials"]["opted_users"]
        users = self.client["credentials"]["users"]
        return int((opted_users.count_documents({}) / users.count_documents({})) * 100)
    
    def is_opted(self,nickname): 
        return True if self.client["credentials"]["opted_users"].find_one({"nickname":nickname}) else False