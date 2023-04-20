# # RabbitMQ communication for Falcon server


# from rabbitmq.config_rabbitmq import configurations
# import uuid
# import json
# import pika



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


# def request(node_ip, command, argument, argument2=None):
#     request = RequestConnection()
    
#     message = {"command": command, "argument": argument}
#     if argument2 != None:
#         message["argument2"] = argument2
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


# def transfer(sender_ip, receiver_ip, file_list):
#     files = ",".join(file_list)
#     receive_response = request(receiver_ip, "receive", sender_ip, files)

#     if receive_response["success"] == True:
#         print(f" [x] {receiver_ip}: Falcon receiver is now active.")
#         send_response = request(sender_ip, "send", receiver_ip, files)

#         if send_response["success"] == True:
#             # TODO: handle successful send (confirm success with receiver node)
#             print(f" [x] {sender_ip}: Completed file transfer to {receiver_ip}.")

#         else:
#             print(f" [x] {sender_ip}: ERROR - Failed to send files to {receiver_ip}.")
#             # TODO: handle failed send (kill Falcon receiver)

#     else:
#         print(f" [x] {receiver_ip}: ERROR - Failed to start Falcon receiver.")
#         # TODO: handle failed receiver startup


# def manage_connections():
#     try:
#         connection = pika.BlockingConnection(parameters)
#         channel = connection.channel()

#         connection_queue = "connections"
#         channel.queue_declare(queue=connection_queue)
#         channel.basic_consume(
#             queue=connection_queue, on_message_callback=on_connection, 
#             auto_ack=True
#         )
#         print(" [x] Waiting for status updates from Falcon nodes...")
#         channel.start_consuming()

#     except KeyboardInterrupt:
#         pass # TODO: close connection (if possible)


# def on_connection(ch, method, props, body):
#     status_message = json.loads(body.decode())
#     update_database(status_message["ip"], status_message["status"])
#     print(f" [x] {status_message['ip']}: Node is {status_message['status']}.")


# def update_database(node_ip: str, status: str):
#     # TODO update database (for Colin)
#     print(f"Updating: {node_ip}\nNew Status: {status}")
#     idp_ips.update_many({"ip": node_ip}, {"$set": {"status": status}})


 # RabbitMQ communication for Falcon web server


from rabbitmq.config_rabbitmq import configurations
import uuid
import json
import pika
from mongodb.mongo_config import *


credentials = pika.PlainCredentials(
    username=configurations["user"], password=configurations["password"], 
    erase_on_connect=True
)
parameters = pika.ConnectionParameters(
    host=configurations["host"], port=configurations["port"], 
    virtual_host=configurations["vhost"], credentials=credentials
)

class RequestConnection: 
    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        queue_result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = queue_result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue, on_message_callback=self.on_response, 
            auto_ack=True
        )

        self.corr_id = str(uuid.uuid4())
        self.properties = pika.BasicProperties(
            reply_to=self.callback_queue, correlation_id=self.corr_id
        )
        
        self.response = None
    

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body.decode())


def request(node_ip, command, argument, argument2=None, argument3=None):
    request = RequestConnection()
    
    message = {"command": command, "argument": argument}
    if argument2:
        message["argument2"] = argument2
    if argument3:
        message["argument3"] = argument3
    message = json.dumps(message)
    

    request.channel.queue_declare(queue=node_ip)
    request.channel.basic_publish(
        exchange="", routing_key=node_ip, body=message,
        properties=request.properties
    )

    request.connection.process_data_events(time_limit=None)
    request.connection.close()

    return request.response


def verify(node_ip, access_token):
    access_token = json.dumps(access_token)
    verification_response = request(node_ip, "verify", access_token)

    if verification_response["success"] == True:
        update_database(node_ip, "verified")
        print(f" [x] {node_ip}: Verified connection.")

    else:
        print(f" [x] {node_ip}: ERROR - Failed to verify connection.")
        # TODO: handle failed verification


def list_directory(node_ip, directory):
    list_response = request(node_ip, "list", directory)

    if list_response["success"] == True:
        print(f" [x] {node_ip}: Received file list for {directory}.")
        return list_response["files"]
    
    else:
        print(f" [x] {node_ip}: ERROR - Failed to list directory.")
        # TODO: handle failed list

        files = {
            "DATA_TYPE": "file_list",
            "path": directory,
            "DATA": []
        }
        return files


def transfer(receiver_ip, receiver_directory, sender_ip, sender_file_list):
    max_receivers = 20
    # if receiver_ip.num_receivers >= max_receivers: TODO Colin
        # print(f" [x] {receiver_ip}: ERROR - Maximum number of receivers active.")
        # TODO: handle failed receiver startup
        # return

    max_senders = 20
    # if sender_ip.num_senders >= max_senders: TODO Colin
        # print(f" [x] {sender_ip}: ERROR - Maximum number of senders active.")
        # TODO: handle failed sender startup
        # return
    
    # increment receiver_ip.num_receivers TODO Colin 
    # increment sender_ip.num_senders TODO Colin

    sender_files = ",".join(sender_file_list)
    receive_response = request(receiver_ip, "receive", receiver_directory, 
        sender_ip, sender_files
    )

    if receive_response["success"] == True:
        print(f" [x] {receiver_ip}: Falcon receiver is now active.")
        receiver_port = receive_response["port"]
        send_response = request(sender_ip, "send", receiver_ip, 
            receiver_port, sender_files
        )

        if send_response["success"] == True:
            # TODO: handle successful send (confirm success with receiver node)
            print(f" [x] {sender_ip}: Completed file transfer to {receiver_ip}.")

        else:
            print(f" [x] {sender_ip}: ERROR - Failed to send files to {receiver_ip}.")
            # TODO: handle failed send (kill Falcon receiver)

    else:
        print(f" [x] {receiver_ip}: ERROR - Failed to start Falcon receiver.")
        # TODO: handle failed receiver startup

    # decrement receiver_ip.num_receivers TODO Colin
    # decrement sender_ip.num_senders TODO Colin


def manage_connections():
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    connection_queue = "connections"
    channel.queue_declare(queue=connection_queue)
    channel.basic_consume(
        queue=connection_queue, on_message_callback=on_connection, 
        auto_ack=True
    )
    print(" [x] Waiting for status updates from Falcon nodes...")
    channel.start_consuming()

    # TODO: close connection (https://gist.github.com/josephernest/77fdb0012b72ebdf4c9d19d6256a1119)


def on_connection(ch, method, props, body):
    status_message = json.loads(body.decode())
    update_database(status_message["ip"], status_message["status"])
    print(f" [x] {status_message['ip']}: Node is {status_message['status']}.")


def update_database(node_ip: str, status: str):
    # update status in database TODO Colin
    print(f"Updating: {node_ip}\nNew Status: {status}")
    idp_ips.update_many({"ip": node_ip}, {"$set": {"status": status}})