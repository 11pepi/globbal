from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import subprocess
from concurrent.futures import ThreadPoolExecutor

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

visitedpages = open("crawler/blocklist.txt").readlines()

def build_selector(globs):
    selector = "a[href]"
    return selector

def crawl(url: str, id: int, depth: int=0):
    global visitedpages

    if url in visitedpages:
        print(depth, "skipped", url)
        return

    visitedpages.append(url)
    print(id, depth, "visiting", url)
    driver.get(url)

    try:
        selector = build_selector(visitedpages)
        e = driver.find_elements(By.CSS_SELECTOR, selector)
        for i in e:
            href = i.get_attribute("href")
            if href and href not in visitedpages:
                crawl(href, id+1, depth+1)
    except Exception as e:
        print(e)
        exit()

with ThreadPoolExecutor(max_workers=2) as executor:
    future = executor.submit(crawl, "https://getpocket.com", 1)
