"""
Golf Card Game
By Cato Cannizzo
02/2026
This file contains the game flow and non class based methods

It runs a card game of Golf with prompts for the user on how they want the game set up.
"""
# To Do:
# add computer opponent
# Add round system
# Make load a game method so a game can be init'd then loaded
    # So the object is self sufficient
# Add Jokers

# For functions that do need need any other imports
from GeneralFunctions import prompt_user
# A collection of all game objects
from GameObjects import *
import json

def set_up_game(num_players=None):
    '''Sets up the game, from sratch, prompting user for rules, and player count '''
    print("Welcome to the card game Golf!")
    rules_prompt = "Would you like a rules overview for this game? (y/n)"
    if prompt_user(typed=str, user_prompt=rules_prompt, ynChoice=True):
        #!!! Bring in the ability to access this at any time
        print("The game starts with each player having 6 face down cards in front of them.")
        print("The cards for each player are in 2 rows of 3 columns, this is their hand.")
        print("You take your turn by swapping a card in your hand"\
               "for a card from the deck or discard pile.")
        print("Any card you swap becomes face up.")
        print("The game ends when one player has all 6 cards in their hand face up.")
        print("The goal of the game is to have the lowest number of points.")
        print("All cards are worth their number, with Jacks & Queens worth 10")
        print("Kings are worth 0, as well as getting vertical pairs.\n\n")
    if not num_players:
        player_prompt = "How many players will there be today? (max 4)"
        num_players = prompt_user(int,player_prompt,0,5)
    deck=Deck()
    print("Deck shuffled!")
    print(deck)
    players=[]
    for player in range(0,num_players):
        # +1 for zero indexing
        name_prompt = f"What is the name of player {player+1}? "\
            "(Name must be between 1-14 chars)"
        name = prompt_user(str,name_prompt,1,14)
        hand = []
        for x in range(6):
            hand.append(deck.deal())
        players.append(Player(hand, name))
        # Input and prints just for more player feedback, 
        # otherwise screen transitions left me disorientated 
        print(f"6 Cards dealt to {name}!n")
        print(deck)
        input("Press enter to continue!")
    return {"players": players, "deck":deck}

def load(save_file:str =None):
    '''Loads game, automatically if called with a file name as string'''
    loading=True
    while(loading):
        # For unittests, or coded files
        if save_file:
            file_name = save_file
        else:
            file_name = "What file would you like to load?"
            file_name = prompt_user(str, file_name,0)
        try:
            f = open(file_name, 'r')
            data = json.load(f)

        except FileNotFoundError as e:
            # If file errors give player option to just start new game
            print(f'Error: the file was not found! {e}')
            if prompt_user(user_prompt="Would you like to start a "\
                              "new game instead? (y/n)",\
                              ynChoice=True):
                loading = False
                return set_up_game()
        else:
            # Start of game state unpacking
            players= []
            for p in data['players']:
                cards = []
                for c in p['grid']:
                    cards.append(Card(c['suit'],c['rank'],c['face_up']))
                players.append(Player(cards,p['name']))

            temp_discard = []
            for c in data['discard']:
                temp_discard.append(Card(c['suit'],c['rank'],c['face_up']))
            discard = Deck(temp_discard)
            temp_deck = []
            for c in data['deck']:
                temp_deck.append(Card(c['suit'],c['rank'],c['face_up']))
            deck = Deck(temp_deck)
            f.close()
            # Returns for **args unpacking
            return {
                "players": players,
                "deck": deck,
                "discard": discard,
                "last_round": data["last_round"],
                "current_player": data["current_player"],
                "row_length": data["row_length"],
                "message": data["message"],
                "ended": data["ended"],
                "save_path": file_name
            }

if __name__ == "__main__":
    '''Plays a game of golf, with out four corners rule.'''
    saved_prompt = "Would you like resume a previously saved game? (y/n)"
    if prompt_user(typed=str, 
                  user_prompt=saved_prompt, 
                  ynChoice=True
                  ):
        game_state = load()
    else:
        game_state = set_up_game()
        
    game = Game(**game_state)
    
    while not game.last_round:
        game.play_turn()
    # Once last round triggered wait for the turn of the player who ended the game
    while game.current_player != game.ended:
        game.play_turn()

    game.score()