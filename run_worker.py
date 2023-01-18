# run_worker.py
import asyncio
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

with workflow.unsafe.imports_passed_through():
    from flask import Flask, flash, redirect, render_template, request, url_for
from app import Subscription, app, subscription_list


# Define a Temporal activity to handle the form submission
@activity.defn
async def handle_subscription(subscription: Subscription):
    subscription_list.append(subscription)
    return redirect(url_for("list_subscribers"))


# Define a Temporal Workflow to execute the activity
@workflow.defn
class SubscriptionWorkflow:
    @workflow.run
    async def run(self, subscription: Subscription) -> None:
        return await workflow.execute_activity(
            handle_subscription,
            subscription,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    client = await Client.connect("localhost:7233")
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
            id="subscription-workflow-id",
            task_queue="subscription-task-queue",
        )


if __name__ == "__main__":
    asyncio.run(main())

