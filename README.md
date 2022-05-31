# StrategyGoAI
A simple engine for a classic strategy board game and AI to play it

StrategyGo.py
    The engine for the game itself. It's not meant to be run, just leave it alone.

Generation.py
    Handles all the generation of AI starting boards. It can be called with the following command lines:

        py generation.py gen [number] [AI] [AI] 
            Runs [number] generations of 100 games between the two [AI]
            I wouldn't suggest more than 10 generations, which will have to run overnight.
        
        py generation.py singleGame [AI] [AI]
            Runs a single game between the two AI and records the match. This will run on a default board.
        
        py generation.py runGames [AI] [AI] [Number]
            Runs [Number] games between the two [AI] and prints information about the games
        
    [AI] and their aliases (not case sensitive):
        Randotron: Randotron, Rando
        Lil Jimmy: LilJimmy, Jimmy, Jim
        
Interface.py
    The user interface to play games and watch replays, run this!

    run Interface.py with the flag -r to load in replay mode and -e to run it in edit (cheat) mode

    When run in play mode (default) you will play as red against an AI. You can input commands with
    moves formatted like this:
            [Space number of the unit you want to move]:[Space number of the target space]
    
    In any mode CTRL can be used to toggle peice display and space number display
    
