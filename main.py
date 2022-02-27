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
                        elif c.Move.from_uci(currentMove) in myBoard.legal_moves: #Legal move
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
                    lastDestination=c.square_name(myBoard.peek().to_square).lower()
                    myBoardWindow.updatePosition(myBoard.piece_map(), lastDestination)
                    myBoardWindow.updateBoard()
            elif e.type == p.KEYDOWN:
                if e.key  == p.K_u:
                    print("UNDO")
                elif e.key == p.K_r:
                    print("ROOK")
                elif e.key == p.K_q:
                    print("QUEEN")
                elif e.key == p.K_b:
                    print("BISHOP")
                elif e.key == p.K_k:
                    print("KNIGHT")



if __name__ == "__main__":
    main()

print("done")