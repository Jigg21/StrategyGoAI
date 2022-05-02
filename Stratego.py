from fileinput import filename
from operator import truediv
import Utilities
import AI.RandoTron
from enum import Enum
import time


class Board ():
    def __init__(self,startBoard="") -> None:
        self.winner = 0
        #initialize an empty board
        if startBoard == "":
            self.board = "000"*42 + "WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW" + "000"*42
        else:
            self.board = startBoard
        self.cheat = False

    #Set board to empty
    def ClearBoard (self):
        self.board = "000"*42 + "WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW" + "000"*42
    
    def getBoard(self):
        '''returns the board in its raw string form'''
        return self.board
    
    def cheatMode(self,value):
        self.cheat = True
    
    def isCheating(self):
        return self.cheat
    
    def getWinner(self):
        '''returns the number of the player that won, returns 0 if the game is still going'''
        return self.winner
    
    #return the data for space 1-100
    def getSpace(self,index):
        return self.board[index*3:(index*3)+3]
    
    def changeSpace(self,index,newState):
        '''Changes the state of the space at index to newState'''
        if len(newState) != 3:
            raise ValueError
        
        self.board = Utilities.stitchString(self.board,index*3,newState)

    def checkDirect(self,source,target):
        '''check if the move is a straight line'''

        if abs(source-target)%10 == 0:
            return True
        if source//10 == target //10:
            return True
        return False
    
    def checkMoveLegality (self,sourceIndex,targetIndex,player,verbose=False):
        '''checks to see if a proposed move is legal'''
        if sourceIndex > 99 or sourceIndex < 0 or targetIndex > 99 or targetIndex < 0:
            return False
        unit = self.getSpace(int(sourceIndex))
        target = self.getSpace(targetIndex)
        #false if the unit is stationary
        if unit[1] == "A" or unit[1] == "B":
            return False

        #false if the move is diagonal
        if not self.checkDirect(sourceIndex,targetIndex):
            if verbose:
                print("NOT DIRECT {source}|{unit}:{target}|{targetUnit}".format(source=sourceIndex, unit=unit, target=targetIndex,targetUnit=target))
            return False
        
        #false if the unit is not the players unit
        if unit[0] != player:
            if verbose:
                print("NOT YOURS {source}|{unit}:{target}|{targetUnit}".format(source=sourceIndex, unit=unit, target=targetIndex,targetUnit=target))
            return False
        
        #false if the unit is not a scout and moves more than one space
        if unit[1] != "8":
            if abs(sourceIndex-targetIndex) != 1 and abs(sourceIndex-targetIndex) != 10:
                if verbose:
                    print("TOO FAR {source}|{unit}:{target}|{targetUnit}".format(source=sourceIndex, unit=unit, target=targetIndex,targetUnit=target))
                return False
        
        #false if the unit tries to move to a water space
        if target[1] == "W":
            if verbose:
                print("WET {source}|{unit}:{target}|{targetUnit}".format(source=sourceIndex, unit=unit, target=targetIndex,targetUnit=target))
            return False
        
        #false if the unit tries to move on top of a friendly unit
        if unit[0] == target[0]:
            if verbose:
                print("ANOTHER UNIT IS THERE {source}|{unit}:{target}|{targetUnit}".format(source=sourceIndex, unit=unit, target=targetIndex,targetUnit=target))
            return False

        return True

    def makeMove(self,sourceIndex,targetIndex,player):
        if self.checkMoveLegality(sourceIndex,targetIndex,player):
            unit = self.getSpace(sourceIndex)
            target = self.getSpace(targetIndex)
            self.changeSpace(sourceIndex,"000")
            #if the target square is empty, change the square, else resolve battle
            if target[0] == "0":
                self.changeSpace(targetIndex,unit)
            #if its the flag, the game is over
            elif target[1] == "A":
                self.winner = unit[0]
                self.changeSpace(targetIndex,unit)
            elif target[1] == "B":
                if unit[1] == "7":
                    self.changeSpace(targetIndex,unit)
            #if the unit wins move the unit onto the target space and reveal the unit
            elif unit[1] < target[1] or (unit[1] == "9" and target[1]=="0") :
                self.changeSpace(targetIndex,unit[0:2]+"1")
            #if tie, both are destroyed, otherwise the target is revealed 
            elif unit[1] == target[1]:
                self.changeSpace(targetIndex,"000")
            else:
                self.changeSpace(targetIndex,target[0:2]+"1")
        else:
            print("ILLEGAL MOVE")

    def __str__(self) -> str:
        return self.board

