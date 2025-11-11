from aio_pika import Message, connect_robust, Queue, IncomingMessage
from aio_pika.abc import AbstractRobustConnection
import asyncio
import logging

from app.configs.rabbitmq_config import RabbitMQConfig
from app.configs import RABBITMQ_CONFIG
from app.models.pydantic.msg import Msg
from app.sender import create_sender, BaseSender


class RabbitMQConsumer:
    def __init__(self, config: RabbitMQConfig = RABBITMQ_CONFIG):
        self.connection: AbstractRobustConnection = None
        self.__encoding_to = "utf-8"
        self.RABBITMQ_NACK_QUEUE_NAME = "nacks"
        self.config: RabbitMQConfig = config

    async def connect(self, config: RabbitMQConfig = RABBITMQ_CONFIG) -> bool:
        self.config = config
        try:
            self.connection = await connect_robust(
                host=self.config.RABBITMQ_HOST,
                port=int(self.config.RABBITMQ_PORT),
                login=self.config.RABBITMQ_USER,
                password=self.config.RABBITMQ_PASSWORD
            )
        except Exception as e:
            logging.error(f"Error connecting to RabbitMQ: {e}")
            logging.debug(self.config.__str__())
            return False
        else:
            logging.debug("RabbitMQ connected successfully.")
            return True

    async def listen(self):
        async with self.connection:
            channel = await self.connection.channel()

            queue: Queue = await channel.declare_queue(self.config.RABBITMQ_QUEUE_NAME, durable=True)
            logging.debug("RabbitMQ queues defined")

            await queue.consume(self.__on_message_post)
            logging.debug("Waiting for messages...")

            await asyncio.Future()

    async def __on_message_post(self, incoming_message: IncomingMessage):
        async with incoming_message.process(ignore_processed=True):
            logging.debug(
                f"New msg delivered: {incoming_message.body.decode(self.__encoding_to)}")
            try:
                msg_data: Msg = Msg.model_validate_json(
                    incoming_message.body.decode(self.__encoding_to))

                msg_sender: BaseSender = create_sender(msg_data.sender)
                success = await msg_sender.send_single(msg=msg_data)

                if not success:
                    if await self.__requeue_to_nack(msg_data):
                        logging.warning(
                            f"Unable to requeue msg to nack queue: {msg_data.model_dump_json()}")
                    # NOTE: не стоит гонять заведомо сломанное сообщение бесконечно
                    await incoming_message.reject(requeue=False)
                    raise Exception("Msg failed")

                await incoming_message.ack()
                logging.debug(f"Msg successfully proccessed")
            except Exception as e:
                logging.error("Error while msg proccessed: ", exc_info=True)

    async def __requeue_to_nack(self, msg: Msg) -> bool:
        channel = await self.connection.channel()
        queue = await channel.declare_queue(self.config.RABBITMQ_QUEUE_NAME, durable=True)

        nack_msg = Message(
            body=msg.model_dump_json().encode(self.__encoding_to),
            content_type="application/json",
            headers={"status": "ok"}
        )
        await channel.default_exchange.publish(
            nack_msg, routing_key=self.RABBITMQ_NACK_QUEUE_NAME
        )
