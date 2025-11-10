from aio_pika import connect_robust, Queue, IncomingMessage
import asyncio
import logging

from app.configs.rabbitmq_config import RabbitMQConfig
from app.configs import RABBITMQ_CONFIG
from app.models.pydantic.msg import Msg
from app.sender import create_sender, BaseSender


async def listen_rabbitmq(config: RabbitMQConfig = RABBITMQ_CONFIG):
    logging.debug(config.__str__())

    global channel

    connection = await connect_robust(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        login=config.RABBITMQ_USER,
        password=config.RABBITMQ_PASSWORD
    )

    async with connection:
        channel = await connection.channel()

        queue: Queue = await channel.declare_queue(config.RABBITMQ_QUEUE_NAME, durable=True)

        await queue.consume(on_message_post)
        logging.debug("Waiting for messages...")

        await asyncio.Future()

__encoding_to = "utf-8"


async def on_message_post(incoming_message: IncomingMessage):
    async with incoming_message.process(ignore_processed=True):
        logging.debug(
            f"New msg delivered: {incoming_message.body.decode(__encoding_to)}")
        try:
            msg_data: Msg = Msg.model_validate_json(
                incoming_message.body.decode(__encoding_to))

            msg_sender: BaseSender = create_sender(msg_data.sender)
            success = await msg_sender.send_single(msg=msg_data)

            if not success:
                # WARNING: если будет ошибка, то при requeue=True получится бесконечный цикл
                # -> пересылать в очередь для ошибок
                await incoming_message.reject(requeue=True)
                raise Exception()

            await incoming_message.ack()
            logging.debug(
                f"Msg successfully proccessed")
        except Exception as e:
            logging.error("Error while msg proccessed: ", exc_info=True)
            await incoming_message.nack()
