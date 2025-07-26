from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import subprocess
from collections import Counter
from random import choice
import re
import db
import model

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

def build_selector(globs):
    selector = "a[href]"
    return selector

visitedhrefs = []
evaluations = {}

def evaluate_page(href):
    text = driver.find_element(By.TAG_NAME, "body").text.lower()
    words = re.findall(r"\b[a-z]{2,}\b", text)

    word_counts = Counter(words)
    n = 4  # phrase length
    forbidden = set(["the", "and", "to", "or", "of", "by", "we", "with", "on"])

    phrases = []
    phrase_words = []

    for i in range(len(words) - n + 1):
        phrase = words[i:i + n]

        # Skip if any forbidden word is in the phrase
        if any(f in forbidden for f in phrase):
            continue

        joined = " ".join(phrase)
        phrases.append(joined)
        phrase_words.append(phrase)

    phrase_counts = Counter(phrases)

    top_words = word_counts.most_common(10)
    top_phrases = phrase_counts.most_common(10)

    combined = []
    combined.extend(top_phrases)
    combined.extend(top_words)
    combined.extend(phrase_words)

    evaluations[href] = {
        "url": href,
        "title": driver.title,
        "keywords": combined
    }

def do_crawl(url: str, depth: int = 0):
    global visitedhrefs
    if url in visitedhrefs:
        print(depth, "skipped", url)
        return

    print(depth, "crawl", url)
    driver.get(url)
    visitedhrefs.append(url)

    try:
        selector = build_selector(visitedhrefs)
        e = driver.find_elements(By.CSS_SELECTOR, selector)
        for i in e:
            href = i.get_attribute("href")
            evaluate_page(href)
            if href and href not in visitedhrefs:
                do_crawl(href, depth+1)

    except Exception as err:
        print(depth, "error", err)
        return

#do_crawl("https://getpocket.com/home")

import funnyevals
evaluations = funnyevals.evals

print(f"results")
print(f"==========================")
print(f"visited: {visitedhrefs}   ")
print(f"\n\n\nevaluations: {evaluations}")

@db.db_transaction
def save(session = None):
    for _, e in evaluations.items():
        keywords = e.get("keywords")
        keywords = {k: v for k, v in keywords}
        print(keywords)

save()