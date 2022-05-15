from contextvars import Context
from ctypes.wintypes import tagRECT
from operator import index, truediv
from sre_constants import SUCCESS
from AI.AIBase import moveOBJ
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
      validMoves = list()
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
                  validMoves.append(moveOBJ(i,i-n))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if self.isSpaceMoveable(space,target):
                    break
                else:
                  break

              #right
              for n in range(1,10):
                if boardObj.checkMoveLegality(i,i+n,context["playerNumber"]):
                  moveList.append("{unit}:{target}".format(unit=i,target=i+n))
                  validMoves.append(moveOBJ(i,i+n))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if self.isSpaceMoveable(space,target):
                    break
                else:
                  break
              
              #Down
              for n in range(1,10):
                if boardObj.checkMoveLegality(i,i-(10*n),context["playerNumber"]):
                  moveList.append("{unit}:{target}".format(unit=i,target=i-(10*n)))
                  validMoves.append(moveOBJ(i,i-(10*n)))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if self.isSpaceMoveable(space,target):
                    break
                else:
                  break
              
              #Up
              for n in range(1,10):
                if boardObj.checkMoveLegality(i,i+(n*10),context["playerNumber"]):
                  moveList.append("{unit}:{target}".format(unit=i,target=i+(10*n)))
                  validMoves.append(moveOBJ(i,i+(10*n)))
                  target = board[(i-n)*3:((i-n)*3)+3] 
                  if self.isSpaceMoveable(space,target):
                    break
                else:
                  break
      #no valid moves, game over
      if len(moveList) == 0:
        if context["Verbose"]:
          print("No Moves")
        return BT.nodeStates.FAILED
      else:
        context["ValidMoves"] = validMoves
        return BT.nodeStates.SUCCESS

  def isSpaceMoveable(self,unit,target):
    if len(unit) < 3:
      return False
    if len(target) < 3:
      return False
    if unit[1] != "8" or unit[0] != target[0] and target[0] == "0":
      return True
    return False

class node_choseRandomMove(BT.Node):
  def __init__(self, desc="") -> None:
      super().__init__(desc)
  
  def activate(self, context) -> BT.nodeStates:
      super().activate(context)
      chosenMove = context["ValidMoves"][random.randrange(0,len(context["ValidMoves"]))]
      context["Move"] = str(chosenMove)
      return BT.nodeStates.SUCCESS

class node_removeSuicidalMoves(BT.Node):
  def activate(self, context) -> BT.nodeStates:
      super().activate(context)
      moves = context["ValidMoves"]
      boardstr = context["boardState"]
      board = Stratego.Board(boardstr)
      newMoveList = list()
      #remove any move that results in death
      for move in moves:
        unit = board.getSpace(move.getSource())
        target = board.getSpace(move.getTarget())
        if not self.willUnitDie(unit,target):
          newMoveList.append(move)
      if (len(newMoveList) > 0):
        context["ValidMoves"] = newMoveList
        return BT.nodeStates.SUCCESS
      else:
        return BT.nodeStates.FAILED

  def willUnitDie(self,unit,target):
    #empty
    if target[0]=="0":
        return False
    #target is unknown
    elif target[2] == "0":
        return False
    #bombs
    elif target[1] == "B":
        if unit[1] == "7":
            return False
        else:
            return True
    #the flag
    elif target[1] == "A":
        return False
    #combat
    elif int(target[1]) <= int(target[1]):
        if target[1] == "0" and unit[1] == 9:
            return False
        else:
            return True
    else:
        return False