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

forbidden = set()
with open("crawler/words.txt") as f:
    forbidden = set(f.read().splitlines())

print(forbidden)

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

visitedhrefs = list(open("blocklist.txt").readlines())
evaluations = {}

def get_metas(drvr: webdriver.Chrome):
    description_e = drvr.find_element(By.CSS_SELECTOR, "meta[name='description']")
    description = description_e.get_attribute("content")
    if not description:
        description = "I'd love to show you a description, but there's literally nothing here"

    if "kuro" in description.lower():
        description = "OMG PROJECT KURO REFERENCE"

    return description

def count_phrases(words: list[str], n: int, num_phrases: int, forbidden: set):
    phrases = []
    phrase_words = []

    for i in range(len(words) - n + 1, num_phrases * n + 1, n):
        phrase = words[i:i + n]

        # Skip if any forbidden word is in the phrase
        if any(f in forbidden for f in phrase):
            continue

        joined = " ".join(phrase)
        phrases.append(joined)
        phrase_words.append(phrase)

    phrase_counts = Counter(phrases)
    return phrases, phrase_words, phrase_counts

def count_words(text):
    words = re.findall(r"\b[a-z]{3,}\b", text)
    words = [word for word in words if word not in forbidden]

    word_counts = Counter(words)
    return words, word_counts

def evaluate_page(href):
    text = driver.find_element(By.TAG_NAME, "body").text.lower()

    _, word_counts = count_words(text)

    top_words = word_counts.most_common(5)
    #top_phrases = phrase_counts.most_common(num_phrases)

    description = get_metas(driver)

    evaluations[href] = {
        "url": href,
        "title": f"{driver.title}: {description},
        "keywords": top_words
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

from . import funnyevals
evaluations = funnyevals.evals

print(f"results")
print(f"==========================")
print(f"visited: {visitedhrefs}   ")
print(f"\n\n\nevaluations: {evaluations}")

def get_keywords_dict(e):
    keywords = e.get("keywords")
    keywords = {k: v for k, v in keywords}
    return keywords

@db.db_transaction
def save(session = None):
    for url, e in evaluations.items():
        url_obj = model.URLs(
            url = url,
            title = e.get("title")
        )
        session.add(url_obj)

        keywords = get_keywords_dict(e)
        for keyword, weight in keywords.items():
            keyword_obj = model.Keywords(
                word = keyword,
                weight = int(weight),
                url = url_obj
            )
            session.add(keyword_obj)

driver.quit()
save()