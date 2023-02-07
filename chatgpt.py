from base import *
import openai
import env
openai.api_key = env.openaiapikey

s = """
12-03-22
:foobar

hey
this is it

12-04-22
:jumper

i like it
12-04-22
:jumper

cmon lets go
"""

def aiprompt():
    promptMessage = 'Hello. What question can I answer for you?'
    #fallback = 'Write a python function to organize and parse this data: ' + quote(s)
    #fallback = 'How many days are there in a year?'
    q = 'organize the following raw data into json: ' + s
    completion = openai.Completion.create(
        engine="text-davinci-003",
        max_tokens=60,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    clip(completion)
    return completion
    return completion.choices[0].text

#pprint(aiprompt())
#"https://platform.openai.com/docs/api-reference/completions/create"

defaultKwargs = dict(
        engine="text-davinci-003",
        max_tokens=60,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
)

history = []
def conversation(message = 'Hello. How may I help you?'):
    global history
    q = prompt(message)
    if not q:
        return clip(history)
    completion = openai.Completion.create(**defaultKwargs, prompt=q)
    text = completion.choices[0].text
    history.append(dict(question=q, answer=text))
    return conversation(text)
    # conversation()
    # it doesnt work
