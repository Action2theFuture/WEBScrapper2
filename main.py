from flask import Flask, render_template, request, redirect, send_file
from Scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route("/")  #@: decorate 바로 아래에 있는 함수를 찾는다
def home():
    return render_template("fuck.html")


@app.route("/<username>")  # dynamic url
def contact(username):
    return f"Helloooo {username} how are you doing"


@app.route("/report")
def report():
    word = request.args.get('mouse')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html",
        SearchingBy=word,
        ResultsNumber=len(jobs),
        jobs = jobs,
        tomato="muscle")  #rendering html에 있는 {{}}에 변수를 보여준다
                          #rendering html에 있는 {%%}에 코드를 실행한다

@app.route("/export")
def export():
  try:
    word = request.args.get('mouse')
    if not word:
      raise Exception()
      #Exception == error
    word = word.lower()
    jobs = db.get(word) 
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")
  # try를 실행하다 error가 나면 except를 실행
    

app.run(host="0.0.0.0")
