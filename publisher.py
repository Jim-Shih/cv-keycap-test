import os
import time
import numpy as np
from rmq_connection import rmq_connection
from dotenv import load_dotenv


def load_config():
    load_dotenv()
    config = {
        "queue_name": os.getenv("QUEUE_NAME"),
        "message_duration": float(os.getenv("SEND_MESSAGE_DURATION")),
        "message_deviation": float(os.getenv("SEND_MESSAGE_DEVIATION")),
        "max_message_size": int(os.getenv("MAX_MESSAGE_SIZE")),
        "min_message_size": int(os.getenv("MIN_MESSAGE_SIZE")),
    }
    return config


def generate_and_publish_message(publisher, config):
    sleep_time = (
        np.random.beta(1, 1) * config["message_deviation"] + config["message_duration"]
    )
    size_of_message = np.random.randint(
        config["min_message_size"], config["max_message_size"]
    )
    message = "a" * size_of_message
    publisher.publish(message + " " + str(sleep_time))
    time.sleep(sleep_time)


def main():
    config = load_config()
    with rmq_connection(config["queue_name"]) as publisher:
        while True:
            generate_and_publish_message(publisher, config)


if __name__ == "__main__":
    main()
