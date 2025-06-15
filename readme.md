 Multiplayer Number Guessing Game (TCP) by
Ayan Ali and  
Muhammad Faizan Ahmad 

Setup instructions:

In one terminal run :
python server.py

In separate terminals (or on different machines) run :
python client.py

change HOST = 'localhost'  in game_client.py to the IP address of the server (e.g. 192.168.1.100) if you are not running the server on the same machine.

 Gameplay Guide
1. Pre-Game Chat: After joining, players enter a chat room.
2. Any player can start the game by typing \start.
3.Or you can just type normal messages to chat with others before the game.

Starting the Game
Type \start to begin.
Choose a difficulty level each level has diffrent range for secrect number:
1: Easy (1–100)
2: Medium (1–150)
3: Hard (1–200)

The game will start for all players simultaneously.
And all rounds are synced .

Game Rounds
There are 3 rounds in one session of \start and after 3 rounds leaderboard is displayed.
1. Each round has a 30-second time limit.
2. Players guess numbers until someone guesses correctly (gets 10 points), or Time runs out.
4. Rounds start for all player at same time, and after the times up you have  to enter at least 1 value to end the round
6. After each round, the correct\secret number is shown.

Scoring
1. +10 points for guessing the correct number.
2. No penalty for wrong guesses.
3. Final leaderboard is displayed at the end of three rounds.

logs:
All of the logs are in the logs file game_log.txt.

>if you are not the host player of the game you have to enter the first guess
twice.

Usage Example
Terminal 1:

> python server.py

> [Server listening...]

Terminal 2 (Player 1):
> python client.py

> Welcome to the Guessing Game! Please enter your name: Alice

> Alice has joined the Chat room.

> \start

> Please select from level 1, 2, or 3: 1

> Game started at Level 1 by Alice!

>Round 1 begins! You have 30 seconds to guess.

Terminal 3 (Player 2):

> python client.py

> Welcome to the Guessing Game! Please enter your name: Bob

> Bob has joined the Chat room.

> Game started at Level 1 by Alice!

> Round 1 begins! You have 30 seconds to guess.

>22

>22

>Too low

Game:
> Round 1 started

> Enter your guess: 45

> Too high.

> Enter your guess: 23

> Alice guessed correctly! +10 points

[Leaderboard displayed]

