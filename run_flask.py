from typing import Any, Dict

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
    emails_sent: int = await handle.query(SendEmailWorkflow.count)
    email: str = await handle.query(SendEmailWorkflow.greeting)

    return jsonify({"status": "ok", "email": email, "emails_sent": emails_sent})


@app.route("/get-details/", methods=["POST"])
async def get_query() -> Dict[str, Any]:
    handle = client.get_workflow_handle(
        "send-email-activity",
    )
    count: int = await handle.query(SendEmailWorkflow.count)
    greeting: str = await handle.query(SendEmailWorkflow.greeting)
    message: str = await handle.query(SendEmailWorkflow.message)

    return jsonify(
        {
            "status": "ok",
            "numberOfEmailsSent": count,
            "email": greeting,
            "message": message,
        }
    )


@app.route("/unsubscribe/", methods=["POST"])
async def end_subscription():
    handle = client.get_workflow_handle(
        "send-email-activity",
    )
    await handle.cancel()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
