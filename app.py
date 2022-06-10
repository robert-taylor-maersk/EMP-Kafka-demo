#!/usr/bin/env python

import json
import os
import time

from confluent_kafka import Consumer
from flask import Flask, Response, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def events(c):
    while True:
        msg = c.poll(5.0)
        if msg is None:
            continue
        if msg.error():
            continue

        data = json.loads(msg.value().decode("utf-8"))
        if data.get("TYPE_NAME") == "Container Ship":
            time.sleep(0.1)
            yield "data: {}\n\n".format(msg.value().decode("utf-8"))


@app.route("/map/live")
def get_messages():

    c = Consumer(
        {
            "bootstrap.servers": "pkc-lq8gm.westeurope.azure.confluent.cloud:9092",
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": "{}".format(os.environ.get("PROD_CCLOUD_KEY")),
            "sasl.password": "{}".format(os.environ.get("PROD_CCLOUD_SECRET")),
            "session.timeout.ms": 45000,
            "group.id": "EMP-Kafka-map-demo",
            "auto.offset.reset": "latest",
        }
    )

    c.subscribe(["MSK.arrivalIntelligence.marineTrafficAisReading.topic.internal.any.v1"])
    return Response(events(c), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=False, port=5001)
