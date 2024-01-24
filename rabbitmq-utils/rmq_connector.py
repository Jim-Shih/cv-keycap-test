import pika
from rmq_utils import get_message_size


class rmq_connector:
    """
    This class represents a RabbitMQ connection.

    Attributes:
        queue_name (str): The name of the queue.
        connection (pika.BlockingConnection): The RabbitMQ connection.
        channel (pika.adapters.blocking_connection.BlockingChannel): The channel of the connection.
    """

    def __enter__(self):
        """
        Enter method for context manager.

        Returns:
            rmq_connector: Returns self.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method for context manager. Closes the connection.

        Args:
            exc_type (Type[BaseException]): The type of the exception.
            exc_value (BaseException): The instance of the exception.
            traceback (TracebackType): A traceback object.
        """
        self.connection.close()

    def __init__(self, queue_name) -> None:
        """
        The constructor for rmq_connection class.

        Args:
            queue_name (str): The name of the queue.
        """
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def publish(self, message):
        """
        Publishes a message to the queue.

        Args:
            message (str): The message to be published.
        """
        message_size = get_message_size(message)
        message = message + " size:" + str(message_size)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(),
        )
        print(" [x] Sent %r" % message.replace("a", ""))

    def consume(self, callback):
        """
        Consumes messages from the queue.

        Args:
            callback (function): The callback function to be called when a message is received.
        """
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    @staticmethod
    def callback(ch, method, properties, body):
        """
        Callback function that is called when a message is received.

        Args:
            ch (pika.adapters.blocking_connection.BlockingChannel): The channel.
            method (pika.spec.Basic.Deliver): The method.
            properties (pika.spec.BasicProperties): The properties.
            body (bytes): The body of the message.
        """
        print("Received message:", body.decode()[-10:])
