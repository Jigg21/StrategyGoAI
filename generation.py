import Stratego

def runGames(count):
    Player1Win = 0
    Player2Win = 0
    for i in range (count):
        result = Stratego.runGame(Stratego.OPPONENTS.RANDOTRON,Stratego.OPPONENTS.RANDOTRON,"1301701701701601B01A01B01B01701301801301901401501B01601501801601801201201101801601B01B0150100140150170180140180180180140000000WWWWWW000000WWWWWW000000000000WWWWWW000000WWWWWW0000002B02B02602602B02602302702802802302302402402202402702902202102502502502402302702702502002B02602702802802802802802802B02A0")
        if result == 1:
            Player1Win += 1
        elif result == 2:
            Player2Win += 1
    
    print("Player 1 won {win} games ({pct})".format(win=Player1Win,pct=Player1Win/count))
    print("Player 2 won {win} games ({pct})".format(win=Player2Win,pct=Player2Win/count))

runGames(1000)