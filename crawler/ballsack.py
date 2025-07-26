from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import subprocess
from random import choice

def system(cmd):
    stdout = subprocess.run(cmd, shell=True, capture_output=True).stdout.decode().strip()
    print(stdout)
    return stdout

options = Options()
options.binary_location = system("which chromium")
options.add_argument("--headless=new")  # or just --headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(system("which chromedriver"))  # fix this too

driver = webdriver.Chrome(service=service, options=options)

visitedpages = set()

def build_selector(globs):
    # Just return all links with href, can be refined later
    return "a[href]"

def crawl(url: str, depth: int):
    if url in visitedpages:
        print(depth, "skipped", url)
        return

    print(depth, "visiting", url)
    visitedpages.add(url)  # Mark visited ASAP
    driver.get(url)

    try:
        selector = build_selector(visitedpages)
        elements = driver.find_elements(By.CSS_SELECTOR, selector)  # get all links

        for e in elements:
            href = e.get_attribute("href")
            if href and href not in visitedpages:
                crawl(href, depth+1)

    except NoSuchElementException:
        print("no element")

# Start crawling
crawl("https://google.com", 0)