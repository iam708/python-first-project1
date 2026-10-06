import random
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0]*cols for _ in range(rows)]      # actual board
        self.visible = [['.']*cols for _ in range(rows)]  # what player sees
        self.flagged = [[False]*cols for _ in range(rows)]
        self.game_over = False
        self.won = False
        self.first_move = True
        self.revealed = 0

    def place_mines(self, safe_r, safe_c):
        """Place mines after first move, avoiding the clicked cell."""
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)
                     if not (r == safe_r and c == safe_c)]
        mine_positions = random.sample(positions, self.mines)
        for r, c in mine_positions:
            self.board[r][c] = -1  # -1 = mine

        # Calculate numbers
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                self.board[r][c] = sum(
                    1 for dr in [-1,0,1] for dc in [-1,0,1]
                    if 0 <= r+dr < self.rows and 0 <= c+dc < self.cols
                    and self.board[r+dr][c+dc] == -1
                )

    def reveal(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        if self.visible[r][c] != '.' or self.flagged[r][c]:
            return

        if self.first_move:
            self.place_mines(r, c)
            self.first_move = False

        if self.board[r][c] == -1:
            self.visible[r][c] = '*'
            self.game_over = True
            self._reveal_all_mines()
            return

        val = self.board[r][c]
        self.visible[r][c] = str(val) if val > 0 else ' '
        self.revealed += 1

        if val == 0:  # flood fill for empty cells
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal(r+dr, c+dc)

        # Check win
        safe_cells = self.rows * self.cols - self.mines
        if self.revealed == safe_cells:
            self.won = True
            self.game_over = True

    def flag(self, r, c):
        if self.visible[r][c] != '.' :
            print("Can only flag unrevealed cells.")
            return
        self.flagged[r][c] = not self.flagged[r][c]

    def _reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.visible[r][c] = '*'

    def display(self):
        # Column headers
        col_header = '    ' + '  '.join(str(c+1).rjust(2) for c in range(self.cols))
        print(col_header)
        print('   ' + '+---' * self.cols + '+')
        for r in range(self.rows):
            row_label = str(r+1).rjust(2)
            cells = []
            for c in range(self.cols):
                if self.flagged[r][c] and self.visible[r][c] == '.':
                    cells.append(' F ')
                else:
                    v = self.visible[r][c]
                    if v == '*':
                        cells.append(' * ')
                    elif v == ' ':
                        cells.append('   ')
                    elif v == '.':
                        cells.append(' . ')
                    else:
                        cells.append(f' {v} ')
            print(f'{row_label} |' + '|'.join(cells) + '|')
            print('   ' + '+---' * self.cols + '+')

        flags_left = self.mines - sum(self.flagged[r][c] for r in range(self.rows) for c in range(self.cols))
        print(f'\n  Mines remaining: {flags_left}')

def get_input(prompt, valid_range):
    while True:
        try:
            val = int(input(prompt))
            if val in valid_range:
                return val
            print(f"  Please enter a number between {valid_range[0]} and {valid_range[-1]}.")
        except ValueError:
            print("  Invalid input. Enter a number.")

def choose_difficulty():
    print("\n  ╔══════════════════════╗")
    print("  ║    MINESWEEPER 💣    ║")
    print("  ╚══════════════════════╝\n")
    print("  Difficulty:")
    print("  1) Beginner   (9×9,  10 mines)")
    print("  2) Intermediate (16×16, 40 mines)")
    print("  3) Expert     (16×30, 99 mines)")
    print("  4) Custom")
    choice = get_input("\n  Choose [1-4]: ", range(1, 5))
    if choice == 1:
        return 9, 9, 10
    elif choice == 2:
        return 16, 16, 40
    elif choice == 3:
        return 16, 30, 99
    else:
        rows = get_input("  Rows (2-20): ", range(2, 21))
        cols = get_input("  Cols (2-30): ", range(2, 31))
        max_mines = rows * cols - 1
        mines = get_input(f"  Mines (1-{max_mines}): ", range(1, max_mines+1))
        return rows, cols, mines

def main():
    while True:
        clear()
        rows, cols, mines = choose_difficulty()
        game = Minesweeper(rows, cols, mines)

        while not game.game_over:
            clear()
            print("\n  ╔══════════════════════╗")
            print("  ║    MINESWEEPER 💣    ║")
            print("  ╚══════════════════════╝\n")
            game.display()
            print("\n  Commands:  R row col  →  reveal   |  F row col  →  flag/unflag")
            print("  Example:   R 3 5     or   F 1 2\n")

            cmd = input("  > ").strip().upper().split()
            if len(cmd) != 3:
                print("  Usage: R row col  or  F row col"); input("  Press Enter..."); continue
            action = cmd[0]
            if action not in ('R', 'F'):
                print("  Unknown command. Use R or F."); input("  Press Enter..."); continue
            try:
                r, c = int(cmd[1])-1, int(cmd[2])-1
            except ValueError:
                print("  Row and col must be numbers."); input("  Press Enter..."); continue
            if not (0 <= r < rows and 0 <= c < cols):
                print(f"  Out of bounds. Row 1-{rows}, Col 1-{cols}."); input("  Press Enter..."); continue

            if action == 'R':
                game.reveal(r, c)
            else:
                game.flag(r, c)

        clear()
        print("\n  ╔══════════════════════╗")
        print("  ║    MINESWEEPER 💣    ║")
        print("  ╚══════════════════════╝\n")
        game.display()

        if game.won:
            print("\n  🎉  You win! All mines cleared!\n")
        else:
            print("\n  💥  BOOM! You hit a mine!\n")

        again = input("  Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("\n  Thanks for playing!\n")
            break

if __name__ == '__main__':
    main()