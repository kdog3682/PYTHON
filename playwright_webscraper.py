import base as assda
from utils import *
from playwright.sync_api import sync_playwright

def playwright_runner(fn, *args, **kwargs):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
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


def get_typst_packages(page, url = None):
    if not url: 
        url = "https://typst.app/docs/packages/"

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

def scrape_craigslist_jobs(page, url = None):
    if not url: url = "https://newyork.craigslist.org/search/edu#search=1~thumb~0~0"
    page.goto(url)
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
            data.append(store)

    return data
