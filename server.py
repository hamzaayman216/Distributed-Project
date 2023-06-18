import json
import socket
import concurrent.futures
import time
import threading
from pymongo.mongo_client import MongoClient
from queue import Queue

data_queue = Queue()

# Open the JSON file
with open('server_data.json', 'r') as file:
    # Load the JSON data
    data = json.load(file)

uri = data['data_base_url']
# Create a new client and connect to the server
client = MongoClient(uri, tlsAllowInvalidCertificates=True)

db1 = client['Game']
p1 = db1['player1']
p2 = db1['player2']
p3 = db1['player3']
c = db1['chat']

db2 = client['GameRep']
p1Rep = db2['player1Rep']
p2Rep = db2['player2Rep']
p3Rep = db2['player3Rep']
cRep = db2['chatRep']


# Get the list of collections in the database
collections = db1.list_collection_names()

# Clear data in each collection
for collection_name in collections:
    collection = db1[collection_name]
    collection.delete_many({})
    print(f"Cleared data in collection: {collection_name}")

player1 = {
    "name": "no name",
    "x_position": 0,
    "y_position": 0,
    "game_over": False,
    "score": 0
}
player2 = {
    "name": "no name",
    "x_position": 0,
    "y_position": 0,
    "game_over": False,
    "score": 0
}
player3 = {
    "name": "no name",
    "x_position": 0,
    "y_position": 0,
    "game_over": False,
    "score": 0
}
default_data_chat1 = {
    'message': 'Default Message'
}

collectionsRep = db2.list_collection_names()

for collection_name in collectionsRep:
    collectionRep = db2[collection_name]
    collectionRep.delete_many({})
    print(f"Cleared data in collection: {collection_name}")

player1Rep = {
    "name": "no name",
    "x_position": 0,
    "y_position": 0,
    "game_over": False,
    "score": 0
}
player2Rep = {
    "name": "no name",
    "x_position": 0,
    "y_position": 0,
    "game_over": False,
    "score": 0
}
player3Rep = {
    "name": "no name",
    "x_position": 0,
    "y_position": 0,
    "game_over": False,
    "score": 0
}
default_data_chat2 = {
    'message': 'Default Message'
}

p1.insert_one(player1)
p2.insert_one(player2)
p3.insert_one(player3)
c.insert_one(default_data_chat1)

p1Rep.insert_one(player1Rep)
p2Rep.insert_one(player2Rep)
p3Rep.insert_one(player3Rep)
cRep.insert_one(default_data_chat2)
#--------------------------------------------------------------------------------

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port number
ip_address = data['ip']
port = data['port']

# Bind the socket to the IP address and port number
server_socket.bind((ip_address, port))

# Listen for incoming connections
server_socket.listen(5)

clients = []
max_clients = 3  # Set the maximum number of clients to 3
enemy_car_x_positions = [35, 180, 325, 470]
player_names = []
data_list = []
prev_db_data = ""
prev_data = {}
last_data_time = {}
score = {}
signal = False
allowed = False
full_names = True
position = False
has_started_enemy = True
db_init = True

# Create a thread pool with a maximum number of worker threads
executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_clients+1)

