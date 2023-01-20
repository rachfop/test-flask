import asyncio

from flask import Flask
from temporalio.client import Client

from run_worker import Subscription, SubscriptionWorkflow

app = Flask(__name__)

# TEMPORARY - Set the secret key to a temporary value!
app.secret_key = "BAD_SECRET_KEY"

# Log that the Flask application is starting
app.logger.info("Starting the Flask App...")

client = Client("localhost:7233")

# ------
# Routes
# ------


@app.route("/subscribe/", methods=["POST"])
async def start_subscriber():

    await client.execute_workflow(
        SubscriptionWorkflow.run,
        Subscription,
        id="subscription-workflow-id",
        task_queue="subscription-task-queue",
    )


app.route("/get_details/", methods=["GET"])


async def get_subscriber(email):
    # client.query(wf-id, )
    # how to define a query
    # get the state of thw query
    # how many emails have been sent
    pass


def is_valid_email(email: str) -> bool:
    import re

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


if __name__ == "__main__":
    app.run(debug=True)
