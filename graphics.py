from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from math import floor
import pygame as p
import chess as c

p.init()

class BoardGraph():
    def __init__(self) -> None:
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.WIDTH = 800
        self.HEIGHT = 800
        self.SQ_SIZE = self.WIDTH/8
        self.PIECE_SIZE = 80
        self.maxFPS = 25
        self.IMAGES = {}
        self.COLORS = [p.Color("tan"), p.Color("dimgrey")]
        self.clock = p.time.Clock()
        self.squareName=[[]]
        self.rank={}
        self.file={}
        self.ScreenCoordinates={}
        self.MatrixCoordinates={}
        self.LastMove = '.'
        
        for r in range(8): #For all 8 ranks (rows)
            tmp = []
            for f in range(8): #For all 8 files (columns)
                tmp.append(chr(int(ord('a') + f))+str(r+1))
                #self.squareName[r][f]=str(int(ord('a') + f))+str(r+1)
                self.rank[tmp[f]]=7-r
                self.file[tmp[f]]=f
                self.ScreenCoordinates[tmp[f]]=[f*self.SQ_SIZE, (7-r)*self.SQ_SIZE]
                self.MatrixCoordinates[tmp[f]]=[r, f]
            self.squareName.append(tmp)
        self.loadImages()
        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        self.drawBoard()
        self.drawPieces()
        self.flip()

    def loadImages(self):
        for piece in c.PIECE_SYMBOLS[1:]:  # Load the images to memory
            self.IMAGES[piece.lower()] = p.image.load(
                "images/b" + piece.upper() + ".png")
            self.IMAGES[piece.upper()] = p.image.load(
                "images/w" + piece.upper() + ".png")
        for image in self.IMAGES:
            self.IMAGES[image] = p.transform.smoothscale(
                self.IMAGES[image], (self.PIECE_SIZE, self.PIECE_SIZE))

    def drawBoard(self):
        self.clock.tick(self.maxFPS)
        fontSize = 18
        font = p.font.SysFont(None, fontSize)
        for r in range(8):
            for c in range(8):
                color = self.COLORS[(r+c) % 2]
                p.draw.rect(self.screen, color, p.Rect(
                    c*self.SQ_SIZE, r*self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                if c == 0: #In the first column we plot numbers
                    img = font.render(str(8-r), 'True', self.COLORS[(r+1) % 2])
                    rect = img.get_rect()
                    self.screen.blit(img, (2, r*self.SQ_SIZE+2))
                if r == 7: #In the first row we plot letters
                    img = font.render(chr(ord('A')+c), 'True', self.COLORS[c % 2])
                    rect = img.get_rect()
                    self.screen.blit(img, ((c+1)*self.SQ_SIZE-rect.width, 8*(self.SQ_SIZE)-rect.height-2))
        self.highlightPiece(self.LastMove, "blue")

    def highlightPiece(self, squares, color):
        '''
        Input: 
            squares: tuple with what square(s) to higlight, for example ["d2", "a2"]
            color: what color to use, from pygame selection for instance "blue"
        '''
        if squares!='.' :
            s = p.Surface((self.SQ_SIZE, self.SQ_SIZE))
            s.set_alpha(50) # Transparency: 0 = transparent, 255 = opaque
            s.fill(p.Color(color))
            position = self.ScreenCoordinates[squares]
            self.screen.blit(s, position)

    def drawPieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != '.':
                    square_centre_x, square_centre_y  = [(c+0.5)*self.SQ_SIZE, (r+0.5)*self.SQ_SIZE]
                    pImage = self.IMAGES[piece]
                    pImageXsize, pImageYsize = pImage.get_size()
                    pImageX = square_centre_x - pImageXsize/2
                    pImageY = square_centre_y - pImageYsize/2
                    self.screen.blit(pImage, p.Rect(
                        pImageX, pImageY, pImageXsize, pImageYsize))

    def setColors(self, listTwoColors):
        self.COLORS = listTwoColors

    def squareIsEmpty(self, square):
        if square == '.':
            return True
        elif self.pieceInSquare(square)=='.':
            return True
        else:
            return False

    def pieceColor(self, square):
        return self.pieceInSquare(square).isupper()

    def pieceInSquare(self, square):
        return self.board[self.rank[square]][self.file[square]]

    def selectSquare(self, square):
        self.drawBoard()
        self.highlightPiece(square, 'green')
        self.drawPieces()
        self.flip()

    def flip(self):
        p.display.flip()

    def movePiece(self, homeSquare, destSquare, newPiece='.'):
        '''
        Input: 
            homeSquare: what piece to move, for example "d2"
            destSquare: where to put it, for example "d4"
            newPiece: in case of promotion what piece to promote to
            !! WE ASSUME THE MOVEMENT IS ALWAYS VALID !!
        '''
        homeFile = self.file[homeSquare]
        homeRank = self.rank[homeSquare]
        destFile = self.file[destSquare]
        destRank = self.rank[destSquare]
        currentPiece = self.board[homeRank][homeFile]
        if currentPiece !='.':
            self.board[homeRank][homeFile]='.'
            if (currentPiece.lower()=='p' and (destRank==7 or destRank==0)):  #Only when promoting...
                if (currentPiece.isupper()==True):
                    self.board[homeRank][homeFile]=newPiece.upper()
                else:
                    self.board[homeRank][homeFile]=newPiece.lower()
            else:              #Usual case
                self.board[destRank][destFile]=currentPiece
        self.LastMove=destSquare

    def updatePosition(self, position, lastDest = '.'):
        newPosition = [ ['.','.','.','.','.','.','.','.'],
                        ['.','.','.','.','.','.','.','.'],
                        ['.','.','.','.','.','.','.','.'],
                        ['.','.','.','.','.','.','.','.'],
                        ['.','.','.','.','.','.','.','.'],
                        ['.','.','.','.','.','.','.','.'],
                        ['.','.','.','.','.','.','.','.'],
                        ['.','.','.','.','.','.','.','.']
                        ]
        for square_index in position:
            newPosition[(63-square_index)//8][square_index%8] = str(position[square_index])
        self.board = newPosition
        self.LastMove=lastDest

    def updateBoard(self):
        self.drawBoard()
        self.drawPieces()
        self.flip()

    def getSquareFromXY(self, location):
        rank = str(int(7-location[1]//self.SQ_SIZE)+1)
        file = chr(int(ord('a') +location[0]//self.SQ_SIZE))
        result = file+rank
        return result