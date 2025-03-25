# Tic-Tac-Toe with AI

A Python implementation of the classic Tic-Tac-Toe game with an unbeatable AI opponent using the Minimax algorithm with Alpha-Beta pruning.

## Features

- Graphical user interface built with Tkinter
- Three AI difficulty levels:
  - Easy: Makes random moves
  - Medium: Makes optimal moves 60% of the time
  - Unbeatable: Never loses (uses Minimax with Alpha-Beta pruning)
- Game statistics tracking
- Visual feedback for winning combinations
- Clean and intuitive user interface
- Attractive visual design with custom icon

## Installation

1. Clone this repository or download the source code
2. Make sure you have Python 3.x installed
3. Install the required dependencies:
   
   pip install -r requirements.txt
   

## Requirements

- Python 3.x
- Tkinter (included in standard Python installation)
- Pillow (for image processing)

## How to Play

1. Select the AI difficulty level using the radio buttons
2. Click on any empty cell to make your move
3. Try to get three X's in a row, column, or diagonal
4. Use the "New Game" button to start a new game
5. Use the "Reset Scores" button to reset the statistics

## Project Structure


Tic-Tac-Toe/
│
├── src/                 # Source code directory
│   ├── main.py          # Entry point that connects frontend and backend
│   ├── game_logic.py    # Core game mechanics and AI algorithm
│   ├── gui.py           # Frontend interface using Tkinter
│   └── assets/          # Game assets
│       └── icon.png     # Game icon
├── requirements.txt     # Project dependencies
└── README.md            # This documentation file


## Algorithm

The AI uses the Minimax algorithm with Alpha-Beta pruning to determine the optimal move. This algorithm:

1. Explores all possible game states
2. Assigns scores to terminal states (win, loss, draw)
3. Works backward to determine the best move
4. Uses Alpha-Beta pruning to optimize the search process

## Usage

Run the game using:


python src/main.py


## Development

This project was developed as part of the CodSoft internship program.
