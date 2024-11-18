import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import mysql.connector
from tkinter import PhotoImage
from copy import deepcopy

# Helper function to handle DB connection
def connect_to_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sudoku"
        )
        return db
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database connection error: {err}")
        return None

# Main Page for launching the app
class SudokuFrontPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.bg_color = "#f0e68c"
        self.root.configure(bg=self.bg_color)
        self.root.attributes("-fullscreen", True)

        # Load and resize background image
        self.background_image = Image.open(r"C:\Users\Mounith\Desktop\study\Project\rosy\sudu6.png")
        self.background_image = self.background_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create a Canvas to display the background image
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Display text directly on the canvas
        self.canvas.create_text(self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight() // 12,
                                text="Welcome to Sudoku!", font=("Arial", 36, "bold"), fill="darkblue")

        # Buttons
        self.play_button = tk.Button(self.root, text="Play", font=("Arial", 20), bg="#4CAF50", fg="white", command=self.show_login_page)
        self.quit_button = tk.Button(self.root, text="Quit", bg="red", fg="white", font=("Arial", 20), command=self.root.quit)

        # Pack buttons after canvas
        self.play_button.place(x=self.root.winfo_screenwidth() // 2 - 70, y=self.root.winfo_screenheight() // 3+50)
        self.quit_button.place(x=self.root.winfo_screenwidth() // 2 - 70, y=self.root.winfo_screenheight() // 2 + 60)

        self.root.mainloop()
    

    def show_login_page(self):
        self.root.withdraw()
        LoginPage(self.root)

# Login Page class
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login Page")
        self.login_window.configure(bg="#f0e68c")
        self.login_window.attributes("-fullscreen", True)

        # Load background image
        self.bg_image = PhotoImage(file="sudu2.png")  # Replace with the actual path
        self.bg_label = tk.Label(self.login_window, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Make background fill entire window

        # Create a frame for better layout management
        frame = tk.Frame(self.login_window, bg="#f0e68c")
        frame.pack(expand=True)

        # Username label and entry
        self.username_label = tk.Label(frame, text="Username", font=("Arial", 14), bg="#f0e68c")
        self.username_label.pack(pady=10)
        
        self.username_entry = tk.Entry(frame, font=("Arial", 14))
        self.username_entry.pack(pady=10)

        # Password label and entry
        self.password_label = tk.Label(frame, text="Password", font=("Arial", 14), bg="#f0e68c")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=10)

        # Login button
        self.login_button = tk.Button(frame, text="Login", font=("Arial", 14), command=self.login)
        self.login_button.pack(pady=10)

        # Sign Up button
        self.signup_button = tk.Button(frame, text="Sign Up", font=("Arial", 14), command=self.show_signup_page)
        self.signup_button.pack(pady=10)

        # Back button
        self.back_button = tk.Button(frame, text="Back", font=("Arial", 14), command=self.login_window.quit)
        self.back_button.pack(pady=10)
        

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db = connect_to_db()
        if db is None:
            return

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.login_window.destroy()
            self.start_game(username)  # Pass the username to the game
        else:
            messagebox.showerror("Error", "Invalid username or password.")

        cursor.close()
        db.close()

    def show_signup_page(self):
        self.login_window.withdraw()
        SignupPage(self.root)

       

    def start_game(self, username):  # Accept username parameter
        self.root.withdraw()  # Hide the main window
        game = SudokuGame(self.root, username)  # Pass the username to SudokuGame
        game.difficulty_selection()


# Signup Page class
class SignupPage:
    def __init__(self, root):
        self.root = root
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Signup Page")
        self.signup_window.configure(bg="#f0e68c")
        self.signup_window.attributes("-fullscreen", True)

        # Load background image for design enhancement
        self.bg_image = PhotoImage(file="sudu8.png")  # Replace with the actual path to your background image
        self.bg_label = tk.Label(self.signup_window, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)  # Make background fill the entire window

        # Create a frame for form styling
        frame = tk.Frame(self.signup_window, bg="#f0e68c")
        frame.place(relx=0.5, rely=0.4, anchor="center")

        # Title label for the signup page
        self.title_label = tk.Label(frame, text="Create a New Account", font=("Arial", 24, "bold"), bg="#f0e68c", fg="blue")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Username label and entry field
        self.username_label = tk.Label(frame, text="Username", font=("Arial", 14), bg="#f0e68c", fg="black")
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.username_entry = tk.Entry(frame, font=("Arial", 14), width=25, bd=2, relief="solid")
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # Password label and entry field
        self.password_label = tk.Label(frame, text="Password", font=("Arial", 14), bg="#f0e68c", fg="black")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 14), width=25, bd=2, relief="solid")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Confirm Password label and entry field
        self.confirm_password_label = tk.Label(frame, text="Confirm Password", font=("Arial", 14), bg="#f0e68c", fg="black")
        self.confirm_password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        
        self.confirm_password_entry = tk.Entry(frame, show="*", font=("Arial", 14), width=25, bd=2, relief="solid")
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Sign Up Button
        self.signup_button = tk.Button(frame, text="Sign Up", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=self.signup)
        self.signup_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Back to Login Button
        self.back_button = tk.Button(frame, text="Back to Login", font=("Arial", 14), command=self.go_back_to_login, bg="orange", fg="black")
        self.back_button.grid(row=5, column=0, columnspan=2, pady=10)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        db = connect_to_db()
        if db is None:
            return

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists!")
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        messagebox.showinfo("Success", "Account created successfully!")
        self.signup_window.destroy()
        LoginPage(self.root)

        cursor.close()
        db.close()

    def go_back_to_login(self):
        self.signup_window.destroy()
        LoginPage(self.root)