class BoardDisplay():
    def __init__(self) -> None:
        pass
    

    def displayBoard(self,boardObj, fullDisplay = False):
        displayString = ""
        for row in range(0,10):
            for col in range(0,10):
                space = boardObj.getSpace((row*10)+col)
                if space[2] == "0" and (space[0] == "2" and not boardObj.isCheating()):
                    displayString += " XXX "
                elif fullDisplay:
                    displayString += " " + space + " "
                else:
                    displayString += " " + space[1] + " "
            displayString += "\n"
        print (displayString)

class OPPONENTS(Enum):
    RANDOTRON = 0

def parseUserInput(userInput, board):
    '''takes input and parses the command, then returns the new board, player is always assumed to be player 1'''
    if (userInput == "return"):
        print(board.getBoard())
        return board.getBoard()
    if (userInput == "cheatOn"):
        board.cheatMode(True)
        return board.getBoard()
    

    userInput = userInput.split(":")
    
    
    if userInput[0][0] == "c" or userInput[0][0] == "C" :
        board.changeSpace(int(userInput[0][1:]),userInput[1])
        return board.getBoard()
    board.makeMove(int(userInput[0]),int(userInput[1]),"1")
    return board.getBoard()

def parseAgentInput(input,board,agentNumber):
    input = input.split(":")
    board.makeMove(int(input[0]),int(input[1]),agentNumber)
    return board.getBoard()

def runGame(Player1,Player2,startingBoard):
    '''runs a game between two ai opponents with a given starting board, returns an int to describe which ai won'''
    gameBoard = Board(startingBoard)
    try:
        Player1 = loadOpponent(Player1,gameBoard,"1")
        Player2 = loadOpponent(Player2,gameBoard,"2")
    except:
        print("FAILED TO INITIALIZE OPPONENTS, ABORTING")
        return -1

    gameFile = open("./Replays/SGR_{Op1}_{Op2}_{time}.txt".format(Op1=Player1,Op2=Player2,time=int(time.time())),"w")
    gameFile.write(startingBoard + "\n")
    turnCount = 0
    while True:
        turnCount += 1
        context = dict()
        context["boardState"] = gameBoard.getBoard()
        context["playerNumber"] = "1"
        context["Verbose"] = False
        if (not Player1.activate(context)):
            #player 2 wins
            print("PLAYER @ WINS")
            gameFile.close()
            return 2
        gameFile.write(context["Move"] + "\n")

        context = dict()
        context["boardState"] = gameBoard.getBoard()
        context["playerNumber"] = "2"
        context["Verbose"] = False
        if (not Player2.activate(context)):
            #player 1 wins
            print("PLAYER ! WINS")
            gameFile.close()
            return 1
        gameFile.write(context["Move"]+"\n")
        
        if gameBoard.getWinner() != 0:
            gameFile.close()
            return gameBoard.getWinner()
        
        #game has gone on too long, ending in a tie
        if turnCount > 10000:
            return -1
        else:
            pass
    
def loadOpponent(opponentType,gameBoard,playerNumber):
    '''Takes an enum and returns the strategoAI object to match'''
    if (opponentType == OPPONENTS.RANDOTRON):
        return AI.RandoTron.Agent_RandoTron(gameBoard,playerNumber)
    else:
        raise ValueError
        
def main():
    runGame(OPPONENTS.RANDOTRON,OPPONENTS.RANDOTRON,"1301701701701601B01A01B01B01701301801301901401501B01601501801601801201201101801601B01B0150100140150170180140180180180140000000WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW0000002B02B02602602B02602302702802802302302402402202402702902202102502502502402302702702502002B02602702802802802802802802B02A0")

if __name__ == "__main__":
    main()
