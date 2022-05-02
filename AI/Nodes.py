from contextvars import Context
from ctypes.wintypes import tagRECT
from operator import index
from sre_constants import SUCCESS
import AI.BehaviorTree as BT
import random

import Stratego


# "boardState" = Board string
# "playerNumber" = player number
class node_getValidMoves(BT.Node):
  def __init__(self, desc="") -> None:
      super().__init__(desc)
    
  def activate(self, context) -> BT.nodeStates:
      super().activate(context)
      moveList = list()
      board = context["boardState"]
      boardObj = Stratego.Board(board)
      #for each space on the board
      for i in range(100):
        space = board[i*3:(i*3)+3] 
        #if the space contains one of this players unit
        if (space[0] == context["playerNumber"]):
          #if it's moveable
          if (space[1] != "A" and space[1] != "B"):
              #left
              for n in range(1,10):
                if boardObj.checkMoveLegality(i,i-n,context["playerNumber"]):
                  moveList.append("{unit}:{target}".format(unit=i,target=i-n))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if space[1] != "8" or space[0] != target[0] and target[0] == "0":
                    break
                else:
                  break

              #right
              for n in range(1,10):
                if boardObj.checkMoveLegality(i,i+n,context["playerNumber"]):
                  moveList.append("{unit}:{target}".format(unit=i,target=i+n))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if space[1] != "8" or space[0] != target[0] and target[0] == "0":
                    break
                else:
                  break
              
              #Down
              for n in range(1,10):
                if boardObj.checkMoveLegality(i,i-(10*n),context["playerNumber"]):
                  moveList.append("{unit}:{target}".format(unit=i,target=i-(10*n)))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if space[1] != "8" or space[0] != target[0] and target[0] == "0":
                    break
                else:
                  break
              
              #Up
              for n in range(1,10):
                if boardObj.checkMoveLegality(i,i+(n*10),context["playerNumber"]):
                  moveList.append("{unit}:{target}".format(unit=i,target=i+(10*n)))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if space[1] != "8" or space[0] != target[0] and target[0] == "0":
                    break
                else:
                  break
      if len(moveList) == 0:
        print("No Moves")
        return BT.nodeStates.FAILED
      else:
        context["ValidMoves"] = moveList
        return BT.nodeStates.SUCCESS

  def isSpaceMoveable(self,board,index,playerNumber):
    if index < 0 or index >= 100:
      return False
    space = board[(index*3):(index*3)+3][0]
    return space[0] == "0" or playerNumber != space[0]

class node_choseRandomMove(BT.Node):
  def __init__(self, desc="") -> None:
      super().__init__(desc)
  
  def activate(self, context) -> BT.nodeStates:
      super().activate(context)
      chosenMove = context["ValidMoves"][random.randrange(0,len(context["ValidMoves"]))]
      context["Move"] = chosenMove
      return BT.nodeStates.SUCCESS