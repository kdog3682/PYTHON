from utils import *
from playwright.sync_api import sync_playwright

def get_href_links_from_url(page, url):
    elements = page.query_selector_all('a')

    links = []
    for element in elements:
        href = element.get_attribute('href')
        if href:
            links.append(href)

    links = unique(links)
    return links


def craiglist_job_scraper(page):

    url = "https://newyork.craigslist.org/search/edu#search=1~thumb~0~0"
    page.goto(url)
    li_elements = page.query_selector_all("li[data-pid]")
    results = []
    for li in li_elements:
        title = li.get_attribute("title")
        if not title:
            continue

        child = li.query_selector("div > a")
        if child:
            href = x.get_attribute("href") if child else None
            if href:
                results.append({"title": title, "url": href})
    return results


def playwright_runner(fn, *args, **kwargs):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        value = fn(page, *args)
        browser.close()
        return value


def find_child_element(element, checkpoint):
    for child in element.query_selector_all('*'):
        if bool(checkpoint(child)):
            return child
        else:
            result = find_child_element(child, checkpoint)
            if result:
                return result

# url = "https://typst.app/docs/packages/"
# playwright_runner(get_href_links_from_url, url)
c2(playwright_runner(craiglist_job_scraper))
