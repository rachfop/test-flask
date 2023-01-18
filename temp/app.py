import asyncio
import json

from flask import Flask, render_template, request
from run_json import ProcessRequest, Subscription
from temporalio.client import Client

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
async def index():
    client = await Client.connect("localhost:7233")

    if request.method == "POST":
        email = request.form["email"]
        subscribe = request.form["subscribe"]

        subscription_data = await client.execute_workflow(
            ProcessRequest.run,
            email,
            id="my-workflow-id",
            task_queue="my-task-queue",
        )
        return render_template("home.html"), subscription_data
    else:

        subscription_data = await client.execute_workflow(
            ProcessRequest.run,
            json.dumps({}),
            id="my-workflow-id",
            task_queue="my-task-queue",
        )
        return render_template("home.html"), subscription_data


if __name__ == "__main__":
    asyncio.run(index())
    app.run(debug=True)
