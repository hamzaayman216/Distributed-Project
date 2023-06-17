import socket
import concurrent.futures
import random
import time
import threading
from pymongo.mongo_client import MongoClient
from queue import Queue

uri = "mongodb+srv://wepres:WKftmGIEZ0PibRdZ@cargamecluster.wn2wpql.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)

# Access the databases
db1 = client['Game']
p1 = db1['player1']
p2 = db1['player2']
c = db1['chat']


db2 = client['GameRep']
p1Rep = db2['player1Rep']
p2Rep = db2['player2Rep']
cRep = db2['chatRep']
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set the IP address and port number
ip_address = 'localhost'
port = 6666

# Bind the socket to the IP address and port number
server_socket.bind((ip_address, port))

# Listen for incoming connections
server_socket.listen(5)

clients = []
max_clients = 3  # Set the maximum number of clients to 3
enemy_car_x_positions = [35, 180, 325, 470]
player_names = []
data_list = []

#--------------------------------------------------------------------------------
# Get the list of collections in the database
collections = db1.list_collection_names()

# Clear data in each collection
for collection_name in collections:
    collection = db1[collection_name]
    collection.delete_many({})
    print(f"Cleared data in collection: {collection_name}")

player1 = {
    "name": "",
    "x_position": 0,
    "y_position": 0,
    "game_over": False
}
player2 = {
    "name": "",
    "x_position": 0,
    "y_position": 0,
    "game_over": False
}
doc = {"data": ""}
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
# Get the list of collections in the database
collectionsRep = db2.list_collection_names()

# Clear data in each collection
for collection_name in collectionsRep:
    collectionRep = db2[collection_name]
    collectionRep.delete_many({})
    print(f"Cleared data in collection: {collection_name}")

player1Rep = {
    "name": "",
    "x_position": 0,
    "y_position": 0,
    "game_over": False
}
player2Rep = {
    "name": "",
    "x_position": 0,
    "y_position": 0,
    "game_over": False
}
docRep = {"data": ""}
#--------------------------------------------------------------------------------

prev_data = {}
last_data_time = {}
score = {}
signal = False
allowed = False
full_names = True
position = False

p1.insert_one(player1)
p2.insert_one(player2)
c.insert_one(doc)


p1Rep.insert_one(player1Rep)
p2Rep.insert_one(player2Rep)
cRep.insert_one(docRep)


# Create a thread pool with a maximum number of worker threads
executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_clients)

# Create a queue to store data that needs to be written to the databases
database_queue = Queue()


def write_to_databases():
    global data_list, prev_data
    while True:
        # Get the next item from the queue. This call will block until there is an item available
        # data = database_queue.get()

        # Here, you need to process the data into the format that you want to store in the databases
        # For this example, let's assume that you want to store it as a string
        # data_str = data.decode()
        # print(data_str)
        #print(player_names[0])
        #print(player_names[1])

        for data in data_list:

            print(data)
            server_status = db1.command("serverStatus")
            print("yo")
            print(server_status)

            if len(server_status) > 0:
                print("arrived")
                if data.startswith('m'):
                    c.insert_one(data[1:])
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
                        p1Rep.update_one(
                            {},
                            {"$set": {
                                "name": f"{split_data[0]}",
                                "x_position": int(split_data[1].split("&")[0]),
                                "y_position": int(split_data[1].split("&")[1]),
                                "game_over": boolean_value
                            }}
                        )
                        print("done i guess")
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
                        p2Rep.update_one(
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
            else:
                pass

            # # Indicate that the task is done. This is necessary when using Queue
            # database_queue.task_done()

        # data_list.clear()


def handle_client(client_socket):
    global prev_data, signal, allowed, full_names, position, data_list

    # Receive the player's name
    player_name = client_socket.recv(2048).decode()
    player_names.append(player_name)
    print(player_name)
    print(player_names)

    # Initialize the previous data, last data time and score for this player
    prev_data[player_name] = None
    last_data_time[player_name] = time.time()

    if full_names:
        if len(player_names) == 2:
            send_player_names()
            time.sleep(3)
            full_names = False
            position = True
            # signal = True

    if position:
        i = 0
        if len(clients) == 2:
            for client in clients:
                client.send(str(enemy_car_x_positions[i]).encode())
                i += 1
        time.sleep(1)
        position = False
        signal = True

    if signal:
        if len(clients) == 2:
            for client in clients:
                client.sendall(b"1")
        signal = False
        # allowed = True

    while True:
        # Receive data from the client
        data = client_socket.recv(2048)

        if data != prev_data[player_name]:
            # Split received data into a list of strings
            data_list = data.decode().split(",")

        # Check if data starts with 's' by decoding only the first byte
        if data[:1].decode() == 's':
            # If it's 's', decode the rest of the data
            data_str = data[1:].decode()

            # Extract the player name and score from the data
            name, sc = data_str.split(':')
            sc = int(sc)

            # Update the score for this player
            score[name] = sc

            if sc > 3000:
                if len(clients) > 1:
                    for client in clients:
                        if client != client_socket:
                            client.sendall("end".encode())
            while True:
                pass

        # Send data back to all other clients except the sender if there is more than one client connected
        elif len(clients) > 1 and data != prev_data[player_name]:
            for client in clients:
                if client != client_socket:
                    client.sendall(data)
                    # print(data)
                    prev_data[player_name] = data
        else:
            pass

        # Update the last data time for this player
        last_data_time[player_name] = time.time()

        # Close the connection if no data is received
        if not data:
            del clients[player_name]  # Remove the client from the list of clients
            print(f"{player_name} disconnected.")
            client_socket.close()
            break

        # Check if any player has stopped sending data
        for name, last_time in last_data_time.items():
            if time.time() - last_time > 20:  # Set a threshold of 10 seconds
                print(f"{name} has stopped sending data and probably disconnected.")


def start_enemy():
    # Start a separate thread to send enemy car data
    enemy_car_thread = threading.Thread(target=send_enemy_car_data)
    enemy_car_thread.start()


def send_player_names():
    # Convert the list to a string
    str_player_names = ', '.join(player_names)
    # Convert the string to bytes and send to all clients
    for client in clients:
        client.sendall(str_player_names.encode())


def send_enemy_car_data():
    while True:
        time.sleep(2)
        x_position = random.choice(enemy_car_x_positions)
        # x_position = 325
        message = f"{str(x_position)}e"
        for client in clients:
            client.sendall(message.encode())


has_started_enemy = False
db_init = False
dataBaseCounter=0
while True:
    dataBaseCounter += 1
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

    # if len(clients) == 1 and not db_init:
    #     # In your main loop, start the write_to_databases function in a new thread
    #     executor.submit(write_to_databases)
    #     db_init = True

    if dataBaseCounter % 2000 and len(clients) > 0:
        executor.submit(write_to_databases)
        #db_init = True
    # Start enemy car data thread after all clients have connected
    if len(clients) == max_clients and not has_started_enemy:
        start_enemy()
        has_started_enemy = True  # Update the flag
