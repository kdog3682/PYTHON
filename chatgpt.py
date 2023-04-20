from base import *
from next import *
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

#Summarize what the following function does and put the results into a json:
s = '''
Write the function below as javascript:

function Node2()
    let tail = Tail()
    if tail == 'app-main.js'
        call BasePY('gac')
    elseif tail == 'worksheet-components.js'
        call VisualAction('vt')
    else
        call PuppetRunner()
    endif
endfunction
'''

def ask(s):
    pprint(s)
    completion = openai.Completion.create(
        **defaultKwargs, prompt=s, max_tokens=3000
    )
    pprint(completion)
    return completion.choices[0].text

def aiprompt(q):
    completion = openai.Completion.create(
        **defaultKwargs, prompt=q
    )
    s = completion.choices[0].text
    if s and prompt(gpt_result=s):
        clipsave(s)


#"https://platform.openai.com/docs/api-reference/completions/create"

defaultKwargs = dict(
        engine="text-davinci-003",
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

#pprint(aiprompt(s))
s = """
Create a title for the following math question:

It's Saturday which means Hammy is playing the walnut game.
Here's how the game works.

You start with 17 walnuts in jar A.
You start with 0 walnuts in jar B.
The goal is to transfer all of the walnuts into jar B.

Rule #1: When you move walnuts out of Jar A, you have to take them out 5 at a time.

Rule #2: When you move walnuts out of Jar B, you have to move them out 3 at a time.

How many moves will it take Hammy to move all 17 walnuts from Jar A into Jar B?
"""

#pprint(aiprompt(s))

