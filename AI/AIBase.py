from contextlib import ContextDecorator
from AI.BehaviorTree import nodeStates
import StrategyGo
import AI.BehaviorTree as BT

class StrategyAI(BT.Tree):
    def __init__(self,board,agentNumber, rootnode=None) -> None:
        super().__init__(rootnode)
        self.board = board
        self.agentNumber = agentNumber

    def activate(self, context):
        if super().activate(context) == BT.nodeStates.FAILED:
            return False
        StrategyGo.parseAgentInput(context["Move"],self.board,self.agentNumber)
        return True
    
    def __str__(self) -> str:
        return "Stratego Base AI"


class moveOBJ():
    def __init__(self,source,target) -> None:
        self.source = source
        self.target = target
        self.value = 0

    def getSource(self):
        return self.source
    
    def getTarget(self):
        return self.target


    def __str__(self) -> str:
        return str(self.source) + ":" + str(self.target)