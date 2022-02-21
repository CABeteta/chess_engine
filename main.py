import graphics
import chess
import time

myBoard = graphics.BoardGraph()
myBoard.movePiece("D2", "D3")
myBoard.updateBoard()
time.sleep(0.5)

myBoard.movePiece("D7", "D6")
myBoard.updateBoard()
time.sleep(0.5)

myBoard.movePiece("C1", "F4")
myBoard.updateBoard()
time.sleep(0.5)

myBoard.movePiece("B8", "C6")
myBoard.updateBoard()
time.sleep(0.5)

myBoard.movePiece("E2", "E3")
myBoard.updateBoard()
time.sleep(0.5)

myBoard.movePiece("G7", "G6")
myBoard.updateBoard()
time.sleep(0.5)

print("done")
