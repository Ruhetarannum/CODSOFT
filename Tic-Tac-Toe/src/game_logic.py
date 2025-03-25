# game_logic.py - Core game mechanics and AI algorithm

import random
import math

class TicTacToe:
    def __init__(self):
        # Initialize empty 3x3 board (represented as a list)
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.ai_difficulty = "unbeatable"  # Default difficulty

    def reset_board(self):
        """Reset the game board and winner"""
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def set_ai_difficulty(self, difficulty):
        """Set AI difficulty level"""
        self.ai_difficulty = difficulty

    def available_moves(self):
        """Return a list of available moves (indices where the board is empty)"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        """Return True if there are empty squares on the board"""
        return ' ' in self.board

    def num_empty_squares(self):
        """Return the number of empty squares on the board"""
        return self.board.count(' ')

    def make_move(self, square, letter):
        """Make a move on the board"""
        if self.board[square] == ' ':
            self.board[square] = letter
            # Check if this move results in a win
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        """Check if the last move resulted in a win"""
        
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # Check diagonals
        # Only need to check if the move is on a diagonal
        if square % 2 == 0:
            # Check main diagonal
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            # Check other diagonal
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        return False

    def get_winner_line(self):
        """Return the winning line positions if there's a winner"""
        # Check rows
        for i in range(3):
            if self.board[i*3] == self.board[i*3+1] == self.board[i*3+2] != ' ':
                return [(i*3), (i*3+1), (i*3+2)]
        
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                return [i, i+3, i+6]
        
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return [0, 4, 8]
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return [2, 4, 6]
        
        return None

class AIPlayer:
    def __init__(self, letter, opponent_letter):
        self.letter = letter
        self.opponent_letter = opponent_letter
    
    def get_move(self, game):
        """Determine the best move based on the AI difficulty"""
        if game.ai_difficulty == "easy":
            return self.get_easy_move(game)
        elif game.ai_difficulty == "medium":
            return self.get_medium_move(game)
        else:  # "unbeatable"
            return self.get_best_move(game)
    
    def get_easy_move(self, game):
        """Make a random move"""
        available_moves = game.available_moves()
        return random.choice(available_moves)
    
    def get_medium_move(self, game):
        """Make a smart move 60% of the time, random move 40% of the time"""
        if random.random() < 0.6:
            return self.get_best_move(game)
        else:
            return self.get_easy_move(game)
    
    def get_best_move(self, game):
        """Use minimax algorithm with alpha-beta pruning to find the best move"""
        if len(game.available_moves()) == 9:
            # If the board is empty, choose a random corner or center
            return random.choice([0, 2, 4, 6, 8])
        
        # Find the best move using minimax with alpha-beta pruning
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in game.available_moves():
            # Try this move
            game.board[move] = self.letter
            
            # Calculate score via minimax
            score = self.minimax(game, 0, False, alpha, beta)
            
            # Undo the move
            game.board[move] = ' '
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
        
        return best_move
    
    def minimax(self, game, depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning"""
        
        # Check terminal states
        available_moves = game.available_moves()
        
        # Check if the opponent has won
        if self.check_winner(game, self.opponent_letter):
            return -10 + depth
        
        # Check if the AI has won
        if self.check_winner(game, self.letter):
            return 10 - depth
        
        # Check if it's a draw
        if not available_moves:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for move in available_moves:
                # Try this move
                game.board[move] = self.letter
                
                # Calculate score via minimax
                score = self.minimax(game, depth + 1, False, alpha, beta)
                
                # Undo the move
                game.board[move] = ' '
                
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
                
            return best_score
        else:
            best_score = float('inf')
            for move in available_moves:
                # Try this move
                game.board[move] = self.opponent_letter
                
                # Calculate score via minimax
                score = self.minimax(game, depth + 1, True, alpha, beta)
                
                # Undo the move
                game.board[move] = ' '
                
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    break
                
            return best_score
    
    def check_winner(self, game, letter):
        """Check if the given letter has won the game"""
        # Check rows
        for i in range(3):
            if game.board[i*3] == game.board[i*3+1] == game.board[i*3+2] == letter:
                return True
        
        # Check columns
        for i in range(3):
            if game.board[i] == game.board[i+3] == game.board[i+6] == letter:
                return True
        
        # Check diagonals
        if game.board[0] == game.board[4] == game.board[8] == letter:
            return True
        if game.board[2] == game.board[4] == game.board[6] == letter:
            return True
        
        return False