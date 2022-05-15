from tracemalloc import start
import Stratego
import random
from progress.bar import FillingSquaresBar
player2Board = "2B02B02602602B02602302702802802302302402402202402702902202102502502502402302702702502002B02602702802802802802802802B02A0"
generationNumber = 0
childNumber = 0
def runGames(board,op1,op2,count):
    Player1Win = 0
    Player2Win = 0
    global generationNumber
    global childNumber
    childNumber += 1
    with FillingSquaresBar("Testing {age}.{child}: ".format(age=generationNumber,child=childNumber),max=count,suffix='%(index)d/%(max)d') as bar:
        for i in range (count):
            result = Stratego.runGame(op1,op2,board)
            if result == 1:
                Player1Win += 1
            elif result == 2:
                Player2Win += 1
            bar.next()
        bar.finish()
        
    
    print("Player 1 won {win} games ({pct})".format(win=Player1Win,pct=Player1Win/count))
    print("Player 2 won {win} games ({pct})".format(win=Player2Win,pct=Player2Win/count))
    return (Player1Win,Player2Win)


def makeStartingBoard(player1,player2):
    return player1 + "000000WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW000000" + player2

def mutateStart(board):
    i = random.randrange(0,40)
    n = random.randrange(0,40)
    spacei = board[i*3:(i*3)+3]
    spacen = board[n*3:(n*3)+3]
    if i == n:
        return board
    elif i < n :
        board = board[:i*3] + spacen + board[(i*3+3):n*3] + spacei + board[(n*3)+3:]
        return board
    else:
        board = board[:n*3] + spacei + board[(n*3+3):i*3] + spacen + board[(i*3)+3:]
        return board

def makeGeneration(fam1,fam2,fam3):
    generation = list()
    generation.append(fam1)
    generation.append(fam1)
    generation.append(mutateStart(fam1))
    generation.append(mutateStart(fam1))
    generation.append(fam2)
    generation.append(mutateStart(fam2))
    generation.append(mutateStart(fam2))
    generation.append(fam3)
    generation.append(mutateStart(fam3))
    generation.append(mutateStart(fam3))
    return generation

def runMilestoneGame(board,op1,op2):
    Stratego.runGame(op1,op2,board,record=True)

def getMaxDictEntry(d):
    maxVal = 0
    maxKey = ""
    for entry in d:
        if d[entry] > maxVal:
            maxVal = d[entry]
            maxKey = entry
    return (maxKey,maxVal)

def main():
    #generate a starting generation
    gen1Start = "1301701701701601B01A01B01501701301801301901401001B01601501801601801101201201801601B01B01B0150140150170180140180180180140"
    generation = makeGeneration(gen1Start,gen1Start,gen1Start)
    #for 5 generations
    for age in range(100):
        global generationNumber
        generationNumber += 1
        print("STARTING GENERATION: {age} ".format(age=age+1))
        childWinRates = dict()
        #each child plays 100 games, the best 3 are chosen for the next generation
        for child in generation:
            results = runGames(makeStartingBoard(child,player2Board),Stratego.OPPONENTS.RANDOTRON,Stratego.OPPONENTS.RANDOTRON,100)
            childWinRates[child] = results[0]
            
        max1 = getMaxDictEntry(childWinRates)
        childWinRates[max1[0]] = 0
        runMilestoneGame(makeStartingBoard(child,player2Board),Stratego.OPPONENTS.RANDOTRON,Stratego.OPPONENTS.RANDOTRON)
        max2 = getMaxDictEntry(childWinRates)
        childWinRates[max2[0]] = 0
        max3 = getMaxDictEntry(childWinRates)
        print("Top 3:")
        print("{board}:{wins} wins".format(board=max1[0],wins=max1[1]))
        print("{board}:{wins} wins".format(board=max2[0],wins=max2[1]))
        print("{board}:{wins} wins".format(board=max3[0],wins=max3[1]))
        generation = makeGeneration(max1[0],max2[0],max3[0])

def runGamesOnDefaultBoard(op1,op2,count):
    gen1Start = "1301701701701601B01A01B01501701301801301901401001B01601501801601801101201201801601B01B01B0150140150170180140180180180140"
    runGames(makeStartingBoard(gen1Start,player2Board),op1,op2,count)

def recordGameOnDefaultBoard(op1,op2):
    gen1Start = "1301701701701601B01A01B01501701301801301901401001B01601501801601801101201201801601B01B01B0150140150170180140180180180140"
    runMilestoneGame(makeStartingBoard(gen1Start,player2Board),op1,op2)


recordGameOnDefaultBoard(Stratego.OPPONENTS.LILJIMMY,Stratego.OPPONENTS.RANDOTRON)