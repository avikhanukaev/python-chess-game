# python-chess-game
My first game written in Python and using the PyGame library. The main purpose of this game is to practice and learn game development and software engineering with PyGame.

#How to play?
First of all, in order to run the game, it is required to install the pygame development library. It can be done using the 'pip install pygame' library. After you have downloaded and installed the pygame library, you can run the game with 'python3.5 main.py' command.

#Levels
Currently there are three levels you can play with:
  (1) 'EASY' - Actually a dummy player. 
  (2) 'MEDIUM' - It is a bit challenging player. It can see into 4 future steps and choose the best step with the minimax algorithm.
  (3) 'HARD' - The idea behind this player is to look and compute the best move as far to future as possible. 

Note that currently the game is implemented with a regular minimax algorithm which is good and fast for the first two levels (easy and medium). However, the regular minimax algorithm is not so fast for the hard level. In future the computation will be advanced and algorithm that will be used is the alpha-beta version of minimax algorithm. It will increase the performance and speed of 'HARD' player.

#How change level?
In main.py there is main() function. Inside that function there is row that looks like - 
  game = Game(Difficulties['EASY'], Colors['WHITE'], Colors['BLACK'])
Now, to change the level you should change the Difficulties[''] parameter to 'EASY', 'MEDIUM' or 'HARD'. 
 
#Future plans and missions:
1) Implement the alpha-beta version of minimax algorithm to increase the AI performance.
2) Implement moves database for openings and end games to increase the AI performance.
3) Code review and improvements, especially within the GameTerminal.py file. 
