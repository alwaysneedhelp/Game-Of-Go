import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys, os

class Start:
    def __init__(self):
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.title("Rules")
        self.label = tk.Label(
            self.window,
            text='Game of Go',
            height=2,
            font=('Fontin', 40, 'bold'),
            fg='black'
        )
        self.label.pack(side='top')
        self.instructions = tk.Label(
            self.window,
            text='Rules:\n- Players take turns placing stones on the board\n- A player can pass their turn\n- A player can resign the game\n- A player can place a stone on an empty intersection\n- A player cannot place a stone on an intersection that is already occupied\n- A player cannot place a stone on an intersection that will result in a self-capture move\n- A player should occupy as much territory as possible\n- If two players pass their turns consecutively, the game ends\n- The player with the most territory wins\n- To place the stone, tap on intersection of two lines on the grid',
            font=('Fontin', 15, 'bold'),
            height=25,
            fg='black'
        )
        self.instructions.pack()

        self.button = tk.Button(
                text="Start The Game",
                command=self.start,
                height=5,
                fg='#645F55',
                font=('Fontin', 20, 'bold'),  # Set font family, size, and weight
                bd=2,
                relief='raised',
            )
        self.button.pack(side='bottom')
        self.window.mainloop()
    
    def start(self):
        self.window.destroy()
        GUI()

