import openai
import env

openai.api_key = env.openaiapikey

defaultKwargs = dict(
    engine="text-davinci-003",
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)

def ask(s):
    completion = openai.Completion.create(
        **defaultKwargs, prompt=s, max_tokens=3000
    )
    return completion.choices[0].text


