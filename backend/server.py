import json
import pika
import datetime
from bson.json_util import dumps, loads

from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from mongodb.mongo_config import *
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from flask_cors import CORS, cross_origin
from flask_session import Session


#------------------CILogon OIDC---------------------------------------------------------------------------#
from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata, ProviderMetadata
from flask_pyoidc.user_session import UserSession
#---------------------------------------------------------------------------------------------------------#

from rabbitmq import rmq_server as rmq
from threading import Thread

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.config.update(
    SECRET_KEY=env.get("APP_SECRET_KEY"),
    OIDC_REDIRECT_URI=env.get("OIDC_REDIRECT_URI"),
    SESSION_TYPE="filesystem",
    SESSION_PERMANENT=False
)
CORS(app, resources={r"/*":{'origins':"*"}})
Session(app)

# Static Client/Provider Registration
client_metadata = ClientMetadata(
    client_id=env.get("CILOGON_CLIENT_ID"),
    client_secret=env.get("CILOGON_CLIENT_SECRET"),
    post_logout_redirect_uris=['https://localhost:3000/logout'])

provider_metadata = ProviderMetadata(
    issuer='https://cilogon.org',
    authorization_endpoint='https://cilogon.org/authorize',
    token_endpoint='https://cilogon.org/oauth2/token',
    introspection_endpoint='https://cilogon.org/oauth2/introspect',
    userinfo_endpoint='https://cilogon.org/oauth2/userinfo',
    #end_session_endpoint='https://idp.example.com/logout',
    jwks_uri='https://cilogon.org/oauth2/certs',
    registration_endpoint='https://cilogon.org/oauth2/register')

auth_params = {'scope': ['openid', 'profile', 'email', 'org.cilogon.userinfo']} # specify the scope to request

provider_config = ProviderConfiguration(
    provider_metadata=provider_metadata,
    client_metadata=client_metadata,
    auth_request_params=auth_params)

auth = OIDCAuthentication({
    'CILogon': provider_config,
    "Site1": provider_config,
    "Site2": provider_config
    }, app)


# Create thread to handle manage_connections
# Falcon WS listens to online Falcon Nodes on startup
daemon = Thread(
    target=rmq.manage_connections, daemon=True, name=f"manage_falcon_connections"
)
daemon.start()

@app.route("/get_user")
@cross_origin(supports_credentials=True)
def get_user():
    print(session)

    return jsonify({
        "user_info": session.get("user_info"),
        "site1_info": session.get("site1_info"),
        "site2_info": session.get("site2_info")
    })


@app.route("/login")
@auth.oidc_auth('CILogon')
def login():
    print("logging in!")

    session['user_info'] = {
        "full_name": session["userinfo"]["name"],
        "email": session["userinfo"]["email"],
        "idp_name": session["userinfo"]["idp_name"],
        "access_token": session["access_token"],
        "id_token_jwt": session["id_token_jwt"]
    }

    print(f'Logged in as {session["user_info"]["full_name"]}')
    print(session["user_info"])

    return redirect("http://localhost:8080/dashboard")


@app.route("/loginSite1")
@auth.oidc_auth('Site1')
def loginSite1():

    # retrieve IPs from mongoDB
    site1_ips = []
    for x in idp_ips.find({"idp": session["userinfo"]["idp_name"]}):
        site1_ips.append({
            "ip": x["ip"],
            "status": x["status"]
        })
    
    session['site1_info'] = {
        "full_name": session["userinfo"]["name"],
        "email": session["userinfo"]["email"],
        "idp_name": session["userinfo"]["idp_name"],
        "access_token": session["access_token"],
        "id_token_jwt": session["id_token_jwt"],
        "ips": site1_ips
    }
    print(f'Site 1 Info\n{session["site1_info"]}')

    return redirect("http://localhost:8080/dashboard")



@app.route("/loginSite2")
@auth.oidc_auth('Site2')
def loginSite2():

    # retrieve IPs from mongoDB
    site2_ips = []
    for x in idp_ips.find({"idp": session["userinfo"]["idp_name"]}):
        site2_ips.append({
            "ip": x["ip"],
            "status": x["status"]
        })

    session['site2_info'] = {
        "full_name": session["userinfo"]["name"],
        "email": session["userinfo"]["email"],
        "idp_name": session["userinfo"]["idp_name"],
        "access_token": session["access_token"],
        "id_token_jwt": session["id_token_jwt"],
        "ips": site2_ips
    }
    print(f'Site 2 Info\n{session["site2_info"]}')

    return redirect("http://localhost:8080/dashboard")

@app.route('/listFiles', methods=['POST'])
def listFiles():

    post_data = request.get_json()
    ip_addr = post_data['ip_addr']
    file_path = post_data['file_path']

    print(ip_addr)
    print(file_path)

    # Handle multiple users with different threads?
    # daemon = Thread(
    #     target=rmq.make_request, args=(site1_IP, "list", site1_path), 
    #     daemon=True, name=f"{site1_IP}_list_request"
    # )
    # daemon.start()

    # rmq.verify(ip_addr, payload)

    file_list = rmq.list_directory(ip_addr, file_path)
    print(file_list)

    return jsonify({
        "files": file_list["DATA"]
    })


@app.route("/logout")
@auth.oidc_logout
def logout():
    print("Logging OUT")
    session.clear()
    print(session)
    return redirect("http://localhost:8080/")


