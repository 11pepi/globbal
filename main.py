from flask import Flask

rawfile = open("links.txt")
links = []
for i in rawfile.readlines():
  j = i.split("=")
  k = j[0].split()
  links.append([k, j[1]])
print(links)

app = Flask('app')

@app.route('/')
def hello_world():
  return "use the url bar"

@app.route("/<text>")
def search(text):
  query = text.split()
  results = []
  for i in links:
    for j in query:
      if j in i[0]:
        if j not in results:
          results += i[1]
  return results

app.run(host='0.0.0.0', port=8080)

"""
[
  [
    ['qwatys', 'space'],
    'https://www.qwatys.space/\n'
  ],
  [
    ['cool', 'math', 'equasions'],
    'https://www.coolmathequasions.com/'
  ]
]
"""