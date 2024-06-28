import pandas,random,numpy

def journal_prompt_lib():
    prompt = random.choice(list(pandas.read_csv("data/journal_prompts.csv")["prompts"]))
    return prompt

def self_reflection_set():
    return []
