import tkinter as tk
from tkinter import ttk, messagebox, font
import time
import os
from PIL import Image, ImageTk  # You'll need to install Pillow: pip install Pillow

class TicTacToeGUI:
    def __init__(self, root, game_logic, ai_player):
        self.root = root
        self.game = game_logic
        self.ai = ai_player
        self.player_letter = 'X'
        self.ai_letter = 'O'
        self.game_active = True
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        
        # Define color scheme
        self.colors = {
            'bg': '#EAF0F6',            # Lighter blue-gray background
            'primary': '#3498DB',       # Blue for primary elements
            'secondary': '#2ECC71',     # Green for secondary elements
            'accent': '#9B59B6',        # Purple for accent elements
            'text': '#2C3E50',          # Dark blue-gray for text
            'warning': '#E74C3C',       # Red for warnings/errors
            'player_x': '#FF5722',      # Orange for player X
            'player_o': '#3F51B5',      # Indigo for player O
            'win_highlight': '#ABEBC6',  # Light green for win highlighting
            'board_bg': '#D6EAF8'       # Light blue for board background
        }
        
        # Set up the main window - REDUCED SIZE
        self.root.title("Tic-Tac-Toe with AI")
        self.root.geometry("500x650")  
        self.root.resizable(False, False)
        self.root.configure(bg=self.colors['bg'])
        
        # Create custom fonts - ADJUSTED FOR SMALLER WINDOW
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=11, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=9)
        self.button_font = font.Font(family="Helvetica", size=18, weight="bold")
        
        # Set application icon
        self.set_app_icon()
        
        # Create welcome screen first (this is the new addition)
        self.create_welcome_screen()
        
        # Setup styles for ttk widgets
        self.setup_styles()
        
        # Main container for the game (will be hidden initially)
        self.main_container = ttk.Frame(self.root, padding="10")

    def set_app_icon(self):
        try:
            # Get the directory of the current script file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Create absolute paths
            if os.name == 'nt':  
                icon_path = os.path.join(script_dir, "assets", "icon.png")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                else:
                    print(f"Warning: Icon file not found at {icon_path}")
        except Exception as e:
            print(f"Error setting application icon: {e}")
    
    def create_welcome_screen(self):
        """Create a welcome screen with play button"""
        self.welcome_frame = ttk.Frame(self.root, padding="20")
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title for welcome screen
        welcome_title = ttk.Label(self.welcome_frame, 
                                text="Welcome to Tic-Tac-Toe", 
                                font=("Helvetica", 20, "bold"),
                                foreground=self.colors['primary'])
        welcome_title.pack(pady=(40, 20))
        
        # Try to load and display game icon
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir,"assets","icon.png")
            
            if os.path.exists(icon_path):
                # Load and resize the image
                original_image = Image.open(icon_path)
                resized_image = original_image.resize((150, 150), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(resized_image)
                
                # Keep a reference to prevent garbage collection
                self.icon_image = tk_image
                
                # Display the image
                icon_label = ttk.Label(self.welcome_frame, image=self.icon_image, background=self.colors['bg'])
                icon_label.pack(pady=20)
            else:
                # If image not found, display a text placeholder
                placeholder = ttk.Label(self.welcome_frame, text="🎮", font=("Helvetica", 60))
                placeholder.pack(pady=20)
                print(f"Icon not found at {icon_path}, using text placeholder")
        except Exception as e:
            print(f"Error loading game icon: {e}")
            # Fallback to text-based icon
            placeholder = ttk.Label(self.welcome_frame, text="🎮", font=("Helvetica", 60))
            placeholder.pack(pady=20)
        
        # Play button - styled as a large, eye-catching button
        play_button_style = ttk.Style()
        play_button_style.configure("Play.TButton", font=("Helvetica", 16, "bold"))
        
        play_button = ttk.Button(self.welcome_frame, 
                               text="PLAY GAME", 
                               style="Play.TButton",
                               command=self.start_game)
        play_button.pack(pady=30, ipadx=20, ipady=10)
        
        # Add a footer with version
        version_label = ttk.Label(self.welcome_frame, 
                                text="v1.0.0 | Created with ♥", 
                                font=("Helvetica", 8), 
                                foreground="gray")
        version_label.pack(side=tk.BOTTOM, pady=10)
    
    def start_game(self):
        """Start the game by removing welcome screen and showing game interface"""
        # Destroy the welcome frame
        self.welcome_frame.destroy()
        
        # Create and pack the main container
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create all game interface elements
        self.create_header()
        self.create_difficulty_section()
        self.create_game_board()
        self.create_status_section()
        self.create_score_section()
        self.create_control_buttons()
        self.create_footer()
        
        # Reset the game to start fresh
        self.reset_game()

    def run(self):
        self.root.mainloop()
        
    def setup_styles(self):
        """Set up custom styles for ttk widgets"""
        self.style = ttk.Style()
        
        # Configure basic styles
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text'])
        self.style.configure('TButton', font=self.normal_font)
        self.style.configure('TRadiobutton', background=self.colors['bg'], foreground=self.colors['text'])
        
        # Create custom styles
        self.style.configure('Header.TLabel', font=self.header_font)
        self.style.configure('Title.TLabel', font=self.title_font)
        self.style.configure('GameStatus.TLabel', font=self.header_font, foreground=self.colors['primary'])
        
        # Custom button styles
        self.style.configure('Primary.TButton', background=self.colors['primary'], foreground="black", font=("Helvetica", 9, "bold"))
        self.style.map('Primary.TButton', background=[('active', self.colors['primary'])])
        
        self.style.configure('Secondary.TButton', background=self.colors['secondary'], foreground="black", font=("Helvetica", 9, "bold"))
        self.style.map('Secondary.TButton', background=[('active', self.colors['secondary'])])
        
        self.style.configure('Warning.TButton', background=self.colors['warning'], foreground="black", font=("Helvetica", 9, "bold"))
        self.style.map('Warning.TButton', background=[('active', self.colors['warning'])])
        
    def create_header(self):
        """Create the header with game title"""
        header_frame = ttk.Frame(self.main_container, padding="5")  # Reduced padding
        header_frame.pack(fill=tk.X, pady=(0, 10))  # Reduced padding
        
        # Create title label
        title_label = ttk.Label(header_frame, text="Tic-Tac-Toe with AI", style='Title.TLabel')
        title_label.pack()
        
        # Add a horizontal separator
        separator = ttk.Separator(self.main_container, orient='horizontal')
        separator.pack(fill=tk.X, pady=3)  # Reduced padding

    def create_difficulty_section(self):
        """Create the difficulty selection section"""
        difficulty_frame = ttk.LabelFrame(self.main_container, text="AI Difficulty", padding="10")  # Reduced padding
        difficulty_frame.pack(fill=tk.X, pady=5)  # Reduced padding
        
        self.difficulty_var = tk.StringVar(value="medium")
        
        # Create a container for radio buttons with better spacing
        radio_container = ttk.Frame(difficulty_frame)
        radio_container.pack(fill=tk.X, pady=3)  # Reduced padding
        
        # Create tooltips for each difficulty level
        easy_radio = ttk.Radiobutton(radio_container, text="Easy", variable=self.difficulty_var, 
                        value="easy", command=self.set_difficulty)
        easy_radio.pack(side=tk.LEFT, padx=10)  # Reduced padding
        self.create_tooltip(easy_radio, "AI makes random moves. Good for beginners.")
        
        medium_radio = ttk.Radiobutton(radio_container, text="Medium", variable=self.difficulty_var, 
                        value="medium", command=self.set_difficulty)
        medium_radio.pack(side=tk.LEFT, padx=10)  # Reduced padding
        self.create_tooltip(medium_radio, "AI makes smart moves 60% of the time. Moderate challenge.")
        
        unbeatable_radio = ttk.Radiobutton(radio_container, text="Unbeatable", variable=self.difficulty_var, 
                        value="unbeatable", command=self.set_difficulty)
        unbeatable_radio.pack(side=tk.LEFT, padx=10)  # Reduced padding
        self.create_tooltip(unbeatable_radio, "AI never loses. Uses Minimax algorithm with Alpha-Beta pruning.")
    
    def create_game_board(self):
        """Create the game board with buttons"""
        board_frame = ttk.Frame(self.main_container, padding="10")  # Reduced padding
        board_frame.pack(fill=tk.BOTH, expand=True, pady=10)  # Reduced padding
        
        # Create a container for the game grid with a border
        grid_container = tk.Frame(board_frame, bg=self.colors['primary'], padx=3, pady=3)
        grid_container.pack(pady=5)  # Reduced padding
        
        # Create buttons for each cell
        self.buttons = []
        for i in range(3):
            row_frame = tk.Frame(grid_container)
            row_frame.pack()
            for j in range(3):
                idx = i * 3 + j
                btn = tk.Button(row_frame, text="", font=self.button_font, 
                              width=3, height=1, 
                              bg=self.colors['board_bg'], fg=self.colors['text'],
                              activebackground=self.colors['bg'],
                              relief=tk.RAISED, bd=2,
                              command=lambda idx=idx: self.make_move(idx))
                btn.pack(side=tk.LEFT, padx=3, pady=3)
                self.buttons.append(btn)
    
    def create_status_section(self):
        """Create the status section with animated feedback"""
        status_frame = ttk.Frame(self.main_container, padding="5")  # Reduced padding
        status_frame.pack(fill=tk.X, pady=5)  # Reduced padding
        
        self.status_var = tk.StringVar(value="Your turn (X)")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                               style='GameStatus.TLabel', anchor=tk.CENTER)
        status_label.pack(fill=tk.X)
        
        # Add a progress bar for AI "thinking" animation
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          mode='indeterminate', length=300)  # Reduced length
    
    def create_control_buttons(self):
        """Create control buttons with enhanced styling"""
        button_frame = ttk.Frame(self.main_container, padding="5")  # Using ttk.Frame instead of tk.Frame
        button_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        new_game_btn = ttk.Button(button_frame, text="New Game", 
                            style='Primary.TButton',  # Using ttk style
                            command=self.reset_game)
        new_game_btn.pack(side=tk.LEFT, padx=5, pady=3, fill=tk.X, expand=True)
        
        # Reset Scores button
        reset_scores_btn = ttk.Button(button_frame, text="Reset Scores", 
                                style='Secondary.TButton',  # Using ttk style
                                command=self.reset_scores)
        reset_scores_btn.pack(side=tk.LEFT, padx=5, pady=3, fill=tk.X, expand=True)
        
        # Exit button
        exit_btn = ttk.Button(button_frame, text="Exit", 
                        style='Warning.TButton',  # Using ttk style
                        command=self.confirm_exit)
        exit_btn.pack(side=tk.LEFT, padx=5, pady=3, fill=tk.X, expand=True)
        
    def create_score_section(self):
        """Create an enhanced score section"""
        score_frame = ttk.LabelFrame(self.main_container, text="Game Statistics", padding="10")  # Reduced padding
        score_frame.pack(fill=tk.X, pady=10)  # Reduced padding
        
        # Create a grid layout for better alignment
        for i in range(3):
            score_frame.columnconfigure(i, weight=1)
        
        # Player score - with icons and better styling
        player_label = ttk.Label(score_frame, text="You (X)", style='Header.TLabel',
                               foreground=self.colors['player_x'])
        player_label.grid(row=0, column=0, pady=3)  # Reduced padding
        
        self.player_score_var = tk.StringVar(value="0")
        player_score_label = ttk.Label(score_frame, textvariable=self.player_score_var, 
                                     font=("Helvetica", 16, "bold"))  # Reduced font size
        player_score_label.grid(row=1, column=0, pady=3)  # Reduced padding
        
        # Draws
        draws_label = ttk.Label(score_frame, text="Draws", style='Header.TLabel')
        draws_label.grid(row=0, column=1, pady=3)  # Reduced padding
        
        self.draws_var = tk.StringVar(value="0")
        draws_score_label = ttk.Label(score_frame, textvariable=self.draws_var, 
                                    font=("Helvetica", 16, "bold"))  # Reduced font size
        draws_score_label.grid(row=1, column=1, pady=3)  # Reduced padding
        
        # AI score
        ai_label = ttk.Label(score_frame, text="AI (O)", style='Header.TLabel',
                           foreground=self.colors['player_o'])
        ai_label.grid(row=0, column=2, pady=3)  # Reduced padding
        
        self.ai_score_var = tk.StringVar(value="0")
        ai_score_label = ttk.Label(score_frame, textvariable=self.ai_score_var, 
                                 font=("Helvetica", 16, "bold"))  # Reduced font size
        ai_score_label.grid(row=1, column=2, pady=3)  # Reduced padding
        
        # Add total games counter
        games_frame = ttk.Frame(score_frame)
        games_frame.grid(row=2, column=0, columnspan=3, pady=5)  # Reduced padding
        
        ttk.Label(games_frame, text="Total Games: ").pack(side=tk.LEFT)
        self.total_games_var = tk.StringVar(value="0")
        ttk.Label(games_frame, textvariable=self.total_games_var).pack(side=tk.LEFT)
    
    def create_footer(self):
        """Create a footer with credits"""
        footer_frame = ttk.Frame(self.main_container)
        footer_frame.pack(fill=tk.X, pady=(10, 0))  # Reduced padding
        
        # Add a horizontal separator
        separator = ttk.Separator(footer_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=3)  # Reduced padding
        
        # Add version info and credits
        version_label = ttk.Label(footer_frame, text="v1.0.0 | Created with ♥", 
                                font=("Helvetica", 7), foreground="gray")  # Reduced font size
        version_label.pack(side=tk.RIGHT)
    
    def set_difficulty(self):
        """Set the AI difficulty level with feedback"""
        difficulty = self.difficulty_var.get()
        self.game.set_ai_difficulty(difficulty)
        self.reset_game()
        
        # Provide feedback about the difficulty change
        message = "AI difficulty set to: " + difficulty.capitalize()
        self.status_var.set(message)
        self.root.after(1500, lambda: self.status_var.set("Your turn (X)"))
    
    def make_move(self, idx):
        """Handle player's move with enhanced animation"""
        if not self.game_active or self.game.board[idx] != ' ':
            return
        
        # Player's move with animation - CUSTOM X SYMBOL
        self.buttons[idx].config(text="✗", fg=self.colors['player_x'])
        self.game.make_move(idx, self.player_letter)
        
        # Flash the button to show it was pressed
        self.buttons[idx].config(bg="#FFE0B2")  # Light orange
        self.root.update()
        self.root.after(100, lambda: self.buttons[idx].config(bg=self.colors['board_bg']))
        
        # Check if game is over after player's move
        if self.check_game_over():
            return
        
        # AI's move with "thinking" animation
        self.status_var.set("AI is thinking...")
        self.progress_bar.pack(pady=5)  # Reduced padding
        self.progress_bar.start(10)
        self.root.update()
        
        # Schedule AI move with a delay for better UX
        self.root.after(800, self.process_ai_move)
    
    def process_ai_move(self):
        """Process the AI move after animation"""
        ai_move = self.ai.get_move(self.game)
        self.game.make_move(ai_move, self.ai_letter)
        
        # Stop the progress animation
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        # Update the button with animation - CUSTOM O SYMBOL
        self.buttons[ai_move].config(text="◯", fg=self.colors['player_o'])
        self.buttons[ai_move].config(bg="#D1C4E9")  # Light purple
        self.root.update()
        self.root.after(100, lambda: self.buttons[ai_move].config(bg=self.colors['board_bg']))
        
        # Check if game is over after AI's move
        if not self.check_game_over():
            self.status_var.set("Your turn (X)")

    def check_game_over(self):
        """Check if the game is over with enhanced visual feedback"""
        winner_line = self.game.get_winner_line()
        
        if winner_line:
            winner = self.game.board[winner_line[0]]
            
            # Create winning animation with pulsing effect
            for _ in range(3):  # Pulse 3 times
                # Highlight the winning line
                for idx in winner_line:
                    self.buttons[idx].config(bg=self.colors['win_highlight'])
                self.root.update()
                time.sleep(0.2)
                
                # Return to normal
                for idx in winner_line:
                    self.buttons[idx].config(bg=self.colors['board_bg'])
                self.root.update()
                time.sleep(0.1)
            
            # Final highlight
            for idx in winner_line:
                self.buttons[idx].config(bg=self.colors['win_highlight'])
            
            if winner == self.player_letter:
                self.status_var.set("🎉 You win! 🎉")
                self.player_score += 1
                self.player_score_var.set(str(self.player_score))
            else:
                self.status_var.set("AI wins. Better luck next time!")
                self.ai_score += 1
                self.ai_score_var.set(str(self.ai_score))
            
            self.game_active = False
            self.update_total_games()
            return True
        
        elif not self.game.empty_squares():
            self.status_var.set("It's a draw!")
            # Highlight all buttons with a different color for draw
            for btn in self.buttons:
                btn.config(bg="#E0E0E0")  # Light gray
            self.draws += 1
            self.draws_var.set(str(self.draws))
            self.game_active = False
            self.update_total_games()
            return True
        
        return False
    
    def update_total_games(self):
        """Update the total games counter"""
        total = self.player_score + self.ai_score + self.draws
        self.total_games_var.set(str(total))

    def reset_game(self):
        """Reset the game board with animation"""
        self.game.reset_board()
        self.game_active = True
        self.status_var.set("Your turn (X)")
        
        # Animate the reset
        for btn in self.buttons:
            btn.config(text="", bg="#E3F2FD")  # Light blue
        self.root.update()
        time.sleep(0.2)
        
        for btn in self.buttons:
            btn.config(bg=self.colors['board_bg'])
        
        self.status_var.set("Your turn (X)")
    
    def reset_scores(self):
        """Reset all scores with confirmation"""
        if messagebox.askyesno("Reset Scores", "Are you sure you want to reset all game statistics?"):
            self.player_score = 0
            self.ai_score = 0
            self.draws = 0
            self.player_score_var.set("0")
            self.ai_score_var.set("0")
            self.draws_var.set("0")
            self.total_games_var.set("0")
            self.reset_game()
    
    def confirm_exit(self):
        """Confirm before exiting the application"""
        if messagebox.askyesno("Exit Game", "Are you sure you want to exit?"):
            self.root.quit()
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def enter(event):
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(self.tooltip, text=text, background="#FFFFCC", 
                           relief=tk.SOLID, borderwidth=1)
            label.pack()
            
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
        
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)