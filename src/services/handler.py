from src.services.rabbitmq_handler import RabbitmqHandler


class Handler:
    def __init__(self):
        self.rabbit_handler = RabbitmqHandler()

    def run(self):
        print(" [x] Sent 'Hello World!'")
        self.rabbit_handler.basic_producer(exchange='',
                                           routing_key='orchestrator',
                                           body=b'extract_all')

        self.rabbit_handler.basic_consume()
        print(self.rabbit_handler.get_message())
