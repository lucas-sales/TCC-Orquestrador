import ast
import logging
import os

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(format="%(asctime)s |%(name)s| %(levelname)s: %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# APP
CSV_FILE_PATH = os.environ.get('CSV_FILE_PATH')
PLUGIN = os.environ.get('PLUGIN')

# Rabbitmq
RABBITMQ_URL = os.environ.get('RABBITMQ_URL')
EXCHANGE = os.environ.get('EXCHANGE')
EXCHANGE_TYPE = os.environ.get('EXCHANGE_TYPE')
QUEUE = os.environ.get('QUEUE')
CONSUMER_TAG = os.environ.get('CONSUMER_TAG')


def load():
    log.info('Loading settings...')
    required_env_vars = [
        'CSV_FILE_PATH',
        'PLUGIN',
        'RABBITMQ_URL',
        'EXCHANGE',
        'EXCHANGE_TYPE',
        'QUEUE',
        'CONSUMER_TAG'
    ]

    for env_var in required_env_vars:
        if env_var not in os.environ:
            raise EnvironmentError(f'Environment variable not founded.')
