import asyncio
import time

from flask import Flask, render_template, request

app = Flask(__name__)
subscribed = False
count = 0
email = ""


@app.route("/")
def home():
    return render_template("home.html", subscribed=subscribed, count=count, email=email)


@app.route("/", methods=["POST"])
def subscribe():
    global subscribed
    global count
    global email

    if request.form.get("subscribe"):
        subscribed = True
        count += 1
        email = request.form.get("email")
    elif request.form.get("unsubscribe"):
        subscribed = False
        email = ""

    return render_template("home.html", subscribed=subscribed, count=count, email=email)


if __name__ == "__main__":
    app.run(debug=True)
