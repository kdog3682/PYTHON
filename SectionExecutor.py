from helpers.sprawl_lines import sprawl_lines
from helpers.get_parameters import get_parameters
from utils import *
import SectionExecutorApps

def execute_section(lineNumber = None):
    # get the section text
    python_example_file = "/home/kdog3682/PYTHON/examples.py"
    text = read(python_example_file)
    lines = text.split("\n")
    if not lineNumber:
        lineNumber = len(lines) - 1
        # no lineNumber means we run the last section

    section = sprawl_lines(lines, lineNumber, "^-{20,} *$")
    section_text = join(section, "\n")

    # get a config dictionary
    config = colon_dict(section_text)
    config_keys = config.keys()

    # find the control_item used to evaluate `config`
    # the crux is that one of the `config_keys` must exist in `identifiers` 
    def control_item_finder(item):
        identifiers = item.get("identifiers")
        if identifiers and every(identifiers, config_keys):
            return item

    def run(item, config):

        def get(arg_key):
            value = config.get(arg_key, None)
            if value == None and "aliases" in item:
                aliased_arg_key = item["aliases"].get(arg_key)
                assertion(aliased_arg_key)
                value = config.get(aliased_arg_key)
            assertion(value)
            return value
                
        fn_key = item.get("fn")
        fn = getattr(SectionExecutorApps, fn_key)
        assertion(fn)
        arg_list, kwarg_list = get_parameters(fn)
        args = map(arg_list, get)
        kwargs = reduce(kwarg_list, lambda x: (x, get(x)))
        value = fn(*args, **kwargs)
        return value
    
    item = find(SectionExecutorApps.CONTROL_ITEMS, control_item_finder)
    assertion(item, message = "no identifier must have matched")
    result = run(item, config)
    if result:
        print(result)


env.GLOBAL_DEBUG_FLAG = 2
env.GLOBAL_DEBUG_FLAG = 0
package_manager(execute_section)
