from base import *
from next import *
import json
import requests
import env

env.appscripturl = '''https://script.google.com/macros/s/AKfycbw1kpOPSxeIZ4WR7ez09JyIguilWE7_Twg4O9ArOTrnPIE_rZrhVax_qT54suL_AKUL/exec

this one works pretty well



this is the newest one


https://script.google.com/macros/s/AKfycbzR4RdFQ1B_SjloSw3Yy05gbDHpN9qYqCFqOT_xNeiz77VeIugHJ_KEugQdvcv14hUZwQ/exec

reverting to version 1
https://script.google.com/macros/s/AKfycbw1kpOPSxeIZ4WR7ez09JyIguilWE7_Twg4O9ArOTrnPIE_rZrhVax_qT54suL_AKUL/exec
'''

def getUrl(s):
    return re.split('\s+', s.strip())[-1]

def appscript(file = '/home/kdog3682/2023/googleAppScript2.js'):
    code = read(file)
    url = getUrl(env.appscripturl)
    response = requests.post(url, code, timeout = 10)
    result = json.loads(response.text)
    if result.get('open'): ofile(result.get('open'))
    if result.get('clip'): clip(result.get('clip'))
    if result.get('value'): print('value', result.get('value'))
    if result.get('error'): print('main errr', result.get('error'))
    if result.get('caughtErrors'): pprint(result.get('caughtErrors'))
    if result.get('logs'): pprint(result.get('logs'))
    pprint(result)

appscript()
