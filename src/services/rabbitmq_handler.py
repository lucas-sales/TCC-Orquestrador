import pika

from src.config import settings
from src.models.rabbitmq_strategy import RabbitmqStrategy
from src.utils.rabbitmq_variables_optimizer import get_exchanges, get_queues


class RabbitmqHandler(RabbitmqStrategy):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.consumer = None
        self.producer = None
        self._response_data = None
        self._config_rabbitmq()

    @property
    def response_data(self):
        return self._response_data

    @response_data.setter
    def response_data(self, new_value):
        self._response_data = new_value

    def _config_rabbitmq(self):

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_URL))
        self.channel = self.connection.channel()

        # Declaration of rabbitmq structure
        for exchange in get_exchanges():
            self.channel.exchange_declare(exchange=exchange,
                                          exchange_type=settings.EXCHANGE_TYPE,
                                          passive=False,
                                          durable=True,
                                          auto_delete=False)

        for queue in get_queues():
            self.channel.queue_declare(queue=queue)

        self.channel.queue_bind(queue=settings.QUEUE_ETL,
                                exchange=settings.EXCHANGE,
                                routing_key=settings.QUEUE_ETL_ROUTING_KEY)

        self.channel.queue_bind(queue=settings.QUEUE_OPTIMIZER,
                                exchange=settings.EXCHANGE,
                                routing_key=settings.QUEUE_OPTIMIZER_ROUTING_KEY)

        self.channel.queue_bind(queue=settings.QUEUE_MIGRATION,
                                exchange=settings.EXCHANGE,
                                routing_key=settings.QUEUE_MIGRATION_ROUTING_KEY)

        self.channel.queue_bind(queue=settings.QUEUE_ETL_RESPONSE,
                                exchange=settings.EXCHANGE_RESPONSE,
                                routing_key=settings.QUEUE_ETL_RESPONSE_ROUTING_KEY)

        self.channel.queue_bind(queue=settings.QUEUE_OPTIMIZER_RESPONSE,
                                exchange=settings.EXCHANGE_RESPONSE,
                                routing_key=settings.QUEUE_OPTIMIZER_RESPONSE_ROUTING_KEY)

        self.channel.queue_bind(queue=settings.QUEUE_MIGRATION_RESPONSE,
                                exchange=settings.EXCHANGE_RESPONSE,
                                routing_key=settings.QUEUE_MIGRATION_RESPONSE_ROUTING_KEY)

        def callback(ch, method, properties, body):
            self.response_data = body.decode('utf-8')

            self.channel.basic_cancel(consumer_tag=settings.CONSUMER_TAG)
            self.channel.stop_consuming()

        self.consumer = self.channel.basic_consume(queue=settings.QUEUE_ETL_RESPONSE,
                                                   auto_ack=True,
                                                   on_message_callback=callback,
                                                   consumer_tag=settings.CONSUMER_TAG)

    def basic_consume(self):
        try:
            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
        except Exception as e:
            print(e)

    def basic_producer(self, exchange, routing_key, body):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=body)
