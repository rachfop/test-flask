import asyncio
import json
from dataclasses import dataclass
from datetime import timedelta

from flask import Flask, flash, render_template, request
from pydantic import BaseModel, ValidationError, validator
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

app = Flask(__name__)


@dataclass
class Subscription:
    subscribed: bool
    count: int
    email: str

    @validator("Subscription")
    def subscription_check(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError("Stock symbol must be 1-5 characters")
        return value.upper()


subscription = Subscription(False, 0, "")


@app.route("/", methods=["GET", "POST"])
def subscribe():
    if request.method == "POST":
        # Print the form data to the console
        for key, value in request.form.items():
            print(f"{key}: {value}")

        try:
            subscribed_data = Subscription(subscribed=True, count=3, email="hello")
            print(subscribed_data)
        except ValidationError as e:
            print(e)

        return render_template("home.html")
    return render_template("home.html")
