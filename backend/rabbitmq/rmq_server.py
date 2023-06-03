# from rabbitmq.config_rabbitmq import configurations
# import uuid
# import json
# import pika
# from mongodb.mongo_config import *


# credentials = pika.PlainCredentials(
#     username=configurations["user"], password=configurations["password"], 
#     erase_on_connect=True
# )
# parameters = pika.ConnectionParameters(
#     host=configurations["host"], port=configurations["port"], 
#     virtual_host=configurations["vhost"], credentials=credentials
# )

# class RequestConnection: 
#     def __init__(self):
#         self.connection = pika.BlockingConnection(parameters)
#         self.channel = self.connection.channel()

#         queue_result = self.channel.queue_declare(queue="", exclusive=True)
#         self.callback_queue = queue_result.method.queue
#         self.channel.basic_consume(
#             queue=self.callback_queue, on_message_callback=self.on_response, 
#             auto_ack=True
#         )

#         self.corr_id = str(uuid.uuid4())
#         self.properties = pika.BasicProperties(
#             reply_to=self.callback_queue, correlation_id=self.corr_id
#         )
        
#         self.response = None
    

#     def on_response(self, ch, method, props, body):
#         if self.corr_id == props.correlation_id:
#             self.response = json.loads(body.decode())


# def request(node_ip, command, argument, argument2=None, argument3=None):
#     request = RequestConnection()
    
#     message = {"command": command, "argument": argument}
#     if argument2:
#         message["argument2"] = argument2
#     if argument3:
#         message["argument3"] = argument3
#     message = json.dumps(message)
    

#     request.channel.queue_declare(queue=node_ip)
#     request.channel.basic_publish(
#         exchange="", routing_key=node_ip, body=message,
#         properties=request.properties
#     )

#     request.connection.process_data_events(time_limit=None)
#     request.connection.close()

#     return request.response


# def verify(node_ip, access_token):
#     access_token = json.dumps(access_token)
#     verification_response = request(node_ip, "verify", access_token)

#     if verification_response["success"] == True:
#         update_database(node_ip, "verified")
#         print(f" [x] {node_ip}: Verified connection.")

#     else:
#         print(f" [x] {node_ip}: ERROR - Failed to verify connection.")
#         # TODO: handle failed verification


# def list_directory(node_ip, directory):
#     list_response = request(node_ip, "list", directory)

#     if list_response["success"] == True:
#         print(f" [x] {node_ip}: Received file list for {directory}.")
#         return list_response["files"]
    
#     else:
#         print(f" [x] {node_ip}: ERROR - Failed to list directory.")
#         # TODO: handle failed list

#         files = {
#             "DATA_TYPE": "file_list",
#             "path": directory,
#             "DATA": []
#         }
#         return files


# def transfer(receiver_ip, receiver_directory, sender_ip, sender_file_list):
#     max_receivers = 20
#     # if receiver_ip.num_receivers >= max_receivers: TODO Colin
#         # print(f" [x] {receiver_ip}: ERROR - Maximum number of receivers active.")
#         # TODO: handle failed receiver startup
#         # return

#     max_senders = 20
#     # if sender_ip.num_senders >= max_senders: TODO Colin
#         # print(f" [x] {sender_ip}: ERROR - Maximum number of senders active.")
#         # TODO: handle failed sender startup
#         # return
    
#     # increment receiver_ip.num_receivers TODO Colin 
#     # increment sender_ip.num_senders TODO Colin

#     sender_files = ",".join(sender_file_list)
#     receive_response = request(receiver_ip, "receive", receiver_directory, 
#         sender_ip, sender_files
#     )

#     if receive_response["success"] == True:
#         print(f" [x] {receiver_ip}: Falcon receiver is now active.")
#         receiver_port = receive_response["port"]
#         send_response = request(sender_ip, "send", receiver_ip, 
#             receiver_port, sender_files
#         )

#         if send_response["success"] == True:
#             # TODO: handle successful send (confirm success with receiver node)
#             print(f" [x] {sender_ip}: Completed file transfer to {receiver_ip}.")

#         else:
#             print(f" [x] {sender_ip}: ERROR - Failed to send files to {receiver_ip}.")
#             # TODO: handle failed send (kill Falcon receiver)

#     else:
#         print(f" [x] {receiver_ip}: ERROR - Failed to start Falcon receiver.")
#         # TODO: handle failed receiver startup

