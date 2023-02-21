from src.config import settings


def get_queues() -> list:
    return [settings.QUEUE_ETL, settings.QUEUE_OPTIMIZER, settings.QUEUE_MIGRATION,
            settings.QUEUE_ETL_RESPONSE, settings.QUEUE_OPTIMIZER_RESPONSE,settings.QUEUE_MIGRATION_RESPONSE]


def get_exchanges() -> list:
    return [settings.EXCHANGE, settings.EXCHANGE_RESPONSE]


# def get_routing_keys() -> list:
#     return [settings.QUEUE_ETL_ROUTING_KEY, settings.QUEUE_OPTIMIZER_ROUTING_KEY, settings.QUEUE_MIGRATION_ROUTING_KEY,
#             settings.QUEUE_ETL_RESPONSE_ROUTING_KEY, settings.QUEUE_OPTIMIZER_RESPONSE_ROUTING_KEY,
#             settings.QUEUE_MIGRATION_RESPONSE_ROUTING_KEY]
