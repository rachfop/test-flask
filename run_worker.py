# run_worker.py
import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

with workflow.unsafe.imports_passed_through():
    from flask import Flask, flash, redirect, render_template, request, url_for

# --------------
# Helper Classes
# --------------


class Subscription:
    def __init__(
        self,
        email: str,
        is_subscribe: bool,
        num_of_emails_sent: int,
        frequency: float = 3,
    ):
        self.email = email
        self.is_subscribe = is_subscribe
        self.num_of_emails_sent = num_of_emails_sent
        self.frequency = frequency


DEFAULT_FREQUENCY_IN_MIL_SEC = 1


@activity.defn
async def handle_subscription(email: str, message: str) -> None:
    print(f"Sending email to {email} with the following message: \n{message}.")


@workflow.defn
class SubscriptionWorkflow:
    @workflow.run
    async def run(self, subscription: Subscription) -> None:
        num_emails_sent = 0

        # handle query for num of emails sent

        # while loop to send emails
        if request.method == "POST":
            subscription = Subscription(
                request.form["email"], True, 0, DEFAULT_FREQUENCY_IN_MIL_SEC
            )
            await handle_subscription(subscription.email, "Thank you for subscribing!")

            while subscription.is_subscribe:
                await asyncio.sleep(subscription.frequency)

                if subscription.is_subscribe:
                    subscription.num_of_emails_sent += 1
                    await handle_subscription(
                        subscription.email,
                        f"Frequency Email: {subscription.num_of_emails_sent}!",
                    )

        return await workflow.execute_activity(
            handle_subscription,
            subscription,
            start_to_close_timeout=timedelta(seconds=10),
        )

    # handle


async def main():
    client = Client("localhost:7233")
    async with Worker(
        client,
        task_queue="subscription-task-queue",
        workflows=[SubscriptionWorkflow],
        activities=[handle_subscription],
    ):
        # Execute the workflow
        await client.execute_workflow(
            SubscriptionWorkflow.run,
            Subscription,
            id=Subscription.email,
            task_queue="subscription-task-queue",
        )


if __name__ == "__main__":
    asyncio.run(main())
