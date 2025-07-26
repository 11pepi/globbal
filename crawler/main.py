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
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(system("which chromedriver"))  # fix this too

driver = webdriver.Chrome(service=service, options=options)

visitedpages = []

def build_selector(globs):
    selector = "a[href]"
    return selector

def crawl(url: str, depth: int):
    global visitedpages
    driver.get(url)
    try:
        selector = build_selector(visitedpages)
        e = driver.find_element(By.CSS_SELECTOR, selector)
        href = e.get_attribute("href")
        print(depth, href, visitedpages)
        if href in visitedpages:
            print(depth, "skipped")
            return
        else:
            print("doing thing")
            crawl(href, depth+1)
    except NoSuchElementException:
        print("no element")

    visitedpages.append(url)
    return

crawl("https://www.selenium.dev/documentation/webdriver/elements/", 0)