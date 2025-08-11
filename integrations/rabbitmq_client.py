import pika
import json
import logging
from config.config import config

logger = logging.getLogger(__name__)

class RabbitMQClient:
    def __init__(self):
        self.connection_params = pika.ConnectionParameters(
            host=config.RABBITMQ_HOST,
            credentials=pika.PlainCredentials(
                config.RABBITMQ_USER,
                config.RABBITMQ_PASS
            )
        )
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Устанавливает соединение с RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=config.RABBITMQ_QUEUE, durable=True)
            logger.info("Connected to RabbitMQ")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            return False
    
    def send_message(self, message: dict):
        """Отправляет сообщение в очередь"""
        try:
            if not self.channel or self.channel.is_closed:
                self.connect()
            
            self.channel.basic_publish(
                exchange='',
                routing_key=config.RABBITMQ_QUEUE,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            logger.debug(f"Message sent to RabbitMQ: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message to RabbitMQ: {str(e)}")
            return False
    
    def close(self):
        """Закрывает соединение с RabbitMQ"""
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("RabbitMQ connection closed")