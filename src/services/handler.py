from src.config import settings
from src.services.rabbitmq_handler import RabbitmqHandler


class Handler:
    def __init__(self):
        self.rabbit_handler = RabbitmqHandler()

    def run(self):
        settings.log.info(" [x] Sent 'Hello World!'")
        self.rabbit_handler.basic_producer(exchange=settings.EXCHANGE,
                                           routing_key=settings.QUEUE_ETL_ROUTING_KEY,
                                           body=b'extract_all')

        self.rabbit_handler.basic_consume()
        if self.rabbit_handler.response_data == "ETL_DONE":
            self.rabbit_handler.basic_producer(exchange=settings.EXCHANGE,
                                               routing_key=settings.QUEUE_OPTIMIZER_ROUTING_KEY,
                                               body=b'optimize')
