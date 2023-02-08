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

def aiprompt(prompt):
    completion = openai.Completion.create(
        **defaultKwargs, prompt=prompt
    )
    return completion.choices[0].text

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

#pprint(aiprompt(s))
