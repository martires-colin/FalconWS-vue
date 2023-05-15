from os import environ as env

configurations = {
    "host": "35.93.147.38", # IP address of RabbitMQ server
    "port": 5672, # port of RabbitMQ server
    "vhost": "demo", # name of virtual host
    "user": env.get("RABBITMQ_USER"), # user with access to server
    "password": env.get("RABBITMQ_PASSWORD") # password associated with user
}
