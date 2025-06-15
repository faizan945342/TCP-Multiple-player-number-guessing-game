import socket
import threading
import random
import time

# Game configuration
MAX_GUESSES = 100
GUESS_TIME_LIMIT = 30  
ROUNDS = 3

HOST = 'localhost'
PORT = 12345
clients = {} 
player_scores = {}
round_number = 0
game_active = False

def log_game_event(event):
    with open("game_log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()}: {event}\n")

# Function to broadcast messages to all connected clients
def broadcast_message(message):
    for client_socket in clients.keys():
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            # Handle client disconnection
            clients.pop(client_socket, None)

# Function to handle each client connection
def handle_client(client_socket, client_address):
    global round_number, game_active
    client_socket.send("Welcome to the Guessing Game! Please enter your name: ".encode('utf-8'))
    name = client_socket.recv(1024).decode('utf-8')
    
    if name not in player_scores:
        player_scores[name] = 0
        clients[client_socket] = name
    
    log_game_event(f"{name} connected from {client_address}")
    chat_room(client_socket, name)

def chat_room(client_socket, name):
    global round_number, game_active
    if game_active == False :
        broadcast_message(f"{name} has joined the Chat room.")
        client_socket.send("Type '\\start' to start the game. Or you can just chat normally.".encode('utf-8'))
        
        while game_active == False:
                message = client_socket.recv(1024).decode('utf-8')
                
                if message.lower() == "\\start" and round_number == 0 and not game_active:
                    round_number += 1
                    client_socket.send("Please select from level 1, 2, or 3.".encode('utf-8'))
                    level = client_socket.recv(1024).decode('utf-8')
                    return start_game(level,name)
                
                elif message.lower() == "\\start" and game_active:
                    client_socket.send("The game is already in progress.".encode('utf-8'))
                else:
                    if not game_active :
                        if message:
                            broadcast_message(f"{name}: {message}")
                            log_game_event(f"{name} (chat): {message}")

    
def start_game(level, host_name):
    global game_active, round_number
    game_active = True
    round_number = 1

    level_ranges = {"1": 100, "2": 150, "3": 200}
    maxnum = level_ranges.get(level, 100)

    log_game_event(f"Game started by {host_name} at level {level}. Max number: {maxnum}")
    broadcast_message(f"\n🎮 Game started at Level {level} by {host_name}!\n")

    while round_number <= 3:
        secret_number = random.randint(1, maxnum)
        broadcast_message(f"\nRound {round_number} begins! You have {GUESS_TIME_LIMIT} seconds to guess.\n")

        threads = []
        for client_socket in clients.keys():
            name = clients[client_socket]
            thread = threading.Thread(target=play_round, args=(client_socket, name, secret_number))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        round_number += 1

    broadcast_message(f"\n Game over! Final leaderboard:\n{generate_leaderboard()}")
    game_active = False
    log_game_event("Game ended.\n")
    game_active = False
    round_number = 0
    # chat_room()

def play_round(client_socket, name, secret_number):
    try:
        # client_socket.send(f"Round {round_number}\n".encode('utf-8'))
        start_time = time.time()
        guessed_correctly = False

        while time.time() - start_time < GUESS_TIME_LIMIT:
            client_socket.send("Enter your guess: ".encode('utf-8'))
            try:
                guess = int(client_socket.recv(1024).decode('utf-8'))
            except:
                client_socket.send("Invalid input. Please enter a number.".encode('utf-8'))
                continue

            if guess == secret_number:
                if not guessed_correctly:
                    player_scores[name] += 10
                    guessed_correctly = True
                    broadcast_message(f"{name} guessed the number! +10 points.")
                    log_game_event(f"{name} guessed correctly. Secret was {secret_number}.")
                break
            elif guess < secret_number:
                client_socket.send("Too low.\n".encode('utf-8'))
            else:
                client_socket.send("Too high.\n".encode('utf-8'))

        if not guessed_correctly:
            client_socket.send(f"\n Time's up! The correct number was {secret_number}.\n".encode('utf-8'))
            log_game_event(f"{name} failed to guess. Secret was {secret_number}.")
    except Exception as e:
        log_game_event(f"Error during play_round for {name}: {e}")
        
    
    

def generate_leaderboard():
    if not player_scores:
        return "Leaderboard is empty."
    
    sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard = "\n".join([f"{name}: {score} points" for name, score in sorted_players])
    return leaderboard

# Server socket setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server started on {HOST}:{PORT}")

def accept_clients():
    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    accept_clients()
