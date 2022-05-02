from contextlib import ContextDecorator
from AI.BehaviorTree import nodeStates
import Stratego
import AI.BehaviorTree as BT

class StrategoAI(BT.Tree):
    def __init__(self,board,agentNumber, rootnode=None) -> None:
        super().__init__(rootnode)
        self.board = board
        self.agentNumber = agentNumber

    def activate(self, context):
        if super().activate(context) == BT.nodeStates.FAILED:
            return False
        Stratego.parseAgentInput(context["Move"],self.board,self.agentNumber)
        return True
    
    def __str__(self) -> str:
        return "Stratego Base AI"