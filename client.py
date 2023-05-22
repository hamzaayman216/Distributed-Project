
import socket
from cargame import main

s = socket.socket()
host = '127.0.0.1'  # Replace with the server's IP address
port = 6667

s.connect((host, port))

# Call the main game loop or relevant method in your Player class
main()

while True:
    # Receive and decode the game state from the server
    game_state = s.recv(1024).decode()

    # Display the game state
    print("Game State:", game_state)

    response = "Car game finished."  # Set the response message
    s.send(str.encode(response))  # Send the response back to the server

s.close()


