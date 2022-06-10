#!python

from confluent_kafka import Consumer
import os
import time
import json


def main():
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

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue

        print("{},".format(msg.value().decode("utf-8")))
        time.sleep(0.5)

    c.close()


if __name__ == "__main__":
    main()
