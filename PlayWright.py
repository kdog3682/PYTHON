# Installing PlayWright
# pip list
# pip show playwright
# @vim: pip playwright
# python3 -m playwright install

from playwright.sync_api import sync_playwright

def abc():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://example.com')
        print(page.title())
        browser.close()


import asyncio
from playwright.async_api import async_playwright

async def main(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.pdf(path='/home/kdog3682/2024/output.pdf')
        await browser.close()

# the key is that you must first run vite so that localhost is up.
# only then can playwright access the url
# url = "http://localhost:5173/vuetify.html"
# asyncio.run(main(url))