def write_to_databases():
    global data_list
    # time.sleep(5)
    while True:

        data = data_queue.get()

        server_status1 = db1.command("serverStatus")

        if len(server_status1) > 0:
            if data.endswith(':m'):
                document = {
                    'message': f'{data[:-2]}'
                }
                c.insert_one(document)
            elif data.startswith('x'):
                split_data = data.split(":")
                if split_data[0][1:] == player_names[0]:
                    p1.update_one({}, {"$set": {"score": int(split_data[1])}})
                elif split_data[0][1:] == player_names[1]:
                    p2.update_one({}, {"$set": {"score": int(split_data[1])}})
                elif split_data[0][1:] == player_names[2]:
                    p3.update_one({}, {"$set": {"score": int(split_data[1])}})
            elif data.endswith('p'):
                # Splitting the string by ":"
                split_data = data.split(":")

                if split_data[0] == player_names[0]:
                    value3 = bool(split_data[2])
                    boolean_value = (value3 == "True")
                    p1.update_one(
                        {},
                        {"$set": {
                            "name": f"{split_data[0]}",
                            "x_position": int(split_data[1].split("&")[0]),
                            "y_position": int(split_data[1].split("&")[1]),
                            "game_over": boolean_value
                        }}
                    )
                elif split_data[0] == player_names[1]:
                    value3 = bool(split_data[2])
                    boolean_value = (value3 == "True")
                    p2.update_one(
                        {},
                        {"$set": {
                            "name": split_data[0],
                            "x_position": int(split_data[1].split("&")[0]),
                            "y_position": int(split_data[1].split("&")[1]),
                            "game_over": boolean_value
                        }}
                    )
                elif split_data[0] == player_names[2]:
                    value3 = bool(split_data[2])
                    boolean_value = (value3 == "True")
                    p3.update_one(
                        {},
                        {"$set": {
                            "name": split_data[0],
                            "x_position": int(split_data[1].split("&")[0]),
                            "y_position": int(split_data[1].split("&")[1]),
                            "game_over": boolean_value
                        }}
                    )
            else:
                pass

        server_status2 = db2.command("serverStatus")

        if len(server_status2) > 0:
            if data.endswith(':m'):
                document = {
                    'message': f'{data[:-2]}'
                }
                cRep.insert_one(document)
            elif data.startswith('x'):
                split_data = data.split(":")
                if split_data[0][1:] == player_names[0]:
                    p1Rep.update_one({}, {"$set": {"score": int(split_data[1])}})
                elif split_data[0][1:] == player_names[1]:
                    p2Rep.update_one({}, {"$set": {"score": int(split_data[1])}})
                elif split_data[0][1:] == player_names[2]:
                    p3Rep.update_one({}, {"$set": {"score": int(split_data[1])}})
            elif data.endswith('p'):
                # Splitting the string by ":"
                split_data = data.split(":")

                if split_data[0] == player_names[0]:
                    value3 = bool(split_data[2])
                    boolean_value = (value3 == "True")
                    p1Rep.update_one(
                        {},
                        {"$set": {
                            "name": f"{split_data[0]}",
                            "x_position": int(split_data[1].split("&")[0]),
                            "y_position": int(split_data[1].split("&")[1]),
                            "game_over": boolean_value
                        }}
                    )
                elif split_data[0] == player_names[1]:
                    value3 = bool(split_data[2])
                    boolean_value = (value3 == "True")
                    p2Rep.update_one(
                        {},
                        {"$set": {
                            "name": split_data[0],
                            "x_position": int(split_data[1].split("&")[0]),
                            "y_position": int(split_data[1].split("&")[1]),
                            "game_over": boolean_value
                        }}
                    )
                elif split_data[0] == player_names[2]:
                    value3 = bool(split_data[2])
                    boolean_value = (value3 == "True")
                    p3Rep.update_one(
                        {},
                        {"$set": {
                            "name": split_data[0],
                            "x_position": int(split_data[1].split("&")[0]),
                            "y_position": int(split_data[1].split("&")[1]),
                            "game_over": boolean_value
                        }}
                    )
            else:
                pass

        data_queue.task_done()


def handle_client(client_socket):
    global prev_data, signal, player_names, allowed, full_names, position, has_started_enemy, db_init, data_list

    # Receive the player's name
    player_name = client_socket.recv(2048).decode()
    if player_name != "":
        player_names.append(player_name)
        print(player_names)
    else:
        pass

    # Initialize the previous data, last data time and score for this player
    prev_data[player_name] = None
    last_data_time[player_name] = time.time()

    if full_names:
        if len(player_names) == 3:
            send_player_names()
            time.sleep(3)
            full_names = False
            position = True
            # signal = True

    if position:
        i = 0
        if len(clients) == 3:
            for client in clients:
                client.sendall(str(enemy_car_x_positions[i]).encode())
                i += 1
        time.sleep(1)
        position = False
        signal = True

    if signal:
        if len(clients) == 3:
            for client in clients:
                client.sendall(b"1")
        signal = False
        db_init = False

    if len(clients) == 3 and not db_init:
        database_thread = threading.Thread(target=write_to_databases)
        database_thread.start()
        print("Database started!")
        db_init = True

    while True:
        # Receive data from the client
        data = client_socket.recv(2048)

        data_queue.put(data.decode())

        # Check if data starts with 's' by decoding only the first byte
        if data.decode()[0] == 's':
            # If it's 's', decode the rest of the data
            data_str = data[1:].decode()

            # Extract the player name and score from the data
            name, sc = data_str.split(':')
            sc = int(sc)
            print(sc)

            # Update the score for this player
            score[name] = sc

            if sc > 3000:
                if len(clients) > 1:
                    for client in clients:
                        if client != client_socket:
                            client.sendall("end".encode())
                            print("i am here because i got here")

        # Send data back to all other clients except the sender if there is more than one client connected
        elif len(clients) > 1:
            for client in clients:
                if client != client_socket:
                    client.sendall(data)
                    # prev_data[player_name] = data
        else:
            pass


def send_player_names():
    # Convert the list to a string
    str_player_names = ', '.join(player_names)
    # Convert the string to bytes and send to all clients
    for client in clients:
        client.sendall(str_player_names.encode())


while True:
    print("Waiting for connections...")
    # Wait for a connection
    client_socket, addr = server_socket.accept()

    # Check if maximum number of clients is reached
    if len(clients) < max_clients:
        # Add the new client to the list of clients
        clients.append(client_socket)
        print(f"Client {addr} connected.")

        # Submit a new task to the thread pool to handle the client
        executor.submit(handle_client, client_socket)

    else:
        # Reject new connection
        print(f"Connection from {addr} rejected: maximum number of clients reached.")
        client_socket.close()
