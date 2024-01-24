from rmq_connection import rmq_connection
from dotenv import load_dotenv
import os

load_dotenv()
queue_name = os.getenv("QUEUE_NAME")


if __name__ == "__main__":
    with rmq_connection(queue_name) as consumer:
        consumer.consume(consumer.callback)
