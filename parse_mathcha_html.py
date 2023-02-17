from base import *
import bs4
s = """
<area-container>
<line class="root text-mode selected" style="line-height: 1.4;"><prefix></prefix><blocks><baselineblock class="inline"></baselineblock><block>Grade 4 Quiz</block></blocks></line>

</area-container>
"""


def fa(child, key=0, r=False):
    return child.find_all(key, recursive=r) if key else child.find_all(recursive=r)

def getData(child):
        name = child.name
        text = child.get_text()
        attrs = child.attrs
        return [name, attrs, text]

def runner(parent, key):
    for child in fa(parent, key):
        name = child.name
        grandchildren = fa(child)
        store = []
        for gc in grandchildren:
            elName, attrs, text = getData(gc)
            if 'latex-table-symbol' in attrs.get('class', []):
                ggc = fa(gc, key='line', r=1)
                tableChildren = filter([runner(el, 'blocks') for el in ggc], lambda x: x)
                store.append({'tag': 'table', 'children': tableChildren})

            elif text.strip():
                store.append({'tag': elName, 'text': text})
        return store

def main(s):
    s = textgetter(s)
    s = search('<body[\w\W]+?</body>', s) or s
    soup = bs4.BeautifulSoup(s, "html.parser")
    body = soup.find('area-container')
    children = fa(body)
    assert children

    output = []
    for child in children:
        name = child.name
        if name == 'line':
            value = runner(child, 'blocks')
            if value: output.append(value)

    return output

s = """
<line class="root text-mode" style="line-height: 1.4;"><prefix></prefix><blocks><baselineblock class="inline"></baselineblock><block style="font-weight: bold;">What is </block><compositeblock dir="ltr" class="math-container-symbol role-mathmode-area inline" style="font-size: 17px;"><editarea class="math-mode-font lazy lazyable no-area-container" style="font-family: Asana-Math, Asana;"><line class="" style="line-height: 1.2;"><baselineblock></baselineblock><block class="Normal">11</block><block class="Binary">×</block><block class="Normal">111</block><block class="Punctuation">,</block><block class="Normal">111</block><block class="Punctuation">,</block><block class="Normal">111</block><block class="Relation">=</block><block class="Normal"> </block><block class="Punctuation">?</block></line></editarea></compositeblock></blocks></line>
"""

mathchahtml = '/home/kdog3682/2023/mathcha/index.html'

def parseMathchaHTML():
    pprint(main(mathchahtml))

