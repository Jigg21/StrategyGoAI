from cgi import test
from cmath import exp
from msilib.schema import TextStyle
from multiprocessing import context
import tkinter as tk
from tkinter import filedialog
from tokenize import Number
import Stratego
import time

updateFullInfo = False
displayPlayer = "0"
ReplayMode = True
Numbering = False

class BoardDisplay(tk.Frame): 
    def __init__(self,parent):
        self.parent = parent
        super(BoardDisplay,self).__init__(parent,width=30,height=1)
        self.board = list()
        self.boardOBJ = tk.Frame(parent)
        for i in range (10):
            rowOBJ = tk.Frame(self.boardOBJ,padx=0,pady=0)
            for n in range (10):
                space = SimpleTextObj(rowOBJ,height=1,width=3,side="left")
                space.updateSpace('{:0>3}'.format(i*10 + n))
                space.pack(side="left",padx=0,pady=0)
                self.board.append(space)
            rowOBJ.pack(side="bottom",padx=0,pady=0)
        self.boardOBJ.pack()
    
    def updateBoard(self,newBoard):
        for i in range (100):
            code = newBoard[i*3:(i*3)+3]
            self.board[i].updateSpace(code)
    
    def numberBoard(self):
        for i in range (100):
            code = i
            self.board[i].numberSpace(code)
        
class gameReplay():
    '''object to handle replays'''
    def __init__(self,file = None) -> None:
        self.turn = 0
        self.moves = []
        self.turns = []
        self.startBoard = ""
        #open file and get info
        if file != None:
            with open(file,"r") as f:
                self.startBoard = f.readline()
                self.moves = f.readlines()
            #create a board and find board state after each move
            self.boardOBJ = Stratego.Board(self.startBoard)
            playerid = "1"
            for move in self.moves:
                move = move.split(":")
                self.boardOBJ.makeMove(int(move[0]),int(move[1]),playerid)
                self.turns.append(self.boardOBJ.getBoard())
                if playerid == "1":
                    playerid = "2"
                else:
                    playerid = "1"
    
    def next(self):
        '''Progress game by one turn and returns the board'''
        if (self.turn + 1 < len(self.turns)):
            self.turn += 1
            return self.turns[self.turn]
        else:
            return -1
    
    def prev(self):
        '''Regress game by one turn and returns the board'''
        if (self.turn - 1 >= 0):
            self.turn -= 1
            return self.turns[self.turn]
        else:
            return self.turns[self.turn]

#Buildings Display

class SimpleTextObj(tk.Frame):
    def __init__(self,parent,height=1,width=1,side='top',padx=0,pady=0):
        self.parent = parent
        super(SimpleTextObj,self).__init__(parent,width=width,height= height,padx=padx,pady=pady)
        
        self.text = tk.Text(parent,height=height,width=width,padx=padx,pady=pady)
        self.text.pack(expand=False,side=side,padx=padx)

    
    def numberSpace(self,number):
        self.text.delete("1.0",tk.END)
        self.text.insert(tk.INSERT,number)


    #takes string from console and displays it
    def updateSpace(self,code):
        self.text.delete("1.0",tk.END)
        if (updateFullInfo):
            if code[0] != displayPlayer and displayPlayer != "0" and code[0] != "0":
                self.text.insert(tk.INSERT,"???")
            else:
                self.text.insert(tk.INSERT,code)
        else:
            if code[0] != displayPlayer and displayPlayer != "0" and code[0] != "0":
                self.text.insert(tk.INSERT,"?")
            else:
                self.text.insert(tk.INSERT,code[1])
        
        if (code == "WWW"):
            self.text.configure(foreground="Blue",background="Blue")

        if (code[0] == "0"):
            self.text.configure(foreground="black")
        if (code[0] == "1" ):
            self.text.configure(foreground="red")
        if (code[0] == "2"):
            self.text.configure(foreground="blue")
        self.text.pack(expand=False)

def enterInput(event = None):
    inp = inputText.get(1.0, "end-1c")
    if (event != None):
        inp = inp[0:len(inp)-1]
    inputText.delete(0.0,'end')
    #TODO: Handle invalid moves
    global board
    Stratego.parseUserInput(inp,board)
    context = dict()
    context["boardState"] = board.getBoard()
    context["playerNumber"] = "2"
    context["Verbose"] = False
    Stratego.loadOpponent(Stratego.OPPONENTS.RANDOTRON,board,"2").activate(context)
    update(board.getBoard())


def numberToggle(event = None):
    global board
    global Numbering
    if Numbering:
        boardDisplay.numberBoard()
        Numbering = False
    else:
        boardDisplay.updateBoard(board.getBoard())
        Numbering = True

def replayNext():
    global displayGame
    next = displayGame.next()
    if next != -1:
        update(next)

def replayPrev():
    global displayGame
    prev = displayGame.prev()
    if prev != -1:
        update(prev)

def playReplay():
    global displayGame
    global root
    next = displayGame.next()
    if next != -1:
        update(next)
        root.after(1,playReplay)    

def loadGame():
    '''loads a game from filepath and returns a game object'''
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Open a game replay file",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    global displayGame
    displayGame = gameReplay(filename)

def update(boardState):
    boardDisplay.updateBoard(boardState)

def main():
    print("DONE")
    #initialize board
    boardDisplay.updateBoard(board.getBoard())
    root.mainloop()


root = tk.Tk()
root.geometry('400x200')
root.title("Stratego")
root.bind('<Return>',enterInput)
root.bind('<Control_L>',numberToggle)
boardDisplay = BoardDisplay(root)
boardDisplay.pack()
if (not ReplayMode):
    inputText = tk.Text(root,height=1,width=20)
    inputText.pack()
    enterButton = tk.Button(root,text = "Enter Move",command= enterInput)
    enterButton.pack()
else:
    replayConsole = tk.Frame(root)
    replayConsole.pack()
    prevButton = tk.Button(replayConsole,text = "Prev",command= replayPrev)
    prevButton.pack(side="left")
    loadButton = tk.Button(replayConsole,text = "Load File",command= loadGame)
    loadButton.pack(side="left")
    nextButton = tk.Button(replayConsole,text = "Next",command= replayNext)
    nextButton.pack(side="right")
    playButton = tk.Button(replayConsole,text = "Play",command= playReplay)
    playButton.pack(side="bottom")


board = Stratego.Board("1301701701701601B01A01B01B01701301801301901401501B01601501801601801201201101801601B01B0150100140150170180140180180180140000000WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW0000002B02B02602602B02602302702802802302302402402202402702902202102502502502402302702702502002B02602702802802802802802802B02A0")
displayGame = gameReplay()
main()
