import pandas,random,numpy

def journal_prompt_lib():
    prompt = random.choice(list(pandas.read_csv("data/journal_prompts.csv")["prompts"]))
    return prompt

def get_radar_question_set():
    qset = list(pandas.read_csv("data/radar_questionnaire.csv")["Questions"])
    return qset
