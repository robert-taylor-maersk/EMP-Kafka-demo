#!/usr/bin/env python

from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

import os
import yaml


def main():

    sr_config = {
        "url": "https://psrc-4kk0p.westeurope.azure.confluent.cloud",
        "basic.auth.user.info": "{}:{}".format(
            os.environ.get("PROD_SR_KEY"),
            os.environ.get("PROD_SR_SECRET"),
        ),
    }

    kafka_config = {
        "schema.registry.url": "https://{}:{}@psrc-4kk0p.westeurope.azure.confluent.cloud".format(
            "VLG4W7M6LYENMBFS", "Ez4%2Fz6q2VL08oghVXtyzpJIx88r17q95zxMnW1k1Vwd6eI8P0XGy%2Bqsv7kvVgVvj"
        ),
        "bootstrap.servers": "pkc-lq8gm.westeurope.azure.confluent.cloud:9092",
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": "{}".format(os.environ.get("PROD_CCLOUD_KEY")),
        "sasl.password": "{}".format(os.environ.get("PROD_CCLOUD_SECRET")),
        "session.timeout.ms": 45000,
        "group.id": "EMP-Kafka-map-demo",
        "auto.offset.reset": "earliest",
    }

    # Subscribe to topic
    consumer = AvroConsumer(kafka_config)
    consumer.subscribe(["MSK.arrivalIntelligence.marineTrafficAisReading.topic.internal.any.v1"])

    # Process messages
    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            elif msg.error():
                print("error: {}".format(msg.error()))
                continue

            # process message
            msg_key = msg.key()
            msg_data = msg.value()
            print(msg_key)

        except SerializerError as e:
            print(f"Avro message deserialization failed: {e} on topic ")

    consumer.close()


if __name__ == "__main__":
    main()
