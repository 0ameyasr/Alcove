"""
libs.py

Fetches some of the hefty textual data stored in .csv files. This stores
only static content and interacts with the local data folder.

"""

import pandas
import random


def journal_prompt_lib():
    prompt = random.choice(list(pandas.read_csv("data/journal_prompts.csv")["prompts"]))
    return prompt


def get_radar_question_set():
    qset = list(pandas.read_csv("data/radar_questionnaire_v2.csv")["Questions"])
    return qset
