from flask import (
    Flask,
    escape,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask.logging import default_handler

app = Flask(__name__)

# TEMPORARY - Set the secret key to a temporary value!
app.secret_key = "BAD_SECRET_KEY"


# Log that the Flask application is starting
app.logger.info("Starting the Flask App...")

from dataclasses import dataclass

# --------------
# Helper Classes
# --------------


@dataclass
class Subscription:
    status: bool
    count: int
    email: str


# ------
# Routes
# ------

subscription_list = []


@app.route("/", methods=["GET", "POST"])
async def get_subscriber():
    if request.method == "POST":
        # Print the form data to the console
        for key, value in request.form.items():
            print(f"{key}: {value}")

            subscription_data = Subscription(
                email=request.form["email"], count=1, status=True
            )
            print(subscription_data)
            # Save the form data to the session object
            subscription_list.append(subscription_data)
            flash(f"Added new email ({subscription_data.email})!", "success")
            app.logger.info(f"Added new email ({request.form['email']})!")

            return redirect(url_for("list_subscribers"))

    return render_template("home.html")


@app.route("/subscribers/")
async def list_subscribers():
    # Retrieve the form data from the session object
    return render_template("list_subscribers.html", subscribers=subscription_list)


@app.route("/users/")
async def list_users():
    return render_template("list_users.html", subscribers=subscription_list)