class GUI:
    def __init__(self) -> 'GUI.start_game':
        """
        Game Of Go

        Rules:
            - Players take turns placing stones on the board
            - A player can pass their turn
            - A player can resign the game
            - A player can place a stone on an empty intersection
            - A player cannot place a stone on an intersection that is already occupied
            - A player cannot place a stone on an intersection that will result in a self-capture move
            - A player should occupy as much territory as possible
            - If two players pass their turns consecutively, the game ends
            - The player with the most territory wins
        """
        self.window = tk.Tk()
        self.window.attributes("-fullscreen", True)
        self.window.title("Go")
        self.window.configure(bg='#5f5c56')
        #creating variable to store buttons
        self.buttons = {}

        # Label for user to know what to do
        self.label = tk.Label(
            self.window,
            text='Choose the size of the board',
            height=2,
            font=('Fontin', 20, 'bold'),
            fg='black'
        )

        self.label.pack(side='top')

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)
        # Load image
        self.photo = ImageTk.PhotoImage(Image.open(resource_path('go.png')).resize((50,50)))

        # Options available for board size
        self.options = [x for x in range(5, 10)]

        # Create frames
        self.option_frame = tk.Frame(self.window, bg='#5f5c56')
        self.option_frame.pack(fill='both', expand=True)
        self.action = ''

        self.board_frame = tk.Frame(self.window, bg='#5f5c56')
        
        # Create option buttons
        row, col = 0, 0

        
        # Create buttons for each option for user to choose for board size
        for option in self.options:
            # Setting button properties
            button = tk.Button(
                self.option_frame,
                text=str(option),
                command=lambda opt=option: self.start_game(opt),
                width=10,
                height=5,
                fg='#645F55',
                font=('Fontin', 20, 'bold'),  # Set font family, size, and weight
                bd=2,
                relief='raised',
            )

            # Place button on grid
            button.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Configure grid
        for i in range(row + 1):
            self.option_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.option_frame.grid_columnconfigure(j, weight=1)

        self.window.mainloop()

    def start_game(self,option:int) -> 'GUI.gui_board':
        """
        Start the game with the selected option

        Parameters:
            - Option selected by the user
        Created:
            - Screen with the board
            - Buttons to pass and resign
            - Lines drawn on the board
            - Game Object
        """

        # Make label disappear
        self.label.pack_forget()
        # Frame for control buttons
        self.control_frame = tk.Frame(self.window, bg='#5f5c56')
        self.control_frame.pack(fill='x', pady=10)


        # Create pass and resign buttons
        pass_button = tk.Button(
            self.control_frame,
            text="Pass",
            command=self.pass_turn,
            width=10,
            height=2,
            fg='#645F55',
            font=('Fontin', 20, 'bold'),
            bd=2,
            relief='raised'
        )
        pass_button.pack(side='left', padx=10)

        resign_button = tk.Button(
            self.control_frame,
            text="Resign",
            command=self.resign,
            width=10,
            height=2,
            fg='#645F55',
            font=('Fontin', 20, 'bold'),
            bd=2,
            relief='raised'
        )

        resign_button.pack(side='right', padx=10)
        
        self.option_frame.pack_forget()
        self.board_frame.pack(fill='both', expand=True) 


        # Create canvas for the board
        self.canvas = tk.Canvas(
            self.board_frame,
            width=650,
            height=692,
            bg='#B58B3A'
        )
        self.canvas.pack(pady=20)
        self.cell_size = 600 // (option - 1)

        # Draw horizontal lines
        for i in range(option):
            self.canvas.create_line(20, 20 + i * self.cell_size, 20 + (option - 1) * self.cell_size, 20 + i * self.cell_size, fill='black', width=3, tags='line')

        # Draw vertical lines
        for i in range(option):
            self.canvas.create_line(20 + i * self.cell_size, 20, 20 + i * self.cell_size, 20 + (option - 1) * self.cell_size, fill='black', width=3, tags='line')


        # Create game object
        self.game = Go(option)

        # Calling function to constantly update the board
        self.gui_board(option)

    def gui_board(self,option:int):
        """
        Update the board with the current state of the game

        Parameters:
            - Option selected by the user
        Functions:
            - Create buttons for each cell
            - Place stones on the board
            - Update the board with the current state of the game
        """

        # Clear the canvas
        self.canvas.delete('!line')

        # Nested loop to create buttons for each cell
        for i in range(option):
            for j in range(option):
                # Check the board
                # Based on the board state place the stones and buttons
                if self.game.board[i][j] == 'x':
                    self.place_oval(i, j, 'black')
                elif self.game.board[i][j] == 'o':
                    self.place_oval(i, j, 'white')
                else:
                    button = tk.Button(
                            self.canvas,
                            width=0,
                            height=0,
                            relief='flat',
                            highlightthickness=0,
                            image=self.photo,
                            borderwidth=0,
                            command=lambda row=i, col=j: self.on_cross_section_click(row, col, option)
                        )
                    button.place(x=20 + j * self.cell_size-5, y=20 + i * self.cell_size-4, height=10, width=10)
                    # Add placed buttons in dict
                    # To be able to access them later
                    self.buttons[(i, j)] = button

    def on_cross_section_click(self,row:int, col:int, option:int):
        """
        Function to handle the click event on the buttons
        
        Parameters:
            - Row and Column of the button clicked
            - Option selected by the user
        Functions:
            - Move the stone to the selected position if it doesn't violate the rules
            - Update the board with the current state of the game
        """
        log_text = f"Button at row {row}, col {col} clicked"
        print(log_text)
        with open('log.txt', 'a') as f:
            f.write(log_text)
            f.write('\n')
        resp = self.game.move([row, col])
        if resp == self.game.SELF_CAPTURE:
            messagebox.showerror("Invalid Move", resp)
        self.action = 'move'
        self.game.present(self.game.board)
        self.gui_board(option)
    
    def place_oval(self,col:int, row:int, color:str):
        """
        Place the stone on the board
        
        Parameters:
            - Row and Column of the button clicked
            - Color of the stone
            
        Functions:
            - Create an oval on the board
            - Make button invisible

        Note:
            - Buttons are made invisible, so in case of capture the stones can be placed on the board again
        """

        # Calculate the center of the cell
        x_center = 20 + row * self.cell_size
        y_center = 20 + col * self.cell_size
        radius = self.cell_size // 4


        # Based on the calculations place the stone on the board
        self.canvas.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill=color
        )

        # Make the button invisible
        self.buttons[(col, row)].configure(bg=color, image='')

    def pass_turn(self):

        """
        Pass the turn to the next player
        """

        # Check if the player wants to pass the turn
        if self.confirmation('pass turn'):

            # Check if previous player has already passed the turn
            if self.action == 'pass':
                # If both players have passed the turn, end the game
                scores = (self.game.totalize())
                self.gui_board(self.game.h)
                if scores[0]>scores[1]:
                    result = "Black wins"
                elif scores[0]<scores[1]:
                    result = "White wins"
                else:
                    result = "Tie"
                messagebox.showinfo("Game Over", f"Black: {scores[0]}\nWhite: {scores[1]}\n{result}!")

                # Offer to play again
                self.play_again()
            else:

                # Pass the turn
                messagebox.showinfo("Pass", f"{self.game.turn.capitalize()} passed their turn!")
                self.game.pass_turn()
                self.action = 'pass'
    
    def play_again(self) -> 'GUI':
        """
        - Ask the user if they want to play again
        - Closes the current window and opens a new one if the user wants to play again
        """
        self.window.destroy()
        # Ensure that user wants to play again
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            return GUI()


    def resign(self) -> 'GUI.play_again':
        """
        Resign the game
        """
        # Ask for confirmation and check if agrees
        if self.confirmation("resign"):
            # If agrees, make opposite color the winner
            winner = "Black" if not(self.game.tcheck) else "White"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.play_again()



    def confirmation(self:classmethod, action:str) -> bool:
        """
        Ask for confirmation before taking any action
        """
        return messagebox.askyesno("Confirmation", f"Are you sure you want to {action}?")

