import pika

from src.config import settings


class RabbitmqHandler:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.consumer = None
        self.producer = None
        self.message_data = None
        self._config_rabbitmq()

    def _config_rabbitmq(self):

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_URL))
        self.channel = self.connection.channel()

        # Declaration of rabbitmq structure
        self.channel.exchange_declare(exchange=settings.EXCHANGE,
                                      exchange_type=settings.EXCHANGE_TYPE,
                                      passive=False,
                                      durable=True,
                                      auto_delete=False)

        self.channel.exchange_declare(exchange=settings.EXCHANGE_RESPONSE,
                                      exchange_type=settings.EXCHANGE_TYPE,
                                      passive=False,
                                      durable=True,
                                      auto_delete=False)

        self.channel.queue_declare(queue=settings.QUEUE_ETL)
        self.channel.queue_bind(queue=settings.QUEUE_ETL,
                                exchange=settings.EXCHANGE,
                                routing_key=settings.QUEUE_ETL_ROUTING_KEY)

        self.channel.queue_declare(queue=settings.QUEUE_ETL_RESPONSE)
        self.channel.queue_bind(queue=settings.QUEUE_ETL_RESPONSE,
                                exchange=settings.EXCHANGE_RESPONSE,
                                routing_key=settings.QUEUE_ETL_RESPONSE_ROUTING_KEY)

        def callback(ch, method, properties, body):
            # self.channel.basic_ack(delivery_tag=method.delivery_tag)
            self.message_data = body.decode('utf-8')

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
        except:
            print("error")

    def basic_producer(self, exchange, routing_key, body):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=body)

    def get_message(self):
        return self.message_data