# @app.route("/account")
# def account():
#     print(session["user_info"])
#     print(session["site1_info"])
#     print(session["site2_info"])
#     return render_template(
#             "home.html",
#             name=session["user_info"]["full_name"],
#             email=session["user_info"]["email"],
#             affiliation=session["user_info"]["idp_name"],
#             site1_name=session["site1_info"]["full_name"],
#             site1_email=session["site1_info"]["email"],
#             site1_affiliation=session["site1_info"]["idp_name"],
#             site2_name=session["site2_info"]["full_name"],
#             site2_email=session["site2_info"]["email"],
#             site2_affiliation=session["site2_info"]["idp_name"],
#             page="Account"
#         )


# @app.route("/history")
# def history():
#     cursor = l_transfer_data.find({"user_email": session["userinfo"]["email"]}).sort("epochTime", -1)
#     list_cur = list(cursor)
#     return render_template(
#             "home.html",
#             session=session["userinfo"],
#             page="History",
#             transferData=list_cur
#         )


@app.route('/site1_ip', methods=['POST'])
def site1_ip():
    post_data = request.get_json()
    site1_ip = post_data['site1_IP']
    site1_access_token = post_data['site1_access_token']
    site1_id_token_jwt = post_data['site1_id_token_jwt']

    # verify ip_idp mapping and set session variables
    if idp_ips.count_documents({"ip": site1_ip}) != 0:
        print("Valid IP address")
        isValidIP = True
        # session["site1_info"]["valid_ip"] = True
        # session["site1_info"]["ip_address"] = site1_ip

        # Send id_token_jwt to Falcon Node for verification
        payload = {
            # "access_token": session["site1_info"]["access_token"],
            # "id_token_jwt": session["site1_info"]["id_token_jwt"]  
            "access_token": site1_access_token,
            "id_token_jwt": site1_id_token_jwt
        }
        daemon = Thread(
            target=rmq.verify, args=(site1_ip, payload), 
            daemon=True, name=f"{site1_ip}_send_jwt"
        )
        daemon.start()

    else:
        print("Invalid IP address")
        isValidIP = False    
        # session["site1_info"]["valid_ip"] = False
        # session["site1_info"]["ip_address"] = None


    return jsonify({'is_valid_ip': isValidIP})
    # return jsonify("hello")


@app.route('/site2_ip', methods=['POST'])
def site2_ip():
    post_data = request.get_json()
    site2_ip = post_data['site2_IP']
    site2_access_token = post_data['site2_access_token']
    site2_id_token_jwt = post_data['site2_id_token_jwt']

    # verify ip_idp mapping and set session variables
    if idp_ips.count_documents({"ip": site2_ip}) != 0:
        print("Valid IP address")
        isValidIP = True
        # session["site1_info"]["valid_ip"] = True
        # session["site1_info"]["ip_address"] = site1_ip

        # Send id_token_jwt to Falcon Node for verification
        payload = {
            # "access_token": session["site1_info"]["access_token"],
            # "id_token_jwt": session["site1_info"]["id_token_jwt"]  
            "access_token": site2_access_token,
            "id_token_jwt": site2_id_token_jwt
        }
        daemon = Thread(
            target=rmq.verify, args=(site2_ip, payload), 
            daemon=True, name=f"{site2_ip}_send_jwt"
        )
        daemon.start()

    else:
        print("Invalid IP address")
        isValidIP = False    
        # session["site1_info"]["valid_ip"] = False
        # session["site1_info"]["ip_address"] = None


    return jsonify({'is_valid_ip': isValidIP})
    # return jsonify("hello")


@app.route('/transferFiles', methods=['POST', 'GET'])
def transferFiles():

    post_data = request.get_json()
    srcIP = post_data['srcIP']
    destIP = post_data['destIP']
    sender_dir = post_data['sender_dir']
    dest_dir = post_data['dest_dir']
    user_name = post_data['user_name']
    user_email = post_data['user_email']
    user_affiliation = post_data['user_affiliation']

    sender_dir_list = []
    sender_dir_list.append(sender_dir)
    
    selectedFiles = post_data['selected_files']

    print("Sending transfer request ...")

    payload = {
        "sender_ip": srcIP,
        "receiver_ip": destIP,
        "dest_dir": dest_dir,
        # "file_list": selectedFiles
        "file_list": sender_dir_list
    }
    print(payload)
    # status = rmq.make_request(payload["sender_ip"], "transfer", payload["receiver_ip"], payload["file_list"])
    # rmq.transfer(payload["sender_ip"], payload["receiver_ip"], payload["file_list"])
    rmq.transfer(payload["receiver_ip"], payload["dest_dir"], payload["sender_ip"], payload["file_list"])

    # transfer should return status code
    status = "success"

    # add transfer job to MongoDB
    epochTime = datetime.datetime.now().timestamp()
    requestTime = datetime.datetime.now().strftime("%m/%d/%Y, %I:%M %p")

    post = {
        "full_name": user_name,
        "email": user_email,
        "idp_name": user_affiliation,
        "srcIP": srcIP,
        "srcDir": sender_dir,
        "destIP": destIP,
        "destDir": dest_dir,
        "selectedFiles": selectedFiles,
        "epochTime":  epochTime,
        "requestTime": requestTime,
        "completionTime": "12345 [temp val]",
        "transferDuration": "12345 [temp val]",
        "transferStatus": status
    }
    print(post)
    l_transfer_data.insert_one(post)

    return jsonify({
        'transfer_status': status,
        "transfer_details": payload
    })

@app.route('/getHistory', methods=['POST', 'GET'])
def getHistory():

    # temp var
    user_email = "cmartires@nevada.unr.edu"

    cursor = l_transfer_data.find({"email": user_email}).sort("epochTime", -1)
    list_cur = list(cursor)
    json_data = dumps(list_cur)
    return jsonify({
        "transferData": json_data
    })
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=env.get("PORT", 3000))