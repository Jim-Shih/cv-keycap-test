from rmq_connector import rmq_connector
from rmq_utils import load_config

if __name__ == "__main__":
    config = load_config()
    with rmq_connector(config["queue_name"]) as consumer:
        consumer.consume(consumer.callback)
