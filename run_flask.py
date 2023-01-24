import asyncio

from flask import Flask, jsonify, request
from temporalio.client import Client

from run_worker import SendEmailWorkflow

app = Flask(__name__)


@app.route("/subscribe/", methods=["POST"])
async def start_subscriber() -> str:
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        SendEmailWorkflow.run,
        args=(request.form["email"], request.form["message"]),
        id="send-email-activity",
        task_queue="hello-activity-task-queue",
    )

    return jsonify({"status": "success", "result": result})


@app.route("/get_details/", methods=["GET"])
async def get_subscriber(email):
    pass


app.run(debug=True)