class Go:

    def __init__(self, *args):

        """
        Core of the Game Of Go
        
        Parameters:
        *args: int
            The size of the board, if only one argument is given, the board will be a square
            if two arguments are given, the first will be the height and the second the width
            if no arguments are given, the board will be a 19x19 square
        """

        # Check if args parameter is given right
        if len(args)==2:
            self.h = args[0]
            self.w = args[1]
        elif len(args)==1:
            for a in args:
                self.h = int(a)
                self.w = int(a)

        # Based on given parameter(s) create the board
        self.size = {'height':self.h, 'width':self.w}
        self.board = [['.' for i in range(self.w)] for i in range(self.h)]

        # Initialize the game
        self.tcheck = True
        self.turn = 'black'
        self.SELF_CAPTURE = 'Cannot place a stone there, it will be a self-capture move'


    def present(self, board:list[list[int]]):

        """
        Present the board in a readable format
        """
        with open('log.txt', 'a') as f:
            for a in board:
                print(a)
                f.write(f'{a}')
                f.write('\n')

    def group(self, symbol:str) -> list:

        """
        Group the stones on the board based on symbol
        """
        groups = [] 
        row = 0

        # Nested loop to go through the board
        for r in self.board:
            col = 0
            group = []
            for s in r:
                # Check if current element is the same as the symbol
                if s==symbol:

                    # Variable to check if the current element is already included in a group
                    included = False
                    for g in groups:
                        # if it is included, skip the current element
                        if [row,col] in g:
                            included = True
                        # if not included:
                        if [row-1, col] in g or [row, col-1] in g:
                            back = symbol
                            g.append([row, col])
                            col_new = col

                            # Going back to check if stone is connected with other stones
                            while back==symbol:
                                if col_new-1<0:
                                    break
                                back = self.board[row][col_new-1]
                                if back!=s:
                                    break

                                # Append connected stones to the group
                                g.append([row, col_new-1])
                                for a in group:
                                    for b in g:
                                        if a==b:
                                            if b in group:
                                                group.remove(b)
                                col_new-=1
                            included = True
                    
                    # If the current element is not included in any group
                    if [row, col-1] not in group:
                        # And group is not empty
                        if group!=[]:
                            # Append the group to the groups list
                            # And make it empty
                            groups.append(group)
                        group=[]
                    if not included:
                        group.append([row, col])
                col += 1
            row += 1

            # If group is not empty and is left not appended, append it to the groups list
            if group!=[]:
                groups.append(group)
                
        groups = sorted(groups)
        return groups


    def check(self, symbol:str,check_sign:str) -> bool:

        """
        Check if the stones are captured or not

        Parameters:
            - symbol: str
                The symbol to check for
            - check_sign: str
                The sign to check from
        Output:
            - captured: bool
                If the stones are captured or not
        """

        # Get the groups
        groups = self.group(symbol)
        captured = False

        # Loop through the groups
        for g in groups:
            # If group is empty, skip
            if g==[]:
                continue

            # amount of blocked position of stones
            blocked = 0

            # Loop through each group in groups
            for pos in g:

                # Getting position of the stone
                row = pos[0]
                col = pos[1]

                # Add per 1 if the stone is blocked
                if row==0 or self.board[row-1][col]!=check_sign:
                    blocked += 1
                if row==len(self.board)-1 or self.board[row+1][col]!=check_sign:
                    blocked +=1
                if col==0 or self.board[row][col-1]!=check_sign:
                    blocked += 1
                if col==self.w-1 or self.board[row][col+1]!=check_sign:
                    blocked += 1

            # If blocked amount is equal to 4 times the length of the group
            # Then the stones are captured
            if blocked==len(g)*4:
                if (symbol == 'x' and self.tcheck) or (symbol == 'o' and (not(self.tcheck))):
                    return True
                for pos in g:
                    if check_sign=='x':
                        self.board[pos[0]][pos[1]] = 'o'
                    elif check_sign=='o':
                        self.board[pos[0]][pos[1]] = 'x'
                    else:
                        self.board[pos[0]][pos[1]] = '.'
                captured = True
        return captured


    def move(self, *args) -> 'Go':

        """
        Move the stones on the board
        
        Parameters:
        *args: int
            The position of the stone to move
        Output:
            - self: Go
                The updated board
        """
        for pos in args:

            # Get object on the position
            row = int(pos[0])
            col = int(pos[-1])
            obj = self.board[row][col]


            # If it is not a stone, place a stone
            if obj == '.':

                # Check for color of the stone
                match self.tcheck:
                    case True:
                        self.board[row][col] = 'x'
                        self.check('o', '.')
                        itself = self.check('x', '.')

                        # If it is a self-capture move, return a message
                        if itself:
                            self.board[row][col] = '.'
                            return self.SELF_CAPTURE
                        # Switch the turn
                        self.turn = 'white'
                        self.tcheck = False
                    case False:
                        # Same as above, but for white stones
                        self.board[row][col] = 'o'
                        self.check('x', '.')    
                        itself = self.check('o', '.')
                        if itself:
                            self.board[row][col] = '.'
                            return self.SELF_CAPTURE
                        self.turn = 'black'
                        self.tcheck = True
            else:
                continue
        return self 
    

    def pass_turn(self) -> 'Go':

        """
        Pass the turn to the other player
        """
        if self.tcheck:
            self.turn = 'white'
        else:
            self.turn = 'black'
        self.tcheck = not(self.tcheck)
        return self


    def totalize(self) -> list[int, int]:
        """
        Count total
        """

        # Initialize the total
        self.white_total = 0
        self.black_total = 0

        # Check for captured areas
        self.check('.', 'x')
        self.check('.', 'o')

        # Count the total using nested loop
        for row in self.board:
            for sign in row:
                if sign=='x':
                    self.black_total += 1
                elif sign=='o':
                    self.white_total += 1
        
        # Present the board to visualize what happened
        self.present(self.board)

        # Return the totals
        return self.black_total, self.white_total
 

if __name__ == '__main__':
    Start()