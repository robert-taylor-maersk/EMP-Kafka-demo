#!/usr/bin/env python

from flask import Flask, render_template, Response
from confluent_kafka import Consumer, TopicPartition
import json
from random import randint
import time


def get_kafka_client():
    return KafkaClient(hosts="127.0.0.1:9092")


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# Consumer API
@app.route("/map/live")
def get_messages():

    # consumer = Consumer(
    #     {
    #         "bootstrap.servers": "localhost:9092",
    #         "group.id": "my_group",
    #         "auto.offset.reset": "earliest",
    #     }
    # )

    # basic_consume_loop(consumer, [TopicPartition(topic="numbers", partition=0, offset=0)], 10)

    def events():
        ships = [
            {"vessel": "00001", "latitude": 51.95804608632545, "longitude": 2.0394680674709065},
            {"vessel": "00002", "latitude": 52.25804608632545, "longitude": 2.0394680674709065},
            {"vessel": "00003", "latitude": 52.29804608632545, "longitude": 2.0394680674709065},
        ]
        while True:
            s = 0
            tracker = [dict(s) for s in ships]
            for _ in range(0, 60):
                s = 0 if s >= len(tracker) - 1 else s + 1
                data = tracker[s]
                data["latitude"] += randint(0, 200) / 1000
                data["longitude"] += randint(0, 200) / 1000
                time.sleep(randint(5, 15) / 10)
                yield "data: {}\n\n".format(json.dumps(data))

    #        for i in client.topics[topicname].get_simple_consumer():
    #            yield "data:{0}\n\n".format(i.value.decode())

    return Response(events(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
