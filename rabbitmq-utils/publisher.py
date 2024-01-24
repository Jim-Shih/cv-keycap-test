from rmq_connector import rmq_connector
from rmq_utils import generate_and_publish_message, load_config

if __name__ == "__main__":
    config = load_config()
    with rmq_connector(config["queue_name"]) as publisher:
        while True:
            generate_and_publish_message(publisher, config)