# Main Sudoku Game
class SudokuGame:
    def __init__(self, root, username):
        self.root = root
        self.username=username
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
        self.entry_t_color = "green"
        self.button_color = "#4CAF50"
        self.time_elapsed = 0
        self.timer_running = False
        self.time_limit = 3600  # 1 hour = 3600 seconds
        self.score = 0
        self.high_score = 0
        

    def update_high_score_in_db(self):
        db = connect_to_db()
        if db is None:
            return

        cursor = db.cursor()
        cursor.execute("SELECT score FROM users WHERE username = %s", (self.username,))
        user = cursor.fetchone()

        if user:
            # User exists, update the high score if necessary
            current_high_score = user[0]
            if self.score > current_high_score:
                cursor.execute("UPDATE users SET score = %s WHERE username = %s", (self.score, self.username))
                db.commit()
                messagebox.showinfo("Success", "High score updated!")
        else:
            messagebox.showerror("Error", "User not found in the database.")

        cursor.close()
        db.close()
 

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

            # Update the high score in the database
            self.update_high_score_in_db()

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
            
            username_label = tk.Label(self.game_window, text=f"Welcome, {self.username}!", font=("Arial", 14), bg="black", fg="white")
            username_label.place(relx=0.5, rely=0.05, anchor="center")

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
        # Create a new window for difficulty selection
        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Sudoku - Choose Difficulty")
        self.game_window.configure(bg=self.bg_color)
        self.game_window.attributes("-fullscreen", True)

        # Load and resize the background image
        self.background_image = Image.open(r"C:\Users\Mounith\Desktop\study\Project\rosy\sudu7.png")
        self.background_image = self.background_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        )
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create a Canvas to display the background image and text
        self.canvas = tk.Canvas(self.game_window, bg=self.bg_color, bd=0, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)  # Fill the entire window
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Ensure window size is available after it is rendered
        self.game_window.after(100, self.add_text_and_buttons)

    def add_text_and_buttons(self):
        # Display the text "Choose difficulty level"
        center_x = self.game_window.winfo_width() // 2
        center_y = self.game_window.winfo_height() // 2

        self.canvas.create_text(center_x, center_y - 400, text="Choose difficulty level", font=("Arial", 24), fill=self.entry_t_color)
        self.canvas.create_text(center_x, center_y - 100, text="Test your logic and problem-solving skills!", font=("Arial", 16), fill=self.entry_t_color)

        # Difficulty buttons
        button_width = 10
        tk.Button(self.game_window, text="Easy", font=("Arial", 14), width=button_width, command=lambda: self.set_difficulty("easy")).place(relx=0.2, rely=0.5, anchor="center")
        tk.Button(self.game_window, text="Medium", font=("Arial", 14), width=button_width, command=lambda: self.set_difficulty("medium")).place(relx=0.5, rely=0.5, anchor="center")
        tk.Button(self.game_window, text="Hard", font=("Arial", 14), width=button_width, command=lambda: self.set_difficulty("hard")).place(relx=0.8, rely=0.5, anchor="center")

        # Quit button
        tk.Button(self.game_window, text="Quit", bg="red", font=("Arial", 14), width=button_width, command=self.root.quit).place(relx=0.5, rely=0.8, anchor="center")

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
