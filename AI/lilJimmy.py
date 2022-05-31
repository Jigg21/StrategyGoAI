from AI.AIBase import StrategyAI
import AI.BehaviorTree as BT
import AI.AIBase
import AI.Nodes

class Agent_lilJimmy(StrategyAI):
    def __init__(self,board,agentNumber, rootnode=None) -> None:
        super().__init__(board,agentNumber,rootnode)
        self.addRootNode(BT.SequenceNode("ROOT"))
        GetMoves = AI.Nodes.node_getValidMoves("Get Valid Moves")
        self.addNodetoRoot(GetMoves)
        civvyDec = BT.FinishDecorator("Finish")
        civvyDec.addChild(AI.Nodes.node_removeSuicidalMoves("Remove Suicidal Moves"))
        self.addNodetoRoot(civvyDec)
        MakeMove = AI.Nodes.node_choseRandomMove(desc="Make Random Move")
        self.addNodetoRoot(MakeMove)
    
    def __str__(self) -> str:
        return "Lil Jimmy"

