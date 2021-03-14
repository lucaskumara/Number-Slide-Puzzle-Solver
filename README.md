# Number Slide Puzzle Solver
A python program that can solve and display the solution to a [number slide puzzle.](http://www.artbylogic.com/puzzles/numSlider/numberShuffle.htm)

## Purpose
This assignment was the first assignment given to me when I did my intro to artificial intelligence course. I am very proud of the work I did in this course and as such I've decided to put the code on GitHub.

The assignment was introducing us to a number of searching algorithms, three of which were implemented in the code:
* Breadth First Search
* Iterative Deepening Depth First Search
* A* Search

## Usage
If you would like to run the code for yourself, you can clone the repo and try it out

1. Using python3, run the `solver.py` file and specify the search algorithm to use. 
```
$ python3 solver.py a*
```
2. You will be prompted to enter the width of the puzzle
```
Enter puzzle width: 3
```
3. Lastly you need to enter the puzzle itself. Enter the puzzle values starting from the top left and seperating the values with a tab. Use a lowercase x in place of the empty space and use a newline once you are done entering a row.
```
Enter puzzle values row by row (seperated with a tab): 
1       2       3
4       5       6
7       x       8
```
4. You are done! The program should now be working to solve the puzzle.
```
$ python3 solver.py bfs
Enter puzzle width: 3
Enter puzzle values row by row (seperated with a tab): 
1       2       3
4       5       6
7       x       8
Solving...
Solution: 1 move(s)
1       2       3
4       5       6
7       x       8

1       2       3
4       5       6
7       8       x
```

## Limitations
One limitation of the program is it is unable to identify whether or not a puzzle is unsolvable. This was not a requirement of the assignment and was therefore left out.

Another limitation is the heuristic for the A* search as it works by identifying how many of the numbers are in their correct spot. The limitation comes from the fact that some puzzle states cannot have that score improved through any of the available moves and as such, there is a chance that the solution provided will be suboptimal.
