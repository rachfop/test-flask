import asyncio

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

# --------------
# Helper Classes
# --------------


class Subscription:
    def __init__(
        self,
        email: str,
        is_subscribe: bool,
        num_of_emails_sent: int,
        frequency: float = 3,
    ):
        self.email = email
        self.is_subscribe = is_subscribe
        self.num_of_emails_sent = num_of_emails_sent
        self.frequency = frequency


DEFAULT_FREQUENCY_IN_MIL_SEC = 1

# ------
# Routes
# ------


async def send_email(email: str, message: str) -> None:
    print(f"Sending email to {email} with the following message: \n{message}.")


@app.route("/", methods=["GET", "POST"])
async def get_subscriber():
    if request.method == "POST":
        try:
            email = request.form["email"]
            is_subscribe = True
            # check for valid email address
            if not is_valid_email(email):
                flash("Invalid Email, Please enter valid email address")
                return redirect(url_for("get_subscriber"))
            else:
                subscription = Subscription(
                    email, is_subscribe, 0, DEFAULT_FREQUENCY_IN_MIL_SEC
                )
                await send_email(subscription.email, "Thank you for subscribing!")
                while subscription.is_subscribe:
                    await asyncio.sleep(subscription.frequency)

                    if subscription.is_subscribe:
                        subscription.num_of_emails_sent += 1
                        await send_email(
                            subscription.email,
                            f"Frequency Email: {subscription.num_of_emails_sent}!",
                        )

                flash("You are unsubscribed from our service")
                return redirect(url_for("unsubscribe"))

        except Exception as e:
            flash(f"Error: {e}")

    return render_template("home.html")


def is_valid_email(email: str) -> bool:
    import re

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


if __name__ == "__main__":
    app.run(debug=True)
