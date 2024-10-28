# Chopsticks Game

Welcome to the **Chopsticks** game! This project implements a console-based version of the finger-counting children's game "aChopsticks." In this game, players take turns using their fingers to “attack” each other's hands, aiming to eliminate the opponent by strategically transferring finger counts.

## Table of Contents

- [Overview](#overview)
- [Gameplay Rules](#gameplay-rules)
- [How to Run](#getting-started)
- [Project Structure](#project-structure)
- [Algorithm Explanation](#algorithm-explanation)
- [Logging and Debugging](#logging-and-debugging)
- [Future Enhancements](#future-enhancements)

## Overview

This Chopsticks game is a two-player game where each player (human or computer) attempts to knock out the opponent's hands by transferring finger counts strategically. The implementation features an AI using the Minimax algorithm to evaluate potential moves, making it challenging for human players.

## Gameplay Rules

1. **Initial Setup**: Each player starts with one finger raised on each hand.
2. **Turns**: Players take turns attacking the opponent.
   - **Attacking**: Choose a hand to attack with and an opponent's hand to attack. 
   - **Damage**: When a hand attacks, its finger count is added to the attacked hand's fingers.
3. **Rollover**: This version of Chopsticks has a rollover, meaning when an attack results in more than five fingers, the resulting fingers is the fingers mod five.
4. **Winning**: The game ends when both hands of one player reach 0 fingers, making them "dead."
5. **Splitting**: This version of chopsticks doesn't include splitting, only attacks.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/chopsticks-game.git
   cd chopsticks-game
2. Run the game.py file
  ```bash
   python3 game.py
  



