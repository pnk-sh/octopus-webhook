# Octopus Webhook
Small application build in Python by using Flask as rest framework, point for this to capture events from Docker Hub everytime a Webhooks is triggered and store it into a database.

You can enable RabbitMQ to automatic sending the webhook settings to RabbitMQ queue so its automatic can prepare deployment process. RabbitMQ is disabled as defualt.

## System requirement
- Python 3.9+
- MongoDB 4.4+
- RabbitMQ 3.8+
