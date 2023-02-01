from dependency_injector.wiring import Provide, inject
from flask import Flask, jsonify, request
from temporalio.client import Client

from run_worker import SendEmailWorkflow

app = Flask(__name__)


@app.before_first_request
async def startup():
    global client
    client = await Client.connect("localhost:7233")


@app.route("/subscribe/", methods=["POST"])
async def start_subscription() -> str:

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
    email = await handle.query(SendEmailWorkflow.greeting)
    return jsonify({"status": "success", "email": email, "emails_sent": emails_sent})


@app.route("/query/", methods=["POST"])
async def get_query():
    handle = client.get_workflow_handle(
        "send-email-activity",
    )
    greeting = await handle.query(SendEmailWorkflow.greeting)
    message = await handle.query(SendEmailWorkflow.message)
    count = await handle.query(SendEmailWorkflow.count)
    return jsonify(
        {"status": "query", "greeting": greeting, "message": message, "count": count}
    )


@app.route("/unsubscribe/", methods=["POST"])
async def end_subscription():
    handle = client.get_workflow_handle(
        "send-email-activity",
    )
    await handle.cancel()
    return jsonify({"status": "end"})


if __name__ == "__main__":
    app.run(debug=True)
