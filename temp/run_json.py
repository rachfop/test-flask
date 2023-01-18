import asyncio
import json
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class Subscription:
    subscribed: bool
    count: int
    email: str


subscription = Subscription(False, 0, "")


@activity.defn
async def home():
    return json.dumps(subscription.__dict__)


@activity.defn
async def subscribe(email: str, subscribe: bool):
    # Checking if the value of `subscribe` is `True`.
    if subscribe:
        subscription.subscribed = True
        subscription.count += 1
        subscription.email = email
    # Checking if the value of `subscribe` is `False`.
    elif not subscribe:
        subscription.subscribed = False
        subscription.email = ""
    return json.dumps(subscription.__dict__)


@activity.defn
async def handle_request(request_data: str):
    request_data = json.loads(request_data)
    email = request_data.get("email")
    subscribe = request_data.get("subscribe")
    if email and subscribe is not None:
        return await subscribe(email, subscribe)
    else:
        return await home()
    """ if email and subscribe is not None:
            return await activity(subscribe, email, subscribe)
        else:
            return await activity.execute(home)"""


@workflow.defn
class ProcessRequest:
    @workflow.run
    async def run(self, request_data: str):
        return await workflow.execute_activity(
            handle_request, request_data, start_to_close_timeout=timedelta(seconds=10)
        )


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[ProcessRequest],
        activities=[home, subscribe, handle_request],
    )
    print(f"Worker started on task queue: {worker.task_queue}")
    print(f"subscription.subscribed: {subscription.subscribed}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
