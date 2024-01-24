import pika
from utils import get_message_size, restricted_message_size


class rmq_connection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def __init__(self, queue_name) -> None:
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def publish(self, message):
        message_size = get_message_size(message)
        if not restricted_message_size(message_size):
            print("Message size is too large")
            raise Exception("Message size is too large")

        message = message + " size" + str(message_size)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(),
        )
        print(" [x] Sent %r" % message.replace("a", ""))

    def consume(self, callback):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        print("Received message:", body.decode()[-10:])
