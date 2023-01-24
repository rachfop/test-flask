from flask import Flask, jsonify, request
from temporalio.client import Client

from run_worker import SendEmailWorkflow

app = Flask(__name__)


@app.route("/subscribe/", methods=["POST"])
async def start_subscription() -> str:
    client = await Client.connect("localhost:7233")
    result = await client.start_workflow(
        SendEmailWorkflow.run,
        args=(request.form["email"], request.form["message"]),
        id=str(request.form["email"]),
        task_queue="hello-activity-task-queue",
    )

    return jsonify({"status": "success", "result": result})


@app.route("/unsubscribe/", methods=["POST"])
async def end_subscription():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(
        "send-email-activity",
    )
    await handle.cancel()
    return jsonify({"status": "end"})


app.run(debug=True)
