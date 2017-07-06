# reubschess
A chess pygame, unsure where it will lead.

reubs' chess. q to quit. r to reset. b to setup 'badly'
v2.3 added guarded[] and moving_into_check() ie king cannot move into check
v2.2 refactored 'is_legal' function into many smaller rules
v2.1 added functions for re-setup pieces, random setup
v2: added pygame interaction, fixed legality function bugs

pieces can be selected, moved, capture opponent's pieces
there are no turns
legal moves are highlighted when a piece is selected
legality questions not yet addressed:
     en passant, check + mate, castling, pawn-promotion.
     though the king cannot move into check, a player can still reveal themselves into check!
the Pawn subclass assumes white is always set up at the bottom,
tho a Piece.direction attr and a setup_pieces_reverse() func could be added
