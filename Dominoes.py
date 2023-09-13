import random

# Define the Domino class
class Domino:
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2

    def __str__(self):
        return f"({self.side1}, {self.side2})"

    def is_match(self, value):
        return self.side1 == value or self.side2 == value

# Define the CDominoes class to manage the pile of dominoes
class CDominoes:
    def __init__(self):
        self.pieces = []

    def initialize_dominoes(self):
        for i in range(7):
            for j in range(i, 7):
                self.pieces.append(Domino(i, j))
        random.shuffle(self.pieces)

    def draw_piece(self):
        if self.pieces:
            return self.pieces.pop()
        else:
            return None

# Define the CPlayer class
class CPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_to_hand(self, pieces):
        self.hand.extend(pieces)

    def play_piece(self, table):
        for piece in self.hand:
            if table.is_playable(piece):
                self.hand.remove(piece)
                return piece
        return None

    def draw_piece(self, dominoes):
        piece = dominoes.draw_piece()
        if piece:
            self.hand.append(piece)
        return piece

# Define the CRandom class to sort the domino pieces
class CRandom:
    def __init__(self, dominoes):
        self.dominoes = dominoes

    def sort_dominoes(self):
        random.shuffle(self.dominoes.pieces)

class CTable:
    def __init__(self):
        self.board = []

    def display_board(self):
        if not self.board:
            print("Dominoes on the table: None")
        else:
            print("Dominoes on the table:")
            for piece in self.board:
                self.print_domino_ascii(piece)

    def place_piece(self, piece, end):
        if not self.board:
            self.board.append(piece)
        else:
            if end == 'head':
                self.board.insert(0, piece)
            elif end == 'tail':
                self.board.append(piece)

    def is_playable(self, piece):
        if not self.board:
            return True
        head, tail = self.board[0].side1, self.board[-1].side2
        return piece.is_match(head) or piece.is_match(tail)

    def print_domino_ascii(self, domino):
        lines = [
            "+-------+",
            f"| {domino.side1}   {domino.side2} |",
            "|       |",
            "+-------+",
        ]
        for line in lines:
            print(line)

    def is_winner(self, player):
        # Check if the player has won
        if not player.hand and all(piece.is_match(self.board[0].side1) and piece.is_match(self.board[-1].side2) for piece in player.hand):
            return True
        return False

# Function to initialize the game
def initialize_game():

    dominoes = CDominoes()
    dominoes.initialize_dominoes()

    player1 = CPlayer("Player 1")
    player2 = CPlayer("Player 2")

    # Assign 10 dominoes to each player
    for _ in range(10):
        player1.add_to_hand([dominoes.draw_piece()])
        player2.add_to_hand([dominoes.draw_piece()])

    remaining_pieces = [str(piece) for piece in dominoes.pieces[:8]]

    print("Player 1 gets these dominoes:")
    for piece in player1.hand:
        print(piece)
    print("Player 2 gets these dominoes:")
    for piece in player2.hand:
        print(piece)
    print("\nRemaining dominoes for both players to choose from:")
    for piece in remaining_pieces:
        print(piece)

    return dominoes, [player1, player2]

# Main game loop
def run_game():
    dominoes, player_list = initialize_game()
    table = CTable()

    current_player = player_list[0]

    consecutive_passes = 0  # Keep track of consecutive passes

    while dominoes.pieces or any(player.hand for player in player_list):
        print(f"\n{current_player.name}'s turn:")
        table.display_board()

        playable_piece = current_player.play_piece(table)

        if playable_piece:
            print(f"{current_player.name} places this domino on the table:")
            table.print_domino_ascii(playable_piece)
            table.place_piece(playable_piece, 'head' if table.board and playable_piece.is_match(table.board[0].side1) else 'tail')

            # Check if the current player has won
            if table.is_winner(current_player):
                print(f"{current_player.name} wins!")
                break
            consecutive_passes = 0
        else:
            drawn_piece = current_player.draw_piece(dominoes)
            if drawn_piece:
                print(f"{current_player.name} draws this domino from the pile:")
                table.print_domino_ascii(drawn_piece)
            else:
                print(f"No available pieces left for {current_player.name}.")
                consecutive_passes += 1

        if consecutive_passes == 2:  # Both players passed consecutively
            print("\nThe game ended in a draw.")
            break

        # Display counts of pieces on the board, remaining pieces, and pile size
        print(f"Total pieces on board: {len(table.board)}")
        print(f"Pieces remaining for {player_list[0].name}: {len(player_list[0].hand)}")
        print(f"Pieces remaining for {player_list[1].name}: {len(player_list[1].hand)}")
        print(f"Pieces remaining in the pile: {len(dominoes.pieces)}")

        current_player = player_list[1] if current_player == player_list[0] else player_list[0]

    if consecutive_passes != 2:  # Determine the second-placed player and remaining pieces
        second_placed_player = player_list[0] if current_player == player_list[1] else player_list[1]
        remaining_pieces = [str(piece) for piece in second_placed_player.hand]

        print("\nFinal Result:")
        print(f"Winner: {current_player.name}")
        print(f"Second Placed: {second_placed_player.name}")
        print(f"Remaining Pieces for {second_placed_player.name}:")
        for piece in remaining_pieces:
            print(piece)
        print("\nDominoes on the table:")
        table.display_board()

if __name__ == "__main__":
    run_game()