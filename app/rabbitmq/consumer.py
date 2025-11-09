from aio_pika import connect_robust, Message, Queue, Channel, IncomingMessage
import asyncio
import logging

from app.configs.rabbitmq_config import RabbitMQConfig
from app.configs import RABBITMQ_CONFIG
from app.models.pydantic.msg import Msg
from app.sender import create_sender


async def listen_rabbitmq(config: RabbitMQConfig = RABBITMQ_CONFIG):
    global channel

    connection = await connect_robust(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        login=config.RABBITMQ_USER,
        password=config.RABBITMQ_PASSWORD
    )

    async with connection:
        channel = await connection.channel()

        queue: Queue
        queue = await channel.declare_queue(config.RABBITMQ_QUEUE_NAME, durable=True)

        await queue.consume(on_message_post)
        logging.debug("Waiting for messages...")

        await asyncio.Future()

__encoding_to = "utf-8"


async def on_message_post(incoming_message: IncomingMessage):
    async with incoming_message.process(ignore_processed=True):
        logging.debug(
            f"New msg delivered: {incoming_message.body.decode(__encoding_to)}")
        try:
            msg_data = Msg.model_validate_json(
                incoming_message.body.decode(__encoding_to))

            msg_sender = create_sender(msg_data.sender)
            # ...
            # TODO: отправка
            # ...
            success = True

            if not success:
                # WARNING: если будет ошибка, то при requeue=True получится бесконечный цикл
                # -> пересылать в очередь для ошибок
                await incoming_message.reject(requeue=True)

            await incoming_message.ack()
            logging.debug(
                f"Msg successfully proccessed")
        except Exception as e:
            logging.error("Error while msg proccessed: ", exc_info=True)
            await incoming_message.nack()
