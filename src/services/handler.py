from src.config import settings
from src.models.handler_strategy import HandlerStrategy
from src.services.rabbitmq_handler import RabbitmqHandler


class Handler(HandlerStrategy):
    def __init__(self):
        self.rabbit_handler = RabbitmqHandler()

    def send_message(self, message: bytes, exchange: str, routing: str) -> None:
        self.rabbit_handler.basic_producer(exchange=exchange,
                                           routing_key=routing,
                                           body=message)

    def get_message(self) -> str:
        self.rabbit_handler.basic_consume()
        return self.rabbit_handler.response_data

    def optimize(self):
        settings.log.info(f'Sending message to ETL queue: "extract_all"')
        self.send_message(message=b'extract_all',
                          exchange=settings.EXCHANGE,
                          routing=settings.QUEUE_ETL_ROUTING_KEY)

        settings.log.info(f'Waiting for ETL to finish')
        etl_message = self.get_message()

        if etl_message == "ETL_DONE":
            settings.log.info(f'ETL finished successfully')
            settings.log.info(f'Sending message to Optimizer queue: "optimize"')

            self.send_message(message=b'optimize',
                              exchange=settings.EXCHANGE,
                              routing=settings.QUEUE_OPTIMIZER_ROUTING_KEY)

            optimizer_message = self.get_message()

            if optimizer_message == "OPTIMIZER_DONE":
                settings.log.info(f'Optimizer finished successfully')

                self.send_message(message=b'migrate',
                                  exchange=settings.EXCHANGE,
                                  routing=settings.QUEUE_MIGRATION_ROUTING_KEY)

                settings.log.info(f'Migrator finished successfully')
                return {"message": "Optimization map:"}
            else:
                settings.log.info(f'Optimizer failed, exiting')

        else:
            settings.log.info(f'ETL failed, exiting')
