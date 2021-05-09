from flask import Flask, url_for, render_template, request, session, redirect
from flask.helpers import send_from_directory

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/request", methods=["POST", "GET"])
def hello(name=None):

    if request.method == "POST":
        session["name"] = request.form["sname"]

        return redirect("/results")
    else:
        return render_template("request.html")


@app.route("/results")
def results():
    if "name" in session:
        return render_template(
            "results.html",
            name=session["name"],
            result="Invest",
            trials="2430",
            confidence="97",
        )
    else:
        return redirect("/")


@app.route("/googlehome/")
def say():
    text = request.args.get("text")
    return redirect(
        "https://www.arielwolle.com:9191/say/?text=" + text + " is a good investment"
    )


if __name__ == "__main__":
    app.run(debug=True)
