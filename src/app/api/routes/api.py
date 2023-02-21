from fastapi import APIRouter

from src.services.handler import Handler

handler = Handler()

router = APIRouter()


@router.get("/hello")
def hello():
    return {"message": "Hello World"}


@router.get("/optimize")
def optimize():
    message = handler.optimize()
    return message


# @router.put("/update_db")
# def update_db(stagger: Stagger):
#     settings.log.info(f'Sending message to ETL queue: "extract_all"')
#     handler.send_message(b'extract_all', exchange=settings.EXCHANGE, routing=settings.QUEUE_ETL_ROUTING_KEY)
#
#     settings.log.info(f'Waiting for ETL to finish')
#     etl_message = handler.get_message()
#
#     settings.log.info(f'ETL finished successfully') if etl_message == "ETL_DONE" \
#         else settings.log.info(f'ETL failed')
