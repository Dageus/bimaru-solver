# Bimaru Solver

Algorithm using ML algorithms to solve bimaru, a battleship puzzle based on using logic to complete the grid proposed

## How to run

Simply place the game grid on the format the algorithm can read, for example:

ROW	2	0	5	0	5	0	0	4	2	2
COLUMN	1	3	4	0	0	0	5	2	4	1
8
HINT	7	8	T
HINT	9	2	C
HINT	8	8	B
HINT	4	8	M
HINT	8	1	W
HINT	0	0	C
HINT	0	6	W
HINT	4	1	C

where *ROW* shows how many items should be on each row, reading from left to right and 0...N
and *COLUMN* shows how many items should be on each column, following the same logic
*HINT* represents the coordinates of each hint given by the game in the start, and:
 - T represents a TOP piece
 - C represents a CENTER piece
 - B represents a BOTTOM piece
 - M represents a MIDDLE piece
 - W represents a WATER piece
 - L represents a LEFT piece
 - R represents a RIGHT piece

and pass it into the algorithm

### example:

`$ python bimaru.py < instance_02.txt`

## The algorithm will use a DFS and a Binary Tree Structure to find the best solution
