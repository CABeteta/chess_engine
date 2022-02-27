import graphics
import pygame as p
import chess as c
import time

def main():
    myBoardWindow = graphics.BoardGraph()
    myBoard = c.Board()
    running = True

    InitialSquare = "."
    FinalSquare = "."
    currentMove = ".."

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                click_location = p.mouse.get_pos() # (x, y) of the mouse
                if(e.button == p.BUTTON_LEFT):
                    if InitialSquare == ".":
                        InitialSquare = myBoardWindow.getSquareFromXY(click_location)
                        if (myBoard.turn == myBoardWindow.pieceColor(InitialSquare) and myBoardWindow.squareIsEmpty(InitialSquare)==False) :
                            myBoardWindow.selectSquare(InitialSquare)
                            #print("InitialSquare: "+InitialSquare)
                        else:
                            InitialSquare="."
                            #print("Tried to select a wrong square")
                    else:
                        FinalSquare = myBoardWindow.getSquareFromXY(click_location)
                        currentMove = InitialSquare.lower()+FinalSquare.lower()
                        if InitialSquare == FinalSquare :
                            #print("Piece dropped.")
                            InitialSquare="." # So the loop starts again
                            FinalSquare="."
                            myBoardWindow.selectSquare(InitialSquare) #Unselects
                        elif c.Move.from_uci(currentMove) in myBoard.legal_moves:
                            myBoard.push_uci(currentMove)
                            myBoardWindow.movePiece(InitialSquare, FinalSquare)
                            myBoardWindow.updateBoard()
                            #print("FinalSquare: "+FinalSquare)
                            InitialSquare="." # So the loop starts again
                            FinalSquare="."
                            if myBoard.is_checkmate() :
                                print("Checkmate!")
                            elif myBoard.is_stalemate() :
                                print("Stalemate!")
                        else:
                            #print("FinalSquare: "+FinalSquare)
                            #print("Move "+InitialSquare+FinalSquare+" is ilegal")
                            FinalSquare="."
                elif myBoard.move_stack!=[]: #If move stack isn't empty
                    myBoard.pop()
                    lastDestination=c.square_name(myBoard.peek().to_square).lower()
                    myBoardWindow.updatePosition(myBoard.piece_map(), lastDestination)
                    myBoardWindow.updateBoard()


if __name__ == "__main__":
    main()

print("done")