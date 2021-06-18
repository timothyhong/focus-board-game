# Focus Game

#### Overview
Contains a Player class and a FocusGame class to play the abstract board game Focus/Domination. You can see the rules [here](https://en.wikipedia.org/wiki/Focus_(board_game)).

The FocusGame class allows for 2-4 human players.

The board looks like a checkerboard with three squares in each corner removed, hence forming 6X6 board with 1X4 extensions on each side (You can find the picture of the board [here](http://www.geekyhobbies.com/domination-aka-focus-board-game-review-and-rules/)). Depending on the number of players, the board is set up differently.

At the beginning of the game, a random player's piece is selected that determines who plays first.

#### Features
- 2-4 human players with correct board set up and rules for number of players
- Robust error checking
- Achieve victory by capturing a user-specified number of pieces or through "domination"

#### Upcoming Features
- Graphical GUI
- Computer players

#### Playing the game:
On a player’s turn they will make one move. They can either make a single move, a multiple move, or a reserve move.
###### Single Move
In a single move the player moves one of their playing pieces which is on a space by itself. This piece can be moved one space vertically or horizontally. The piece may never be moved diagonally. The piece can either be moved to an empty space, or a space with one or more playing pieces on it. If a piece is moved to a space with a stack of pieces on it, the piece that was just moved is placed on the top of the stack. A player can move their playing piece onto a stack containing their own pieces, pieces of other players, or both.
###### Multiple Move
In a multiple move a player can move a whole stack of pieces. A player may only move a stack if their pawn is on top of the stack. When a player wants to move a stack they choose how much of the stack that they want to move. They can either move the entire stack or take some pieces off the top of the stack and leave some of the playing pieces behind. The player will then be able to move the stack a number of spaces up to the height of the stack they are moving, so for example if the player has 3 pieces in stack they can move that stack 3 spaces. They can move the stack vertically or horizontally but not diagonally. When moving a stack it will only impact the pieces on the space that that stack lands on and won’t impact the pieces on the spaces that the stack was moved through.
###### Reserving and Capturing Pieces
After moving a piece/stack the height of the stack that you moved the piece(s) to is checked. If the new stack ever contains more than five pieces some of the pieces will be removed from the stack. Starting with the playing piece on the bottom of the stack, you will remove pieces until the stack only has five pieces remaining.
The pieces that were removed from the board will either be captured or put into reserve. All pieces not belonging to the player who made the move are captured. These pieces are removed and won’t be used for the rest of the game. Pieces belonging to the player who made the move will be added to their reserve pile.
###### Reserve Move (Can be done by only the player who has reserved pieces)
If a player has playing pieces in reserve they can make a reserve move instead of a single or multiple move. To make a reserve move take one of your playing pieces in reserve and place it on any space on the gameboard. The reserve piece can be placed on an empty space, on a space containing one piece, or a space containing multiple pieces. Placing the reserve piece counts as your turn as you don’t get to move the piece you just added to the gameboard.
###### End of the Game
The first player who captures six pieces of the other player or "dominates" all other players wins the game. "Domination" of another player means that player has no reserve pieces left to play and does not control any pieces on the board.

This [YouTube link](https://www.youtube.com/watch?v=DVRVQM9lo9E) explains how to play the game
