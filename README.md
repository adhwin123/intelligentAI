IntelligentAgent for 2048 game

This project implements an intelligent agent that plays the 2048 game using the Expectiminimax algorithm with alpha-beta pruning. The agent evaluates possible moves in a time-constrained environment and selects the most promising direction using a custom heuristic function.

**Project Overview**

Course: Artificial Intelligence (AI)
Instructor: Professor Ansaf Sales-Aouissi
Institution: Columbia University
File: IntelligentAgent-2.py
Language: Python

**Features**

Implements the BaseAI class from the course framework.
Uses expectiminimax search with alpha-beta pruning to explore future game states.
Incorporates time-limited decision-making (~0.2 seconds per move).
Includes a custom heuristic function to estimate grid utility.
Chooses fallback moves randomly when no optimal move is found in time.

**Core Components**

getMove(self, grid)
Entry point for the AI agent.
Evaluates all available moves.
Selects the move with the highest utility as computed by the expectiminimax function.
Falls back to a random move if no decision is made within the time limit.
expectiminimax(...)
Recursive function modeling both the player’s and computer’s moves.
Alternates between max (AI) and expect (random tile spawn) levels.
Applies alpha-beta pruning to eliminate unpromising branches early.
Returns the heuristic value of terminal or time-limited states.
heuristic(grid)
Evaluates a grid based on:
Number of empty tiles
Monotonicity of rows/columns
Smoothness of the board
Maximum tile value

**Requirements:**

Ensure your environment includes:

Python >= 3.6
And a valid BaseAI.py module as provided in the course framework.

**File Structure**

├── IntelligentAgent-2.py   # Main agent implementation
├── BaseAI.py               # Base class for AI agents (provided externally)

**How to Use**

Integrate IntelligentAgent-2.py with the 2048 game engine provided in the course.
Make sure to place the BaseAI.py in the same directory.
Run the game framework and watch the agent make intelligent decisions.

**Acknowledgments**

Special thanks to Professor Ansaf Sales-Aouissi and the Columbia University AI faculty for their guidance and support throughout this project.
