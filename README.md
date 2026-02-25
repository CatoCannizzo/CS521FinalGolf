# Cato C's CS521 Final Project - A Golf Card Game

## Project Summary
This is a terminal based digital version of the "Golf" card game. Built in Python, it allows 1–4 players to play Golf. The goal of the game is to finish with the **lowest** score possible by swapping high cards in your hand for low cards from the deck.

## The Program
This program manages the entire logic and flow of a professional card game session:

* **Game Engine:** It handles the deck, a discard pile, and player turns. It allows players to draw cards, view other players' hands (simulating looking across the table, as golf is played open on a table), and swap cards into their hand.
* **Scoring:** The system calculates scores using Golf rules. It checks for "vertical pairs": matching ranks in a column of a hand and scores them 0.
* **Visual Interface:** It displays game state using ASCII art to show cards in the terminal window, clearly showing which cards are face-up or face-down.
* **Data Persistence:** The program includes a full **Save and Load** system. Allowing game state to be converted to and from JSON files, allowing players to name their save files and resume their game at any time.

## Why It Is Useful
This program is a showcase of my software development practices, and just fun:

* **Unit Testing** testGolf.py shows variety of unit test criteria including saving to and loading from a temporary file
* **Encapsulation:** It uses private attributes (like __RankValues) and private methods (like __getCardbyLine) to ensure that internal logic cannot be accidentally changed by other parts of the code, and streamlines IDE suggestions.
* **Tuples and Sets** It uses a tuple is used to define hand shape, the grid in the code. So you can change the grid size from 2x3 to 4x2 just by editing a single tuple, and the rest of the logic SHOULD adapt automatically to any combination although I've only tested a few.
* **Error Handling:** It uses the try/except/else blocks to handle common issues like missing save files or restricted folder permissions in the Save and Load functions.

* **Fun** Recreational fun is always useful, and the extentive history and varity of card games show case the importance of fun to humans across eras and continents
