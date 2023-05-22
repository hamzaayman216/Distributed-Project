
import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []
game_state = {"car_positions": []}  # Initial game state with empty car positions
game_state_lock = threading.Lock()  # Lock for synchronizing access to game_state


# Create a Socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = '127.0.0.1'
        port = 6667
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established: " + address[0])

            # Send initial game state to the connected client
            with game_state_lock:
                conn.send(str.encode(str(game_state)))

            # Create a thread for each connected client to handle game state updates
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.daemon = True
            client_thread.start()

        except:
            print("Error accepting connections")


# Handle game state updates for a connected client
def handle_client(conn):
    while True:
        try:
            # Receive commands from the client if needed
            # command = conn.recv(1024).decode()

            # Update the game state
            with game_state_lock:
                # Update the car positions in the game state
                game_state["car_positions"] = []  # Replace with your logic to update the car positions

            # Send the updated game state to the client
            conn.send(str.encode(str(game_state)))

            # Sleep for a short duration to control the rate of game state updates
            # Adjust this value as per your requirements
            time.sleep(0.1)

        except:
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            pass  # No need to start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
