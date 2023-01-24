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


@activity.defn
async def send_email(details: ComposeEmail) -> str:
    print(f"Sending email to {details.email} with message: {details.message}")
    return "success"


@workflow.defn
class SendEmailWorkflow:
    @workflow.run
    async def run(self, email, message):

        return await workflow.start_activity(
            send_email,
            ComposeEmail(email, message),
            start_to_close_timeout=timedelta(seconds=10),
        )


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
