#!/usr/bin/env python

from flask import Flask, render_template, Response
from confluent_kafka import Consumer
import os
import time
import json


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# Consumer API
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

    def events():
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                continue

            data = json.loads(msg.value().decode("utf-8"))
            if data.get("TYPE_NAME") == "Container Ship":
                time.sleep(0.1)
                yield "data: {}\n\n".format(msg.value().decode("utf-8"))

    return Response(events(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=False, port=5001)
