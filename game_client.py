import socket
import threading

# Server configurationion
# use the  ip of the server 
HOST = 'localhost'
PORT = 12345

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connection lost.")
            break

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Start a thread to listen to messages constantly
threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

def start_game():
    while True:
        # Take user input and send it to the server
        user_input = input(">")
        if user_input:
            client.send(user_input.encode('utf-8'))

start_game()
