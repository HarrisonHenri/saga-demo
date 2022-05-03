from celery import Celery
from saga_framework import close_sqlalchemy_db_connection_after_celery_task_ends

from app_common import settings
from app_common.messaging import CREATE_ORDER_SAGA_RESPONSE_QUEUE
from .app import CreateOrderSaga, db, CreateOrderSagaRepository

create_order_saga_responses_celery_app = Celery(
    'create_order_saga_responses',
    broker=settings.CELERY_BROKER)
create_order_saga_responses_celery_app.conf.task_default_queue = CREATE_ORDER_SAGA_RESPONSE_QUEUE

close_sqlalchemy_db_connection_after_celery_task_ends(db.session)

saga_state_repository = CreateOrderSagaRepository()
CreateOrderSaga.register_async_step_handlers(saga_state_repository,
                                             create_order_saga_responses_celery_app)
