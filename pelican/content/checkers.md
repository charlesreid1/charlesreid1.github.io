Title: CSE 143 Final Project: Checkers
Date: 2017-06-19 11:00
Category: Computer Science
Tags: programming, computer science, final project, competitive programming

The origin of this problem was the International Competitive Programming Competition (ICPC),
in particular the Pacific Northwest Regional Competition, Division 1 challenges.

[Pacific NW ICPC link](http://acmicpc-pacnw.org/)

In the Checkers problem, you are presented with a checkerboard consisting of 
black and white squares. The boards follow a normal checkers layout, that is,
all of the pieces occupy only the light or dark squares on the board.

## Problem Description

There are several white and black pieces arranged on the checkerboard.
Your goal is to answer the following question: can any one single 
black piece be used to jump and capture all of the white pieces 
in a single move? This assumes that each of the black pieces are 
black "king" pieces and can jump in either direction.

For example, the following 7x7 board configuration has one black piece 
that can jump all of the white pieces on the board with a single sequence
of moves. The black piece at B2 jumps to D4, then to F2.

![Checker Board 1](/images/checkers1.png)

If an additional white piece is added, there is no sequence of moves
that will allow any black piece to jump all of the white pieces.

![Checker Board 2](/images/checkers2.png)

## Input File

The input file consists of one line with a single integer, 
representing the size of the (square) board. 
Following are characters representing the board state.

`.` represents a square that pieces cannot occupy - the off-color squares.

`_` represents an unoccupied but valid square.

`B` represents a black piece. `W` represents a white piece.

Example:

```
8
._._._._
_._._._.
.W._.B._
_.W.W._.
.W.B._._
_._._._.
.W._.W._
_._._._.
```






