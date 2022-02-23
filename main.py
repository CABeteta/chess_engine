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
                if InitialSquare == ".":
                    InitialSquare = myBoardWindow.getSquareFromXY(click_location)
                    print("InitialSquare: "+InitialSquare)
                else:
                    FinalSquare = myBoardWindow.getSquareFromXY(click_location)
                    currentMove = InitialSquare.lower()+FinalSquare.lower()
                    if InitialSquare == FinalSquare :
                        print("Piece dropped.")
                        InitialSquare="." # So the loop starts again
                        FinalSquare="."
                    elif c.Move.from_uci()
                        myBoard.push_uci(currentMove)
                        myBoardWindow.updatePosition(myBoard.piece_map())
                        myBoardWindow.updateBoard()
                        print("FinalSquare: "+FinalSquare)
                        InitialSquare="." # So the loop starts again
                        FinalSquare="."
                        if (myBoard.is_checkmate() == True ):
                            print("Checkmate!")
                    else:
                        print("FinalSquare: "+FinalSquare)
                        print("Move "+InitialSquare+FinalSquare+" is ilegal")
                        InitialSquare="." # So the loop starts again
                        FinalSquare="."
                    

if __name__ == "__main__":
    main()

print("done")
