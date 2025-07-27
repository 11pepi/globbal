from os import name
from flask import Flask, render_template, request
import db
from sqlalchemy import desc, func
from model import URLs, Keywords
from random import choice

db.create_all_tables()

app = Flask('app')

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/search")
def search():
    json = sql_query(request.args.get("q"))
    results = [f"<a href='{i.get('url')}'>{i.get('title')}</a>" for i in json]
    return render_template(
        "searchtemplate.html",
        resultnum=len(results),
        query=request.args.get("q"),
        results="<br />".join(results)
    )

"""@app.route("/jsonstuff/<text>")
def json_query(text):
    KEYWORDS = text.split()
    weights = []
    for link in LINKS:
        weight = 0
        print(link)
        for k, v in link.get("keywords").items():
            print(v)
            if k in KEYWORDS:
                weight += v.get("weight")

        weights.append(weight)

        print("keywords are", KEYWORDS)
        print("weights is", weights)
    try:
        x = [v for k, v in sorted(zip(weights, LINKS), reverse=True) if k != 0]
        print(x)
        return x
    except TypeError as e:
        print(e)
        return []"""

@app.route("/query/<text>")
@db.db_transaction
def sql_query(text: str = None, session = None):
    query_words = text.split()
    print(query_words)
    results = session.query(URLs, func.sum(Keywords.weight).label("total_weight")) \
        .join(Keywords, URLs.id == Keywords.url_id) \
        .filter(Keywords.word.in_(query_words)) \
        .group_by(URLs.id) \
        .order_by(desc("total_weight")) \
        .all()

    print("results arrr", results)
    json = []
    for url, total_weight in results:
        print("yurl is", url, "score:", total_weight)
        json.append({
            "id": url.id,
            "url": url.url,
            "title": url.title,
            "score": total_weight
        })
    return json

app.run(host='0.0.0.0', port=8080)

'''
- go through each item in list
- count how many keywords appear in our search vs that list
- create a list (list comprehension) for that
- sort by that new list

- get a URL
  - get the common ones between URL.keywords and your query
  - sort by URL.keywords.weight
'''
