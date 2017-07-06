# reubs' chess. q to quit. r to reset. b to setup 'badly'

import sys, pygame
from random import choice
from pygame.locals import *

clock = pygame.time.Clock()
frame_rate = 20 # plenty?
screen_size = 600
square_size = screen_size/8
screen = pygame.display.set_mode((screen_size, screen_size))

w = 'white'
b = 'black'
board = [] # to hold Squares
pieces = []
highlighted = [] # to hold Squares too tho
guarded = [] # a list of all squares guarded by opponent at a given moment
selected = False # is a piece selected
selected_piece = None # which piece is selected

light_color = (200,200,200)
dark_color = (100,100,100,)
legal_color = (150,255,150)
selected_color = (255,255,150)

# CLASSES -------------------------------------------------------------------

# squares make up the board
class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([square_size, square_size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
            screen.blit(self.image, (self.rect.x, self.rect.y))

# a Piece has a name(type), color (USA spelling), x and y position
class Piece(pygame.sprite.Sprite):
    def __init__(self, name, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.color = color
        self.moves = []
        self.x = x
        self.y = y
        # do later: self.rect, self.image, etc for pygaming
        # and make Piece a subclass of pygame.sprite.Sprite
    def draw(self):
        self.rect.x = self.x * square_size
        self.rect.y = self.y * square_size
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Piece subclasses explicitly inherit the init block of the Piece class
# they have a list 'moves' of coord tuples that describe piece's moving-style
# that's all the instance 'knows'

class King(Piece):
    def __init__(self, *args):
        super(King, self).__init__(*args)
        if self.color == 'white':
            png = 'png\\wk.png'
        else: png = 'png\\bk.png'
        self.image = pygame.image.load(png)
        self.image = pygame.transform.scale(
                        self.image, (square_size, square_size))
        self.rect = self.image.get_rect()
        self.moved = False
        self.moves = [(-1,0), (1,0), (0,-1), (0,1),# left, right, up, down
                      (1,1), (1,-1), (-1,1), (-1,-1)] # diagonals
        self.checked = False

class Queen(Piece):
    def __init__(self, *args):
        super(Queen, self).__init__(*args)
        if self.color == 'white':
            png = 'png\\wq.png'
        else: png = 'png\\bq.png'
        self.image = pygame.image.load(png)
        self.image = pygame.transform.scale(
                        self.image, (square_size, square_size))
        self.rect = self.image.get_rect()
        # queen moves = bishop moves + rook moves
        for i in range(-7,8):
            if i != 0:
                self.moves.append((i,i))
                self.moves.append((-i,i))
                self.moves.append((i,0))
                self.moves.append((0,i))

class Bishop(Piece):
    def __init__(self, *args):
        super(Bishop, self).__init__(*args)
        if self.color == 'white':
            png = 'png\\wb.png'
        else: png = 'png\\bb.png'
        self.image = pygame.image.load(png)
        self.image = pygame.transform.scale(
                        self.image, (square_size, square_size))
        self.rect = self.image.get_rect()
        for i in range(-7,8):
            if i != 0: # can't move to own square
                self.moves.append((i,i))
                self.moves.append((-i,i))

class Knight(Piece):
    def __init__(self, *args):
        super(Knight, self).__init__(*args)
        if self.color == 'white':
            png = 'png\\wn.png'
        else: png = 'png\\bn.png'
        self.image = pygame.image.load(png)
        self.image = pygame.transform.scale(
                        self.image, (square_size, square_size))
        self.rect = self.image.get_rect()
        self.moves = [(2,1), (1,2), (-2,-1), (-1,-2),
                      (-2,1), (-1,2), (2,-1), (1,-2)]

class Rook(Piece):
    def __init__(self, *args):
        super(Rook, self).__init__(*args)
        if self.color == 'white':
            png = 'png\\wr.png'
        else: png = 'png\\br.png'
        self.image = pygame.image.load(png)
        self.image = pygame.transform.scale(
                        self.image, (square_size, square_size))
        self.rect = self.image.get_rect()
        self.moved = False
        for i in range(-7, 8):
            if i != 0:
                self.moves.append((i,0))
                self.moves.append((0,i))

class Pawn(Piece):
    def __init__(self, *args):
        super(Pawn, self).__init__(*args)
        if self.color == 'white':
            png = 'png\\wp.png'
        else: png = 'png\\bp.png'
        self.image = pygame.image.load(png)
        self.image = pygame.transform.scale(
                        self.image, (square_size, square_size))
        self.rect = self.image.get_rect()
        self.moved = False
        if self.color == 'white':
            self.moves = [(0,-1), (0,-2)]
            self.captures = [(1,-1), (-1,-1)]
        elif self.color == 'black':
            self.moves = [(0,1), (0,2)]
            self.captures = [(1,1), (-1,1)]

# FUNCTIONSSS ----------------------------------------------------------------

def setup_board():
    light_square = True
    for x in range(8):
        for y in range(8):
            if light_square:
                color = light_color
            else:
                color = dark_color
            board.append(Square(x*square_size,y*square_size,color))
            light_square = not light_square
        light_square = not light_square

def setup_pieces():
    pieces.append(Rook('Rook', w, 0, 7))
    pieces.append(Knight('Knight', w, 1, 7))
    pieces.append(Bishop('Bishop', w, 2, 7))
    pieces.append(Queen('Queen', w, 3, 7))
    pieces.append(King('King', w, 4, 7))
    pieces.append(Bishop('Bishop', w, 5, 7))
    pieces.append(Knight('Knight', w, 6, 7))
    pieces.append(Rook('Rook', w, 7, 7))

    pieces.append(Rook('Rook', b, 0, 0))
    pieces.append(Knight('Knight', b, 1, 0))
    pieces.append(Bishop('Bishop', b, 2, 0))
    pieces.append(Queen('Queen', b, 3, 0))
    pieces.append(King('King', b, 4, 0))
    pieces.append(Bishop('Bishop', b, 5, 0))
    pieces.append(Knight('Knight', b, 6, 0))
    pieces.append(Rook('Rook', b, 7, 0))

    for x in range(8):
        pieces.append(Pawn('Pawn', w, x, 6))
        pieces.append(Pawn('Pawn', b, x, 1))

def setup_pieces_badly(): # but only one king, in normal spot
    piece_types = ((Rook, 'Rook'), (Knight, 'Knight'),
                    (Queen, 'Queen'), (Pawn, 'Pawn'), (Bishop, 'Bishop'))
    for x in range(8):
        for y in range(6,8):
            if x == 3 and y == 7:
                pieces.append(King('King', w, x, y))
            else:
                p = choice(piece_types)
                pieces.append(p[0](p[1], w, x, y))

    for x in range(8):
        for y in range(2):
            if x == 3 and y == 0:
                pieces.append(King('King', b, x, y))
            else:
                p = choice(piece_types)
                pieces.append(p[0](p[1], b, x, y))

def draw():
    for square in board:
        square.draw()

    for square in highlighted: # (legal moves and selected square)
        square.image.set_alpha(90) # w some transparency
        square.draw()

    for piece in pieces:
        piece.draw()

    pygame.display.update()

# functions RE chess rules --------------------------------------

def moving_to_own_square(piece, x, y): # trying to move a piece nowhere?
    if piece.x == x and piece.y == y:
        return True
    else: return False

def moving_off_the_board(x, y): # is a coord off the board?
    if x > 7 or y > 7 or x < 0 or y < 0:
        return True
    else: return False

# is there already one of your own pieces at the destination?
def occupied_by_own_color(piece, x, y):
    oboc = False # start with assumption
    for otherpiece in pieces: # will check against itself too but that's ok
        #if x and y and colour all match
        if (otherpiece.x == x and otherpiece.y == y
                and otherpiece.color == piece.color):
            oboc = True
    return oboc

# return list of coords btwn a piece and a destination (exclusive)
def path(piece, x, y):
    path = []
    if x > piece.x:
        if y > piece.y:
            for i in range (1, abs(x - piece.x)):
                path.append((piece.x+i, piece.y+i))
        elif y == piece.y:
            for i in range (1, abs(x - piece.x)):
                path.append((piece.x+i, piece.y))
        elif y < piece.y:
            for i in range (1, abs(x - piece.x)):
                path.append((piece.x+i, piece.y-i))
    elif x == piece.x:
        if y > piece.y:
            for i in range (1, abs(y - piece.y)):
                path.append((piece.x, piece.y+i))
        elif y < piece.y:
            for i in range (1, abs(y - piece.y)):
                path.append((piece.x, piece.y-i))
    elif x < piece.x:
        if y > piece.y:
            for i in range (1, abs(x - piece.x)):
                path.append((piece.x-i, piece.y+i))
        elif y == piece.y:
            for i in range (1, abs(x - piece.x)):
                path.append((piece.x-i, piece.y))
        elif y < piece.y:
            for i in range (1, abs(x - piece.x)):
                path.append((piece.x-i, piece.y-i))
    return path

def piece_in_path(piece, x, y): # is a piece in the way?
    pip = False
    if piece.name != 'Knight': # Knights don't have to worry about paths
        # compare each square in path against the loc of every piece:
        for step in path(piece, x, y):
            for otherpiece in pieces:
                if otherpiece.x == step[0] and otherpiece.y == step[1]:
                    pip = True
    return pip

# does the move conform to the piece's moving-style?
def move_style_ok(piece, x, y):

    msok = False # start with this assumption

    if piece.name == 'Pawn':

        # can capture diagonally
        # (if the move is in captures[] and there's an opposing piece there,
        # then movestyle is ok)
        for capture in piece.captures:
            if x - piece.x == capture[0] and y - piece.y == capture[1]:
                for otherpiece in pieces:
                    if (otherpiece.x == x and otherpiece.y == y
                        and otherpiece.color != piece.color):
                        msok = True

        if piece.moved:
            # if it's not a pawns first move, they can only move 1 space
            # (only check against index 0 of the pawns moves list)
            if (x - piece.x == piece.moves[0][0]
                and y - piece.y == piece.moves[0][1]):
                msok = True
        else:
            for move in piece.moves: # go through the piece's move tuples
                if x - piece.x == move[0] and y - piece.y == move[1]:
                    msok = True

        #can't capture straight-forwards
        #if the move is in moves[] and there's an opponents piece there
        for move in piece.moves:
            if x - piece.x == move[0] and y - piece.y == move[1]:
                for otherpiece in pieces:
                    if (otherpiece.x == x and otherpiece.y == y
                        and otherpiece.color != piece.color):
                        msok = False

    else: # in all other cases...
        for move in piece.moves: # go through the piece's move tuples
            if x - piece.x == move[0] and y - piece.y == move[1]:
                msok = True
    return msok

def guarded(piece): # returns list of squares guarded by opponent
    a = []
    for otherpiece in pieces:
        if piece.color != otherpiece.color:
            if otherpiece.name == 'Pawn':
                for capt in otherpiece.captures:
                    # not checking legality of pawn captures on purpose
                    a.append((otherpiece.x + capt[0], otherpiece.y + capt[1]))
            else:
                for move in otherpiece.moves:
                    x = otherpiece.x + move[0] # destination = location + move
                    y = otherpiece.y + move[1]
                    # using specific rules/parts of is_legal here,
                    # in order to exclude 'occupied_by_own_color'
                    h = moving_to_own_square(otherpiece, x, y)
                    i = moving_off_the_board(x, y)
                    j = piece_in_path(otherpiece, x, y)
                    k = move_style_ok(otherpiece, x, y)
                    if not h and not i and not j and k:
                        a.append((x, y))
    a = list(set(a)) # remove duplicates
    return a

# if king, compare guarded squares to dest AND path (for castling)
def moving_into_check(piece, x, y):
    mic = False
    if piece.name == 'King':
        for guarded_square in guarded(piece):
            if (x,y) == guarded_square:
                mic = True
            for step in path(piece, x, y):
                if step == guarded_square:
                    mic = True
    return mic

def can_castle(piece, x, y): # UNFINISHED
    cc = False # assume no, try to prove yes...
    if piece.name == 'King' and piece.moved == False: # if unmoved King,
        for otherpiece in pieces:
            # and, if there is an unmoved matching-color rook,
            if (otherpiece.name == 'Rook' and otherpiece.color == piece.color
                and otherpiece.moved == False):
                # and if there's nothing in the path between them,
                if not piece_in_path(piece, otherpiece.x, otherpiece.y):
                    pass
                    # TO DO:
                    # and if there's no checks in the path,
                    # and if the king isn't in check to begin with,
                    # then cc = True
    return cc

def is_legal(piece, x, y): # return true if a move is legal (except check)
    #given a piece and its destination.

    motb = moving_off_the_board(x, y)
    if motb:
        return False

    mtos = moving_to_own_square(piece, x, y)
    if mtos:
        return False

    mic = moving_into_check(piece, x, y)
    if mic:
        return False

    oboc = occupied_by_own_color(piece, x, y)
    if oboc:
        return False

    msok = move_style_ok(piece, x, y)
    if not msok:
        return False

    pip = piece_in_path(piece, x, y)
    if pip:
        return False
    else:
        return True


# let's go -------------------------------------------------------------
setup_board()
setup_pieces()

# game loop.... the main parts could be split into multiple functions
while 1:
    clock.tick(frame_rate)
    draw()

    # mouse + keyboard events
    for ev in [pygame.event.wait()] + pygame.event.get(): # look at all events
        if hasattr(ev, 'key'):
            if ev.key == K_q: exit() # press 'q' to quit
            if ev.key == K_r: # type r to rest the pieces
                pieces = []
                setup_pieces()
            if ev.key == K_b:
                pieces = []
                setup_pieces_badly()

        if ev.type == pygame.MOUSEBUTTONDOWN: # if you click...

            # if a piece is already selected, make that move
            if selected:
                for square in board:
                    x = square.rect.x/square_size
                    y = square.rect.y/square_size

                    if square.rect.collidepoint(pygame.mouse.get_pos()):
                        if is_legal(selected_piece, x, y):

                            # capturing?
                            for piece in pieces:
                                if piece.x == x and piece.y == y:
                                    piece.x = 666 # that piece goes to hell
                                    piece.y = 666

                            # move the piece
                            selected_piece.x = x
                            selected_piece.y = y

                            # update 'moved' attr if Pawn/Rook/King
                            if (selected_piece.name == 'Pawn'
                                or selected_piece.name == 'Rook'
                                or selected_piece.name == 'King'):
                                selected_piece.moved = True

                    selected = False
                    highlighted = []
            else:
                highlighted = []
                for piece in pieces:
                    # if you clicked on a piece's Rect,
                    if piece.rect.collidepoint(pygame.mouse.get_pos()):
                        selected = True # then you have made a selection,
                        # save the  c h o s e n   o n e   for later
                        selected_piece = piece

                        # add a Square (to show selected square) to 'highlighted' list
                        highlighted.append(Square(piece.rect.x, piece.rect.y, selected_color))

                        for move in piece.moves: # look where each move would end up
                            x = piece.x + move[0]
                            y = piece.y + move[1]
                            if is_legal(piece, x, y):
                                # add Squares (to show legal moves) to 'highlighted' list
                                highlighted.append(Square(x*square_size, y*square_size, legal_color))

                        if piece.name == 'Pawn': # if pawn, gotta add captures too
                            for capture in piece.captures:
                                x = piece.x + capture[0]
                                y = piece.y + capture[1]
                                if is_legal(piece, x, y):
                                    highlighted.append(Square(x*square_size, y*square_size, legal_color))
