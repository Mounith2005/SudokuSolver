import tkinter as tk
import random
from copy import deepcopy
from tkinter import messagebox
from tkinter import simpledialog
from typing import Self
from PIL import Image, ImageTk
import os

class SudokuFrontPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.bg_color = "#f0e68c"  # Light background color
        self.root.configure(bg=self.bg_color)
        self.root.attributes("-fullscreen", True)

        # Load and resize the background image
        self.background_image = Image.open(r"C:\Users\Mounith\Desktop\study\Project\rosy\images.png")
        self.background_image = self.background_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        self.title_label = tk.Label(self.root, text="Welcome to Sudoku!", font=("Arial", 36, "bold"), fg="darkblue")
        self.title_label.pack(pady=10)

        self.desc_label = tk.Label(self.root, text="SUDOKU", font=("Arial", 40), bg=self.bg_color, fg="blue")
        self.desc_label.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", font=("Arial", 20), bg="#4CAF50", fg="white", command=self.start_game)
        self.play_button.pack(pady=30)

        self.quit_button = tk.Button(self.root, text="Quit", bg="red", fg="white", font=("Arial", 20), command=self.root.quit)
        self.quit_button.pack(pady=30)

        self.shake_animation()
        self.root.mainloop()

    def shake_animation(self, count=0):
        if count < 10:  # Shake 10 times
            shift = random.randint(-10, 10)
            self.desc_label.place(relx=0.5, rely=0.3, anchor="center", x=shift, y=shift)
            self.root.after(100, lambda: self.shake_animation(count + 1))  # Repeat after 100 ms
        else:
            # Reset position
            self.desc_label.place(relx=0.5, rely=0.3, anchor="center")
            self.title_label.place(relx=0.5, rely=0.15, anchor="center")
            self.quit_button.place(relx=0.5, rely=0.65, anchor="center")
            self.play_button.place(relx=0.5, rely=0.50, anchor="center")

    def start_game(self):
        self.root.withdraw()  # Hide the main window
        game = SudokuGame(self.root)  # Pass the main window to SudokuGame
        game.difficulty_selection()


