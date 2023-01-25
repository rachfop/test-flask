from flask import Flask, jsonify, request
from temporalio.client import Client

from run_worker import SendEmailWorkflow

app = Flask(__name__)


@app.route("/subscribe/", methods=["POST"])
async def start_subscription() -> str:
    client = await Client.connect("localhost:7233")
    await client.start_workflow(
        SendEmailWorkflow.run,
        args=(request.form["email"], request.form["message"]),
        id="send-email-activity",
        task_queue="hello-activity-task-queue",
    )
    handle = client.get_workflow_handle(
        "send-email-activity",
    )

    emails_sent = await handle.query(SendEmailWorkflow.count)
    return jsonify({"status": "success", "emails_sent": emails_sent})


@app.route("/unsubscribe/", methods=["POST"])
async def end_subscription():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(
        "send-email-activity",
    )
    await handle.signal(SendEmailWorkflow.unsubscribe)
    return jsonify({"status": "end"})


@app.route("/query/", methods=["POST"])
async def query():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(
        "send-email-activity",
    )
    greeting = await handle.query(SendEmailWorkflow.greeting)
    message = await handle.query(SendEmailWorkflow.message)
    return jsonify({"status": "query", "greeting": greeting, "message": message})


app.run(debug=True)