#     # decrement receiver_ip.num_receivers TODO Colin
#     # decrement sender_ip.num_senders TODO Colin


# def manage_connections():
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()

#     connection_queue = "connections"
#     channel.queue_declare(queue=connection_queue)
#     channel.basic_consume(
#         queue=connection_queue, on_message_callback=on_connection, 
#         auto_ack=True
#     )
#     print(" [x] Waiting for status updates from Falcon nodes...")
#     channel.start_consuming()

#     # TODO: close connection (https://gist.github.com/josephernest/77fdb0012b72ebdf4c9d19d6256a1119)


# def on_connection(ch, method, props, body):
#     status_message = json.loads(body.decode())
#     update_database(status_message["ip"], status_message["status"])
#     print(f" [x] {status_message['ip']}: Node is {status_message['status']}.")


# def update_database(node_ip: str, status: str):
#     # update status in database TODO Colin
#     print(f"Updating: {node_ip}\nNew Status: {status}")
#     idp_ips.update_many({"ip": node_ip}, {"$set": {"status": status}})

# -----------------------------------------------------------------------------------


# RabbitMQ communication for Falcon web server

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from pika.exceptions import AMQPError

from rabbitmq.config_rabbitmq import configurations
import json
import pika
import uuid
from mongodb.mongo_config import *


MAX_USERS = 20 # limited by range of ports to reserve for Falcon receivers
CONNECTION_QUEUE = "connections"

credentials = pika.PlainCredentials(username=configurations["user"], 
    password=configurations["password"], erase_on_connect=True)
            
parameters = pika.ConnectionParameters(host=configurations["host"],
    port=configurations["port"], virtual_host=configurations["vhost"], credentials=credentials)


def manage_connections() -> None:
    """Manages Falcon node status messages."""
    # Connect to the RabbitMQ server
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(CONNECTION_QUEUE)

    except AMQPError:
        print(f" [{CONNECTION_QUEUE}] Failed to start consuming Falcon node status messages.")

    # Consume status update messages from Falcon nodes
    else:
        try:
            channel.basic_consume(queue=CONNECTION_QUEUE, on_message_callback=on_status_message)
            print(f" [{CONNECTION_QUEUE}] Waiting for Falcon node status messages...")
            channel.start_consuming()

        except:
            if channel.is_open:
                channel.stop_consuming()
                channel.close()

            if connection.is_open:
                connection.close()

            print(f" [{CONNECTION_QUEUE}] Stopped consuming Falcon node status messages.")


def on_status_message(ch: BlockingChannel, method: Basic.Deliver, 
    props: BasicProperties, body: bytes) -> None:
    """Consumer Callback: Updates Falcon node connection status in database."""
    message = json.loads(body.decode())
    node_ip = message["ip"]
    status = message["status"]

    # *DB.node_ip.status* = status TODO Colin

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f" [{CONNECTION_QUEUE}] Falcon node at {node_ip} is now {status}.")


class FalconRequestProcessor: 
    def __init__(self):
        self.corr_id = str(uuid.uuid4())
        self.connection: pika.BlockingConnection = None
        self.channel: BlockingChannel = None
        self.callback_queue: str = None
        self.started = False
        self.response: dict = None


    def start(self, queues: list) -> None:
        """Opens connection with RabbitMQ server."""
        try:
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            for queue in queues:
                self.channel.queue_declare(queue)

            self.started = True

        except AMQPError:
            self.started = False


    def request(self, queue: str, message: dict) -> dict:
        """Sends request message to Falcon node and returns response."""
        try:
            queue_result = self.channel.queue_declare(queue="", exclusive=True)
            callback_queue = queue_result.method.queue
            self.channel.basic_consume(queue=callback_queue, 
                on_message_callback=self.on_response)

            props = pika.BasicProperties(reply_to=callback_queue, correlation_id=self.corr_id)
            self.channel.basic_publish(exchange="", routing_key=queue, 
                body=json.dumps(message), properties=props)
            
            self.connection.process_data_events(time_limit=None)
            return self.response

        except AMQPError:
            return {"success": False, "error": "Failed to execute Falcon request."}


    def on_response(self, ch: BlockingChannel, method: Basic.Deliver, 
        props: BasicProperties, body: bytes) -> None:
        """Consumer Callback: Saves the Falcon node response message."""
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body.decode())

        ch.basic_ack(delivery_tag=method.delivery_tag)
    

    def cleanup(self) -> None:
        """Closes connection with RabbitMQ server."""
        if self.channel is not None and self.channel.is_open:
            self.channel.close()

        if self.connection is not None and self.connection.is_open:
            self.connection.close()
    

