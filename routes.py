from flask import Flask, url_for, render_template, request, session, redirect
from flask.helpers import send_from_directory

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=["POST", "GET"])
def hello(name=None):

    if request.method == "POST":
        session["name"] = request.form["sname"]

        return redirect("/results")
    else:
        return render_template("homepage.html")


@app.route("/results")
def results():
    if "name" in session:
        return render_template("template.html", name=session["name"])
    else:
        return redirect("/")
