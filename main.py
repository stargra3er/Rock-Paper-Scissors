import tkinter as tk
from web3 import Web3
from web3.utils.address import to_checksum_address
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/062ad22dfbea48caa283da9d10357945'))
# Define the game logic
def play_game():
    player1_name = entry_player1_name.get()
    player1_password = entry_player1_password.get()
    player1_bet = entry_player1_bet.get()
    player1_move = player1_choice.get()

    player2_name = entry_player2_name.get()
    player2_password = entry_player2_password.get()
    player2_bet = entry_player2_bet.get()
    player2_move = player2_choice.get()

    if player1_move == player2_move:
        result_label.config(text="It's a tie!")
    elif (player1_move == 'Rock' and player2_move == 'Scissors') or \
            (player1_move == 'Scissors' and player2_move == 'Paper') or \
            (player1_move == 'Paper' and player2_move == 'Rock'):
        result_label.config(text=f"{player1_name} wins!")
        pl1toPl2()
    else:
        result_label.config(text=f"{player2_name} wins!")
        pl2toPl1()

# Create the main window
window = tk.Tk()
window.title("Rock-Paper-Scissors Game")
window.geometry('800x200')
window.resizable(0, 1)

# Create labels, entry fields, and buttons
label_player1 = tk.Label(window, text="Player 1")
label_player1.grid(row=0, column=0)

label_player2 = tk.Label(window, text="Player 2")
label_player2.grid(row=0, column=2)

label_name = tk.Label(window, text="Address:")
label_name.grid(row=1, column=0)

label_password = tk.Label(window, text="Private key:")
label_password.grid(row=2, column=0)

label_choice = tk.Label(window, text="Choose move:")
label_choice.grid(row=4, column=0)

label_bet = tk.Label(window, text="Bet amount:")
label_bet.grid(row=3, column=0)

entry_player1_name = tk.Entry(window, width=50)
entry_player1_name.grid(row=1, column=1)

entry_player1_password = tk.Entry(window, show='*', width=50)
entry_player1_password.grid(row=2, column=1)

entry_player1_bet = tk.Entry(window, width=50)
entry_player1_bet.grid(row=3, column=1)

entry_player2_name = tk.Entry(window, width=50)
entry_player2_name.grid(row=1, column=3)

entry_player2_password = tk.Entry(window, show='*', width=50)
entry_player2_password.grid(row=2, column=3)

entry_player2_bet = tk.Entry(window, width=50)
entry_player2_bet.grid(row=3, column=3)

player1_choice = tk.StringVar()
player2_choice = tk.StringVar()

player1_choice.set("Rock")  # Default choice
player2_choice.set("Rock")  # Default choice

choices = ['Rock', 'Paper', 'Scissors']

player1_option_menu = tk.OptionMenu(window, player1_choice, *choices)
player2_option_menu = tk.OptionMenu(window, player2_choice, *choices)

player1_option_menu.grid(row=4, column=1)
player2_option_menu.grid(row=4, column=3)

play_button = tk.Button(window, text="Play", command=play_game)
play_button.grid(row=5, column=2)

result_label = tk.Label(window, text="")
result_label.grid(row=6, column=1, columnspan=3)

# Move these lines inside the play_game() function to get the latest input values
# player1_name = entry_player1_name.get()
# player1_password = entry_player1_password.get()
# player1_bet = entry_player1_bet.get()
# player1_move = player1_choice.get()
#
# player2_name = entry_player2_name.get()
# player2_password = entry_player2_password.get()
# player2_bet = entry_player2_bet.get()
# player2_move = player2_choice.get()


from_account = None
to_account = None
private_key1 = None
private_key2 = None
bet1 = None
bet2 = None
nonce = None

def pl1toPl2():
    global nonce, from_account, to_account, private_key1, private_key2, bet1, bet2

    player1_name = entry_player1_name.get()
    player2_name = entry_player2_name.get()
    private_key1 = entry_player1_password.get()
    private_key2 = entry_player2_password.get()
    bet1 = entry_player1_bet.get()
    bet2 = entry_player2_bet.get()

    from_account = to_checksum_address(player1_name)
    to_account = to_checksum_address(player2_name)
    nonce = web3.eth.getTransactionCount(from_account)

    tx = {
        'nonce': nonce,
        'to': to_account,
        'value': web3.toWei(float(bet1), 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei(float(bet2), 'gwei')
    }

    signed_tx = web3.eth.account.signTransaction(tx, private_key1)
    tx_transaction = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

def pl2toPl1():
    global nonce, from_account, to_account, private_key1, private_key2, bet1, bet2

    player1_name = entry_player1_name.get()
    player2_name = entry_player2_name.get()
    private_key1 = entry_player1_password.get()
    private_key2 = entry_player2_password.get()
    bet1 = entry_player1_bet.get()
    bet2 = entry_player2_bet.get()

    from_account = Web3.toChecksumAddress(player1_name)
    to_account = Web3.toChecksumAddress(player2_name)
    nonce = web3.eth.getTransactionCount(from_account)

    tx = {
        'nonce': nonce,
        'to': from_account,
        'value': web3.toWei(float(bet2), 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei(40, 'gwei')
    }

    signed_tx = web3.eth.account.signTransaction(tx, private_key2)
    tx_transaction = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

window.mainloop()
