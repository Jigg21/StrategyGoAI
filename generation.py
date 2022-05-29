from tracemalloc import start
import sys
from xml.etree.ElementPath import ops
import Stratego
import random
from progress.bar import FillingSquaresBar

player1Board = "1301701701701601B01A01B01501701301801301901401001B01601501801601801101201201801601B01B01B0150140150170180140180180180140"
player2Board = "2B02B02602602B02602302702802802302302402402202402702902202102502502502402302702702502002B02602702802802802802802802B02A0"
generationNumber = 0
childNumber = 0
class SelectionInfoObj():
    def __init__(self) -> None:
        self.player1Wins = 0
        self.player1WinsbyCapture = 0
        self.player2Wins = 0
        self.player2WinsbyCapture = 0
        self.gameCount = 0

    def getWins(self):
        return (self.player1Wins,self.player2Wins)

    def parseGame(self,replay):
        self.gameCount += 1
        if replay.winner == 1:
            self.player1Wins += 1
            if replay.wasCapture:
                self.player1WinsbyCapture += 1
        elif replay.winner == 2:
            self.player2Wins += 1
            if replay.wasCapture:
                self.player2WinsbyCapture += 1

    def __str__(self) -> str:
        result = ""
        result += "Player 1 won {win} games ({pct})\n".format(win=self.Player1Win,pct=self.Player1Win/self.gameCount)
        result += "Player 2 won {win} games ({pct})\n".format(win=self.Player2Win,pct=self.Player2Win/self.gameCount)

def runGames(board,op1,op2,count):
    Player1Win = 0
    Player2Win = 0
    global generationNumber
    global childNumber
    childNumber += 1
    selectionInfo = SelectionInfoObj()
    #run the games and send them to the selection info object, updating the progress bar as it goes
    with FillingSquaresBar("Testing {age}.{child}: ".format(age=generationNumber,child=childNumber),max=count,suffix='%(index)d/%(max)d') as bar:
        for i in range (count):
            result = Stratego.runGame(op1,op2,board)
            selectionInfo.parseGame(result)
            bar.next()
        bar.finish()
        
    
    print (selectionInfo)
    return selectionInfo

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
    return Stratego.runGame(op1,op2,board,record=True)

def getMaxDictEntry(d):
    maxVal = 0
    maxKey = ""
    for entry in d:
        if d[entry] > maxVal:
            maxVal = d[entry]
            maxKey = entry
    return (maxKey,maxVal)

def runGenerations(numberOfGenerations,op1,op2):
    #generate a starting generation
    genAStart = "1A01B01B01B01B01B01B0190180180180180180180180180170170170170170160160160160150150150150140140140140130130130120120110100"
    genBStart = "2002102202202302302302402402402402502502502502602602602602702702702702702802802802802802802802802902B02B02B02B02B02B02A0"
    generationAlpha = makeGeneration(genAStart,genAStart,genAStart)
    generationBeta = makeGeneration(genBStart,genBStart,genBStart)
    #for 100 generations
    for age in range(numberOfGenerations):
        global generationNumber
        generationNumber += 1
        print("STARTING GENERATION: {age} ".format(age=age+1))
        childWinRates = dict()
        #each child plays 100 games, the best 3 are chosen for the next generation
        for child in generation:
            results = runGames(makeStartingBoard(child,player2Board),op1,op2,100)
            childWinRates[child] = results.getWins[0]
            
        max1 = getMaxDictEntry(childWinRates)
        childWinRates[max1[0]] = 0
        runMilestoneGame(makeStartingBoard(max1[0],player2Board),op1,op2)
        max2 = getMaxDictEntry(childWinRates)
        childWinRates[max2[0]] = 0
        max3 = getMaxDictEntry(childWinRates)
        print("Top 3:")
        print("{board}:{wins} wins".format(board=max1[0],wins=max1[1]))
        print("{board}:{wins} wins".format(board=max2[0],wins=max2[1]))
        print("{board}:{wins} wins".format(board=max3[0],wins=max3[1]))
        generation = makeGeneration(max1[0],max2[0],max3[0])

def runGamesOnDefaultBoard(op1,op2,count):
    runGames("1A01B01B01B01B01B01B0190180180180180180180180180170170170170170160160160160150150150150140140140140130130130120120110100000000WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW000000200210220222302302302402402402402502502502502602602602602702702702702702802802802802802802802802902B02B02B02B02B02B02A0",op1,op2,count)

def recordGameOnDefaultBoard(op1,op2):
    runMilestoneGame("1A01B01B01B01B01B01B0190180180180180180180180180170170170170170160160160160150150150150140140140140130130130120120110100000000WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW000000200210220222302302302402402402402502502502502602602602602702702702702702802802802802802802802802902B02B02B02B02B02B02A0",op1,op2)

def parseEnums(opStr):
    str.upper(opStr)
    if opStr == "RANDOTRON" or opStr == "RANDO":
        return Stratego.OPPONENTS.RANDOTRON
    if opStr == "LILJIMMY" or opStr == "JIMMY":
        return Stratego.OPPONENTS.LILJIMMY
    else:
        print("UNKNOWN OPPONENT")
        raise ValueError

def main(argv):
    if len(argv) == 0:
        print("Command line tool help!")
        print("- gen [number] to run a number of generations")
        print("- singleGame [Opponent1] [Opponent2] to run a default game between two opponents")
        return
    if argv[0] == "gen":
        if len(argv) == 1:
            raise ValueError
        gens = int(argv[1])
        print(gens)
        #runGenerations(gens)
        return
    if argv[0] == "singleGame":
        if len(argv) != 3:
            raise ValueError
        else:
            op1 = parseEnums(argv[1])
            op2 = parseEnums(argv[2])
            
            replay = recordGameOnDefaultBoard(op1,op2)
            print(replay)



if __name__ == "__main__":
    main(sys.argv[1:])