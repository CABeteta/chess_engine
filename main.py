import graphics
import pygame as pg
import chess as ch
import time

def main():
    myBoardWindow = graphics.BoardGraph()
    myBoard = ch.Board()
    running = True

    InitialSquare = "."
    FinalSquare = "."
    currentMove = ".."

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                click_location = pg.mouse.get_pos() # (x, y) of the mouse
                if(e.button == pg.BUTTON_LEFT):
                    if InitialSquare == ".": #Selecting origin
                        InitialSquare = myBoardWindow.getSquareFromXY(click_location)
                        if (myBoard.turn == myBoardWindow.pieceColor(InitialSquare) and myBoardWindow.squareIsEmpty(InitialSquare)==False) :
                            myBoardWindow.selectSquare(InitialSquare)
                        else: #Invalid first selection, ignoring
                            InitialSquare="."
                    else: #Selecting destination
                        FinalSquare = myBoardWindow.getSquareFromXY(click_location)
                        currentMove = InitialSquare.lower()+FinalSquare.lower()
                        if InitialSquare == FinalSquare: #Unselecting
                            InitialSquare="." # So next time we select origin again
                            FinalSquare="."
                            myBoardWindow.selectSquare(InitialSquare) #Unselects
                        elif ch.Move.from_uci(currentMove) in myBoard.legal_moves: #Legal move
                            myBoard.push_uci(currentMove)
                            myBoardWindow.movePiece(InitialSquare, FinalSquare)
                            myBoardWindow.updateBoard()
                            InitialSquare="." # So next time we select origin again
                            FinalSquare="."
                            if myBoard.is_checkmate() :
                                print("Checkmate!")
                            elif myBoard.is_stalemate() :
                                print("Stalemate!")
                        else: # The move was ilegal
                            FinalSquare="."
                elif myBoard.move_stack!=[]: #If move stack isn't empty
                    myBoard.pop()
                    lastDestination=ch.square_name(myBoard.peek().to_square).lower()
                    myBoardWindow.updatePosition(myBoard.piece_map(), lastDestination)
                    myBoardWindow.updateBoard()
            elif e.type == pg.KEYDOWN:
                if e.key  == pg.K_u:
                    print("UNDO")
                elif e.key == pg.K_r:
                    print("ROOK")
                elif e.key == pg.K_q:
                    print("QUEEN")
                elif e.key == pg.K_b:
                    print("BISHOP")
                elif e.key == pg.K_k:
                    print("KNIGHT")



if __name__ == "__main__":
    main()

print("done")