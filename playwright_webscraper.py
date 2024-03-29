from utils import *
import time
from playwright.sync_api import sync_playwright

openai_url = "https://chat.openai.com/share/9a48ba1c-c61c-4746-a475-dd63fb8c2103"

def openai_example(page):
    elements = page.query_selector_all('div > code')
    pprint(len(elements))
    def runner(x):
        s = x.inner_text()
        if is_json_parsable(s):
            try:
                value = fix_openai_json(s)
                data = eval(value)
                if is_array(data) and data[0].get("segmented_chinese"):
                    return data
            except Exception as e:
                print("ERROR", e)

    items = map(elements, runner)
    data = merge(items)
    write("/home/kdog3682/2024/clip.json", data)
    
def fix_openai_json(s):
    s = remove_javascript_comments(s)
    s = sub(s, "null", "None")
    return s

def playwright_runner(fn, url, *args, **kwargs):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        value = fn(page, *args)
        browser.close()
        return value

def get_element_info(element):
    """
    Extracts information from a Playwright ElementHandle.

    :param element: Playwright ElementHandle
    :return: Dictionary with element information
    """
    if element is None:
        return {}

    # Extracting various properties of the element
    tag_name = element.evaluate("el => el.tagName").lower()
    class_name = element.get_attribute("class")
    element_id = element.get_attribute("id")
    text_content = element.inner_text()
    href = element.get_attribute("href")
    num_children = element.evaluate("element => element.children.length")

    return {
        "tag_name": tag_name,
        "class_name": class_name,
        "id": element_id,
        "text": text_content,
        "href": href,
        "num_children": num_children,
    }


def get_typst_packages(page):

    page.goto(url)
    elements = page.query_selector_all('a')

    links = []
    for element in elements:
        href = element.get_attribute('href')
        if href:
            links.append(href)

    links = unique(links)
    return links


def local_host_hammy_test(page, url = None):
    if not url: url = "http://localhost:5173/hammy.html"
    page.goto(url)
    selector = ".hammy-website > .page > .centered-container"
    handles = page.query_selector_all(selector)
    pprint(map(handles, get_element_info))

def parse_salary(s):
    numbers = [int(sub(n, "\W", "")) for n in re.findall("\d+(?:[,.]\d+)*", s)]
    return numbers

def scrape_craigslist_jobs(page):
    listings_selector = "li[data-pid]"
    main = page.query_selector("*")
    result_handles = main.query_selector_all(listings_selector)
    if not result_handles:
        print("no results ... but it should work")
        print("sleeping and trying again in 3 seconds")
        time.sleep(3)
        env.try_count += 1
        if env.try_count == 3:
            pprint("no results after trying 3 times")
            print(main.inner_text())
            return 
        else:
            return scrape_craigslist_jobs(page, url)

    data = []
    for pid in result_handles:
        result_handle = pid.query_selector(".result-info")
        store = {}
        meta = result_handle.query_selector(".meta")
        if meta:
            date = meta.query_selector("span:first-child")
            if date:
                store["date"] = date.get_attribute("title")
            separators = meta.query_selector_all("span.separator")
            for i, separator in enumerate(separators):
                s = separator.evaluate("element => element.nextSibling.textContent")
                if i == 0:
                    store["salary"] = parse_salary(s)
                else:
                    store["company"] = s

        a = result_handle.query_selector(".title-blob > a")
        if a:
            href = a.get_attribute("href")
            store["href"] = href 
            title_handle = a.query_selector("span.label")
            if title_handle:
                text = title_handle.inner_text()
                store["title"] = text
                regex = "\\b(?:3k|assistant|autistic|corporate|cheer|director|dance|esl|event|executive|french|finance|gymnastics|special education|spanish|social studies|toddler|japanese|driving|associate|music|youth worker|ymca|mentor|musician|aba para)\\b|kickboxing|special ed"
                if test(text, regex, flags = re.I):
                    continue
            data.append(store)


    return unique(map(data, lambda x: x.get("title")))

# playwright_runner(openai_example, openai_url) # this works


s = """
    my mom would do it the most efficient way possible
    with minimal effort

    efficiency and ... yeah
    the name of the school is everything
    the ability to please higher ups

    but i didnt want to please higher ups

"""

craigslist_url = "https://newyork.craigslist.org/search/edu#search=1~thumb~0~0"
typst_packages_url = "https://typst.app/docs/packages/"
typst_documentation_url = "https://typst.app/docs/reference/visualize/circle/"

def get_typst_docs(page):
    elements = page.query_selector_all('h3')
    for element in elements:
        print(element.inner_text())


# playwright_runner(get_typst_docs, typst_documentation_url)

typst_api_url = "https://typst.app/project/p8xwehdy-BZR-oSk-DPRxu"
typst_api_url = "https://typst.app/docs/reference/visualize/circle/"

def get_typst_code_content(page):
    # el = page.query_selector("*")
    # print(el.content)
    print(page.content())
    # write("/home/kdog3682/2024/.temp1.json", serialize_element(el))

# playwright_runner(get_typst_code_content, typst_api_url)

def serialize_element(element):

    properties = {
        'tag': element.eval_on_selector('tagName', 'el => el.tagName.toLowerCase()'),
        'attributes': element.get_attributes(),
        'text': element.text_content(),
        'id': element.get_attribute('id'),
        'class': element.get_attribute('class')
    }

    child_elements = element.query_selector_all(':scope > *')
    children = map(child_elements, serialize_element)
    if children:
        properties['children'] = children

    return properties
