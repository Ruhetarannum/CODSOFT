# main.py - Entry point that connects frontend and backend

import tkinter as tk
from game_logic import TicTacToe, AIPlayer
from gui import TicTacToeGUI

def main():
    """Main function to run the Tic-Tac-Toe game"""
    # Create the game logic
    game = TicTacToe()
    
    # Create the AI player
    ai_player = AIPlayer('O', 'X')
    
    # Create the GUI
    root = tk.Tk()
    app = TicTacToeGUI(root, game, ai_player)
    
    # Start the game
    root.mainloop()

if __name__ == "__main__":
    main()