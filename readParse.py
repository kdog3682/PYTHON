from base import *
from next import *

class ReadParseConfig:
    def __init__(self, s):

        m = re.findall('^ *# *(\S+): *(.+)', s, flags=re.M)
        config = dict(m)

        file = config.get('file')

        if not isfile(file) and getExtension(file) == 'json':
            file = npath(resdir, file)

        mode = config.get('mode')
        args = config.get('args')
        debug = config.get('debug')
        arg = config.get('arg')
        outpath = config.get('outpath')
        if not outpath:
            outpath = file
            debug = True

        self.file = file
        self.mode = mode
        self.outpath = outpath
        self.args = args
        self.arg = arg
        self.debug = debug


def readParse(s):
    # m = re.findall('$c', s)
    # m = re.findall('$c', s, flags=re.M)

    chunks = getChunks(s)
    chunk = chunks[-1]
    name = getFunctionName(chunk)

    config = ReadParseConfig(chunk)

    if config.arg:
        argString = toStringArgument(config.arg)
    elif config.args:
        argString = config.args
    elif config.file:
        argString = f"read('{config.file}')"
    else:
        warn('config.args or config.file is required')

    def finish(result):
        if not result:
            return 

        if config.debug:
            blue(linebreak)
            pprint(result)
            blue(linebreak)
            blue('Preview the result before proceeding to write')
            blue('Outpath', config.outpath)
            input()

        if config.outpath:
            write(config.outpath, result)

    code = f"{chunk}\n\nfinish({name}({argString}))"
    exec(code)

    
    
def isQuote(s):
    return test('^[\'"]', s)

def toStringArgument(s):
    if not isPrimitive(s):
        return json.dumps(s)
    if isNumber(s) or isQuote(s):
        return s
    return f"'{s}'"


s = """

def foo(s):

    # file: cssProperties.json
    
    return list(s.values())[0]
"""

readParse(s)
