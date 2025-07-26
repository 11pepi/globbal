from flask import Flask, render_template

rawfile = open("links.txt")
links = []
for i in rawfile.readlines():
  j = i.split("=")
  k = j[0].split()
  links.append([k, j[1], j[0]])
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
        if i[1] not in results:
          results.append(f"<a href='{i[1]}'>{i[2]}</a>")
  return render_template(
    "searchtemplate.html",
    resultnum=len(results),
    query=text,
    results="<br />".join(results)
  )


app.run(host='0.0.0.0', port=8080)