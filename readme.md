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
TODO: Безопасность при взаимодействии через API планирую обеспечить путем добавления API-ключа или JWT-токенов. Это станет возможно после создания auth-service.

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
      SERVER_PORT: ${NOTIFICATIONS_PORT}          # порт на, на котором запускается FastApi
      ROOT_PATH: ${ROOT_PATH}                     # префикс на Nginx перед приложением - например /notifications 
      TG_BOT_TOKEN: ${TG_BOT_TOKEN}               # токен ТГ бота
      TG_DEFAULT_CHAT_ID: ${TG_DEFAULT_CHAT_ID}   # id ТГ чата, куда по умолчанию приходят системные сообщения
      RABBITMQ_HOST: ${RABBITMQ_HOST}             # хост rabbitmq
      RABBITMQ_PORT: ${RABBITMQ_PORT}             # порт rabbitmq
      RABBITMQ_USER: ${RABBITMQ_USER}             # пользователь rabbitmq
      RABBITMQ_PASSWORD: ${RABBITMQ_PASSWORD}     # пароль пользователя rabbitmq
      RABBITMQ_QUEUE_NAME: ${RABBITMQ_QUEUE_NAME} # имя очереди для сообщений в rabbitmq
      POSTGRES_HOST: ${POSTGRES_HOST}             # хост бд
      POSTGRES_PORT: ${POSTGRES_PORT}             # порт бд
      POSTGRES_USER: ${POSTGRES_USER}             # пользователь бд
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}     # пароль пользователя бд
      POSTGRES_DB: ${POSTGRES_DB}                 # имя бд
      DROP_TABLES: ${DROP_TABLES}                 # надо ли удалять существующую схему
      CREATE_TABLES: ${CREATE_TABLES}             # надо ли создавать новую схему
      RUSTORE_PUSH_PROJECT_ID: ${RUSTORE_PUSH_PROJECT_ID}
      RUSTORE_PUSH_SERVICE_TOKEN: ${RUSTORE_PUSH_SERVICE_TOKEN}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${NOTIFICATIONS_PORT}/health_check"]
      interval: 180s
      timeout: 10s
      retries: 3
      start_period: 10s
...
```
### Планы:
Steps:
1. [готово] Просто сервис который слушает RabbitMQ/Kafka для отправки разовых сообщений. На данном этапе реализация только ТГ
2. [готово] Локализация
3. Реализация триггеров хранимых в бд, планировщика; Добавить Fast API
4. Реализации других мессенджеров
5. Реализация Push через Rustore SDK (работает при уставновленных VK сервисах)
6. [готово] Функционал техподдержки в ботов (хотя бы на уровне "сообщить об ошибке")
7. Соединение через чат бота специалиста техподдержки с пользователем

### Features:
Также реализован REST API - FastAPI для будущей более детальной настройки уведомлений, рассылок, триггеров.