# TODO Colin
def can_add_user(user: str, node_ip: str) -> bool:
    """Finds if user process can be created on a Falcon node."""
    pass
    # if *DB.node_ip.num_users* == MAX_USERS:
    #    return False

    # if user in *DB.node_ip.user_list*:
    #    return False

    # return True


def add_user(user: str, node_ip: str, access_token: dict) -> bool:
    """Creates user process on Falcon node."""
    # Start request processor
    queue = node_ip + "-root"
    processor = FalconRequestProcessor()
    processor.start([queue])

    if not processor.started:
        processor.cleanup()
        print(f" [{queue}] Failed to connect to RabbitMQ.")
        return False
    
    # Send 'add_user' request to Falcon node and process response
    message = {"cmd": "add_user", "arg_1": access_token, "arg_2": user}
    response = processor.request(queue, message)
    processor.cleanup()

    if not response["success"]:
        print(f" [{queue}] Failed to create user process for {user}.")
        return False

    # *DB.node_ip.num_users* += 1 # TODO Colin
    # *DB.node_ip.user_list*.append(user) # TODO Colin

    print(f" [{queue}] Created user process for {user}.")
    return True


def list_directory(user:str, node_ip: str, directory: str) -> dict:
    """Lists contents of directory on Falcon node."""
    # Start request processor
    queue = node_ip + "-" + user
    processor = FalconRequestProcessor()
    processor.start([queue])

    if not processor.started:
        processor.cleanup()
        print(f" [{queue}] Failed to connect to RabbitMQ.")
        return {"DATA_TYPE": "file_list", "path": directory, "DATA": []}

    # Send 'list_directory' request to Falcon node and process response 
    message = {"cmd": "list_directory", "arg_1": directory}
    response = processor.request(queue, message)
    processor.cleanup()
        
    if not response["success"]:
        print(f" [{queue}] Failed to list contents of '{directory}'.")
        return {"DATA_TYPE": "file_list", "path": directory, "DATA": []}
    
    print(f" [{queue}] Received list of contents of '{directory}'.")
    return response["files"]


def transfer(user: str, receiver_ip: str, receiver_dir: str, sender_ip: str,
        sender_file_list: list) -> bool:
    """Coordinates the Falcon file transfer sequence between sites."""
    # Start request processor
    receiver_queue = receiver_ip + "-" + user
    sender_queue = sender_ip + "-" + user
    processor = FalconRequestProcessor()
    processor_started = processor.start([receiver_queue, sender_queue])

    if not processor_started:
        processor.cleanup()
        print(f" [{receiver_queue}] Failed to connect to RabbitMQ.")
        return False

    # Send 'start_receive' request to receiver node and process response
    message = {"cmd": "start_receive", "arg_1": receiver_dir, "arg_2": sender_ip}
    start_response = processor.request(receiver_queue, message)

    if not start_response["success"]:
        processor.cleanup()
        print(f" [{receiver_queue}] Failed to start Falcon receiver.")
        return False
        
    print(f" [{receiver_queue}] Falcon receiver is now active.")

    # Send 'send' request to sender node and process response
    port = start_response["port"]
    sender_files = ",".join(sender_file_list)
    message = {"cmd": "send", "arg_1": receiver_ip, "arg_2": port, "arg_3": sender_files}
    send_response = processor.request(sender_queue, message)

    if send_response["success"]:
        print(f" [{sender_queue}] Completed file transfer to {receiver_ip}.")
    else:
        print(f" [{sender_queue}] Failed to send files to {receiver_ip}.")

    # Send 'end_receive' request to receiver node and process response
    message = {"cmd": "end_receive", "arg_1": sender_ip}
    end_response = processor.request(receiver_queue, message)
    processor.cleanup()

    if end_response["success"]:
        print(f" [{receiver_queue}] Completed file transfer from {sender_ip}.")
    else:
        print(f" [{receiver_queue}] Failed to receive files from {sender_ip}.")

    return end_response["success"]