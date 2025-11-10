# Notifications-service
### Summary:
Сервис, управляющий разными способами отправки сообщений пользователям.

### На данный момент поддерживаются:
1. Telegram
2. ...

### Взаимодействие:
Сервис получает задачи из брокера сообщений RabbitMQ (потом возможно Kafka). Структура сообщения:
```json
{
    "title": <text>,
    "body": <text>,
    "sender": <text>
}
```
где `sender` это тип отправителя (например, TG / ...).
Архитектура заточена под легкое добавление новых `sender`, для этого достаточно унаследоваться от `BaseSender` и реализовать необходимые методы.
Безопасность при взаимодействии через API планирую обеспечить путем добавления API-ключа или JWT-токенов

### Запуск:
Сначала необходимо сбилдить образ:
```sh
docker build -t notifications-service:latest .
```
Для запуска можно использовать общий манифест docker-compose.yaml, потому что необходимо передать переменные окружения:
```yaml
services:
...
  notifications:
    container_name: notifications-service
    image: notifications-service:latest
    ports:
      - "${NOTIFICATIONS_PORT}:${NOTIFICATIONS_PORT}"
    environment:
      SERVER_PORT: ${NOTIFICATIONS_PORT}
      TG_BOT_TOKEN: ${TG_BOT_TOKEN}
      TG_DEFAULT_CHAT_ID: ${TG_DEFAULT_CHAT_ID}
      RABBITMQ_PORT: ${RABBITMQ_PORT}
      RABBITMQ_ADMINPANEL_PORT: ${RABBITMQ_ADMINPANEL_PORT}
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_DEFAULT_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_DEFAULT_PASS}
      RABBITMQ_QUEUE_NAME: ${RABBITMQ_QUEUE_NAME}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${NOTIFICATIONS_PORT}/health_check"]
      interval: 180s
      timeout: 10s
      retries: 3
      start_period: 20s
...
```
### Планы:
см. notes.md

Также реализован REST API - FastAPI для будущей более детальной настройки уведомлений, рассылок, триггеров.