class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.game_window = None
        self.board = None
        self.solved_board = None
        self.original_board = None
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.selected_difficulty = None
        self.bg_color = "#f0e68c"
        self.fixed_bg_color = "white"
        self.fixed_text_color = "black"
        self.entry_bg_color = "white"
        self.entry_text_color = "black"
        self.button_color = "#4CAF50"
        self.time_elapsed = 0
        self.timer_running = False
        self.time_limit = 3600  # 1 hour = 3600 seconds
        self.score = 0
        self.high_score = 0

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_row_start + i][box_col_start + j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    shuffled_numbers = random.sample(range(1, 10), 9)
                    for num in shuffled_numbers:
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def create_solved_board(self):
        board = [[0]*9 for _ in range(9)]
        self.solve_sudoku(board)
        return board

    def remove_cells(self, board, num_cells):
        cells_removed = 0
        while cells_removed < num_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if board[row][col] != 0:
                board[row][col] = 0
                cells_removed += 1

    def generate_sudoku(self, difficulty):
        self.solved_board = self.create_solved_board()
        self.board = deepcopy(self.solved_board)

        if difficulty == "easy":
            num_cells_removed = 20
        elif difficulty == "medium":
            num_cells_removed = 40
        elif difficulty == "hard":
            num_cells_removed = 55

        self.remove_cells(self.board, num_cells_removed)
        self.original_board = deepcopy(self.board)

    def display_board(self):
        center_frame = tk.Frame(self.game_window, bg="black")
        center_frame.place(relx=0.5, rely=0.4, anchor="center")
        

        for i in range(9):
            for j in range(9):
                e = tk.Entry(center_frame, width=4, justify="center", font=("Arial", 14))
                self.entries[i][j] = e
                if self.board[i][j] != 0:
                    e.insert(0, self.board[i][j])
                    e.config(state="readonly", disabledbackground=self.fixed_bg_color, disabledforeground=self.fixed_text_color)
                else:
                    e.config(bg=self.entry_bg_color, fg=self.entry_text_color)
                e.grid(row=i, column=j, padx=2, pady=2)

    def hint(self):
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = self.solved_board[row][col]
            self.entries[row][col].insert(0, self.solved_board[row][col])
            self.entries[row][col].config(state="readonly", disabledbackground=self.fixed_bg_color, disabledforeground=self.fixed_text_color)

    def check_puzzle(self):
        correct = True
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    user_input = self.entries[i][j].get()
                    if not user_input.isdigit() or int(user_input) != self.solved_board[i][j]:
                        correct = False
                        self.entries[i][j].config(bg="lightcoral")
                    else:
                        self.score += 1
                        self.entries[i][j].config(bg="lightgreen")

        if correct:
            self.stop_timer()
            if self.score > self.high_score:
                self.high_score = self.score
            messagebox.showinfo("Success", f"Puzzle solved correctly! Your score: {self.score}\nHigh Score: {self.high_score}")

            # Generate the next puzzle
            self.next_puzzle()

    def next_puzzle(self):
        """Generate and display a new puzzle after the current one is solved."""
        self.reset_puzzle()  # Reset the current puzzle
        self.generate_sudoku(self.selected_difficulty)  # Generate a new puzzle
        self.display_board()  # Display the new puzzle
        self.score = 0  # Reset score for the new puzzle
        self.start_timer()  # Restart the timer

    def reveal_puzzle(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = self.solved_board[i][j]
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, self.solved_board[i][j])
                self.entries[i][j].config(state="readonly", disabledbackground=self.fixed_bg_color, disabledforeground=self.fixed_text_color)

    def reset_puzzle(self):
        self.board = deepcopy(self.original_board)
        self.score = 0
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state="normal", bg=self.entry_bg_color, fg=self.entry_text_color)
                self.entries[i][j].delete(0, tk.END)
                if self.board[i][j] != 0:
                    self.entries[i][j].insert(0, self.board[i][j])
                    self.entries[i][j].config(state="readonly", disabledbackground=self.fixed_bg_color, disabledforeground=self.fixed_text_color)

    def setup_buttons(self):
        button_frame = tk.Frame(self.game_window, bg="black")
        button_frame.place(relx=0.5, rely=0.8, anchor="center")

        tk.Button(button_frame, text="Hint", bg="grey", fg="white", font=("Arial", 14), command=self.hint).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Check Puzzle", bg="grey", fg="white", font=("Arial", 14), command=self.check_puzzle).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Reveal Puzzle", bg="grey", fg="white", font=("Arial", 14), command=self.reveal_puzzle).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Reset Puzzle", bg="grey", fg="white", font=("Arial", 14), command=self.reset_puzzle).grid(row=0, column=3, padx=10)
        tk.Button(button_frame, text="Back", bg="grey", fg="white", font=("Arial", 14), command=self.go_back_to_difficulty_selection).grid(row=0, column=4, padx=10)
        tk.Button(button_frame, text="Save Solved Board", bg="grey", fg="white", font=("Arial", 14), command=self.save_solved_board).grid(row=0, column=5, padx=10)

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            if self.time_elapsed < self.time_limit:
                minutes, seconds = divmod(self.time_elapsed, 60)
                self.timer_label.config(text=f"Time Elapsed: {minutes:02}:{seconds:02}    |    Score: {self.score}   |     High Score: {self.high_score}",bg="grey")
                self.time_elapsed += 1
                self.game_window.after(1000, self.update_timer)
            else:
                self.stop_timer()
                messagebox.showinfo("Time Up", "1 hour has passed! Time's up!")

    def start_game(self):
        if self.selected_difficulty:
            self.game_window = tk.Toplevel(self.root)  # Create a new window for the game
            self.game_window.title("Sudoku Game")
            self.game_window.configure(bg="black")
            self.game_window.attributes("-fullscreen", True)  # Set to fullscreen

            self.background_image = Image.open(r"C:\Users\Mounith\Desktop\study\Project\rosy\sudu3.jpg")  # Update path as needed
            self.background_image = self.background_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
            self.background_image = ImageTk.PhotoImage(self.background_image)

            background_label = tk.Label(self.game_window, image=self.background_image)
            background_label.place(relwidth=1, relheight=1)
            
            self.generate_sudoku(self.selected_difficulty)
            self.display_board()
            self.setup_buttons()

            self.timer_label = tk.Label(self.game_window, bg="grey", fg="black", font=("Arial", 14))
            self.timer_label.place(relx=0.5, rely=0.1, anchor="center")
            self.start_timer()

    def set_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
        self.start_game()

    def difficulty_selection(self):
        self.game_window = tk.Toplevel(self.root)  # Create a new window for difficulty selection
        self.game_window.title("Sudoku - Choose Difficulty")
        self.game_window.configure(bg=self.bg_color)
        self.game_window.attributes("-fullscreen", True)

        # Load and resize the background image
        self.background_image = Image.open(r"C:\Users\Mounith\Desktop\study\Project\rosy\sudu2.png")
        self.background_image = self.background_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        background_label = tk.Label(self.game_window, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)  # Set to fullscreen

        label = tk.Label(self.game_window, text="Choose difficulty level", font=("Arial", 16), bg=self.bg_color, fg=self.entry_text_color)
        label.place(relx=0.5, rely=0.075, anchor="center")
        label = tk.Label(self.game_window, text="Test your logic and problem-solving skills!", font=("Arial", 16), bg=self.bg_color, fg=self.entry_text_color)
        label.place(relx=0.5, rely=0.189, anchor="center")

        tk.Button(self.game_window, text="Play", font=("Arial", 14), width=10, command=lambda: self.set_difficulty("easy")).place(relx=0.2, rely=0.5, anchor="center")
        tk.Button(self.game_window, text="Play", font=("Arial", 14), width=10, command=lambda: self.set_difficulty("medium")).place(relx=0.5, rely=0.5, anchor="center")
        tk.Button(self.game_window, text="Play", font=("Arial", 14), width=10, command=lambda: self.set_difficulty("hard")).place(relx=0.8, rely=0.5, anchor="center")

        tk.Button(self.game_window, text="Quit", bg="red", font=("Arial", 14), width=10, command=self.root.quit).place(relx=0.5, rely=0.8, anchor="center")

    def go_back_to_difficulty_selection(self):
        self.game_window.destroy()
        self.difficulty_selection()

    def save_solved_board(self):
        try:
        # Generate a unique filename
            documents_folder = os.path.expanduser("~/Documents/sudoku")
            base_filename = "sudoku"
            file_extension = ".txt"
            count = 1
        
        # Find the next available filename
            while True:
                file_path = os.path.join(documents_folder, f"{base_filename}{count}{file_extension}")
                if not os.path.exists(file_path):
                    break
                count += 1
        
        # Save the solved board to the generated filename
            with open(file_path, "w") as f:
                for row in self.solved_board:
                    f.write(" ".join(map(str, row)) + "\n")
        
            messagebox.showinfo("Saved", f"Solved Sudoku board saved to '{file_path}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")


# Run the application
if __name__ == "__main__":
    SudokuFrontPage()
