import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@dataclass
class ComposeEmail:
    email: str
    message: str
    count: int = 0


@activity.defn
async def send_email(details: ComposeEmail) -> str:
    print(
        f"Sending email to {details.email} with message: {details.message}, count: {details.count}"
    )
    return "success"


@workflow.defn
class SendEmailWorkflow:
    def __init__(self) -> None:
        self._email: str = "<no email>"
        self._message: str = "<no message>"
        self._subscribed: bool = True
        self._count: int = 0

    @workflow.run
    async def run(self, email, message):
        self._email = f"{email}"
        self._message = "Here's your message!"
        self._subscribed = True
        self._count = 0
        while self._subscribed is True:
            self._count += 1
            return await workflow.start_activity(
                send_email,
                ComposeEmail(self._email, self._message, self._count),
                start_to_close_timeout=timedelta(seconds=10),
            )
        else:
            return await workflow.start_activity(
                send_email,
                ComposeEmail(email, message, self._count),
                start_to_close_timeout=timedelta(seconds=10),
            )

    @workflow.signal
    def subscribe(self):
        self._count += 1
        self._subscribed = True

    @workflow.signal
    def unsubscribe(self):
        self._message = "You have unsubscribed from our mailing list."
        self._subscribed = False

    @workflow.query
    def greeting(self) -> str:
        return self._email

    @workflow.query
    def message(self) -> str:
        return self._message

    @workflow.query
    def count(self) -> int:
        return self._count


async def main():
    client = await Client.connect("localhost:7233")

    # run worker here
    worker = Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[SendEmailWorkflow],
        activities=[send_email],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
