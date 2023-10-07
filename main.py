import tkinter as tk
from tkinter import simpledialog, messagebox
import random


# Function to play Rock-Paper-Scissors
def play_rps(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return "It's a tie!"
    elif (player1_choice == 'Rock' and player2_choice == 'Scissors') or \
            (player1_choice == 'Paper' and player2_choice == 'Rock') or \
            (player1_choice == 'Scissors' and player2_choice == 'Paper'):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!"


# Function to handle the game logic
def play_game():
    # Ask for username and password for Player 1
    player1_name = simpledialog.askstring("Player 1", "Enter your username:")
    player1_password = simpledialog.askstring("Player 1", "Enter your password:")

    # Ask for username and password for Player 2
    player2_name = simpledialog.askstring("Player 2", "Enter your username:")
    player2_password = simpledialog.askstring("Player 2", "Enter your password:")

    # Check if the passwords match for both players
    if player1_password != player2_password:
        messagebox.showerror("Error", "Passwords do not match. Please try again.")
        return

    # Create a new window for the game
    game_window = tk.Toplevel(root)
    game_window.title("Rock-Paper-Scissors Game")

    # Create labels and buttons for player choices
    player1_label = tk.Label(game_window, text=f"{player1_name}'s Choice:")
    player1_label.pack()

    player1_choice_var = tk.StringVar()
    player1_choice_var.set("Rock")
    player1_choice_menu = tk.OptionMenu(game_window, player1_choice_var, "Rock", "Paper", "Scissors")
    player1_choice_menu.pack()

    player2_label = tk.Label(game_window, text=f"{player2_name}'s Choice:")
    player2_label.pack()

    player2_choice_var = tk.StringVar()
    player2_choice_var.set("Rock")
    player2_choice_menu = tk.OptionMenu(game_window, player2_choice_var, "Rock", "Paper", "Scissors")
    player2_choice_menu.pack()

    result_label = tk.Label(game_window, text="")
    result_label.pack()

    # Function to handle the game result
    def show_result():
        player1_choice = player1_choice_var.get()
        player2_choice = player2_choice_var.get()
        result = play_rps(player1_choice, player2_choice)
        result_label.config(text=result)

    play_button = tk.Button(game_window, text="Play", command=show_result)
    play_button.pack()


# Create the main window
root = tk.Tk()
root.title("Rock-Paper-Scissors Game")

# Create a button to start the game
start_button = tk.Button(root, text="Start Game", command=play_game)
start_button.pack()

# Run the main loop
root.mainloop()
