# python-chess-game
My first game written in Python and using the PyGame library. The main purpose of this game is to practice and learn game development and software engineering with PyGame.

## Getting Started

### Prerequisites
In order to run the game or participate in its developemnts one should have the PyGame game development library. One should install it using the following command: 
```
pip install pygame
``` 

### Run
After you have downloaded and installed the pygame library, you can run the game with
```
python3.5 main.py
```

## About The Game

### Difficulty 
Currently there are three levels you can play with:

1) 'EASY' - Actually a dummy player. 
2) 'MEDIUM' - It is a bit challenging player. It can see into 4 future steps and choose the best step with the minimax algorithm.
3) 'HARD' - The idea behind this player is to look and compute the best move as far to future as possible. 

Note that currently the game is implemented with a regular minimax algorithm which is good and fast for the first two levels (easy and medium). However, the regular minimax algorithm is not so fast for the hard level. In future the computation will be advanced and algorithm that will be used is the alpha-beta version of minimax algorithm. It will increase the performance and speed of 'HARD' player.

### How change level?
In main.py there is main() function. Inside that function there is row that looks like -
``` 
game = Game(Difficulties['EASY'], Colors['WHITE'], Colors['BLACK'])
```
To change the level of difficulty you should change the ```Difficulties['']``` parameter to 'EASY', 'MEDIUM' or 'HARD'.

### Important Notes 

It is worthy to note that this version of game is incomplete. First of all, it does not have the option to castle - this will be added in next version of the game. Second, for one to win a game he must <b>eat</b> opponents king. There is still no validation of check-mate to stop the game without eating king. 
 
## Future Plans
1) Implement the alpha-beta version of minimax algorithm to increase the AI performance.
2) Implement moves database for openings and end games to increase the AI performance.
3) Code review and improvements, especially within the GameTerminal.py file.
4) Add option for user to play with black.
5) Add castle moves.
6) Implement the `save log` functionality. 

## Project Architecture

### Project Structure

* ```main.py``` - An entry point of the game. 
* ```GameObjectInterface.py``` - The interface for ```Game``` object. This is used especially when there are some outer manipulations on the `Game` object. For example, when pressing button on games terminal affect and manipulate the game. 
* ```Game.py``` - This file contains the main game object. The `Game` object is responsible for running and manage whole game. In our project, there is only one instance of `Game` object.  
* `Board.py` - This file contains three classes. 
    * `BoardNode` - Which represent and handles each cell on the chess board.
    * `Board` - The <b>logical</b> board. The logical board is controller that conrols and manipulates the board of the game. Each operation that is done and performed in game may reflect on the board and manipulate it.   
    * `DisplayBoard` - The <b>graphical</b> board. This is the view that is responsible to display board and moves on the screen. It is connected the the logical board. 
* `GameTerminal.py` - File contains the `GameTerminal` class which is responsible for the side bar logger and menu. 
* `Move.py` - Contains the `Move` class that represents each move made by user or computer on the board.
* `ComputerAI.py` - Contains the `ComputerAI` class that is responsible for the computer player. Currently, the algorithm that is used is the regular minimax algorithm. 
* `Button.py` - Implements the functionality of buttons. 
* `TextHandler.py` - Handles the visualization of text on screen.
* `ButtonFunctionality.py` - Implements the functionality of buttons that are on the terminal.
* `Pieces.py` - Contains a helper class `Pieces` that deals with loading and handling the graphical issues of pieces. 
* `Consts.py` - Contains all consts values that is used in different parts of projects. 

## Current Version

* v1.0.0

## Built With

* [Python](https://www.python.org/) - The Python programming language.
* [pygame](https://www.pygame.org/news) - Python library for multimedia applications.

## Authors

* **Avraham Khanukaev** - *Initial work* - [Avraham Khanukaev](https://github.com/avikhanukaev)