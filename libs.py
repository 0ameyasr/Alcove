import pandas,random,numpy

def journal_prompt_lib():
    return random.choice(list(pandas.read_csv("data/journal_prompts.csv")["prompts"]))

def self_reflection_set():
    return []

print(journal_prompt_lib())