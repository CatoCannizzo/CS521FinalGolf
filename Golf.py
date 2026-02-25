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
from GeneralFunctions import promptUser
# A collection of all game objects
from GameObjects import *

def setUpGame(numPlayers):
    '''Sets up the game, from sratch, prompting user for rules, and player count '''
    print("Welcome to the card game Golf!")
    rulesPrompt = "Would you like a rules overview for this game? (y/n)"
    if promptUser(typed=str, userPrompt=rulesPrompt, ynChoice=True):
        #!!! Bring in the ability to access this at any time
        print("The game starts with each player having 6 face down cards in front of them.")
        print("The cards for each player are in 2 rows of 3 columns, this is their hand.")
        print("You take your turn by swapping a card in your hand"\
               "for a card from the deck or discard pile.")
        print("Any card you swap becomes face up.")
        print("The game ends when one player has all 6 cards in their hand face up.")
        print("The goal of the game is to have the lowest number of points.")
        print("All cards are worth their number, with Jacks & Queens worth 10")
        print("Kings are worth 0, as well as getting vertical pairs.")
    playerPrompt = "How many players will there be today? (max 4)"
    numPlayers = promptUser(int,playerPrompt,0,5)
    deck=Deck()
    print("Deck shuffled!")
    print(deck)
    players=[]
    for player in range(0,numPlayers):
        # +1 for zero indexing
        namePrompt = f"What is the name of player {player+1}? "\
            "(Name must be between 1-14 chars)"
        name = promptUser(str,namePrompt,1,14)
        hand = []
        for x in range(6):
            hand.append(deck.deal())
        players.append(Player(hand, name))
        # Input and prints just for more player feedback, 
        # otherwise screen transitions left me disorientated 
        print(f"6 Cards dealt to {name}! \n We still have")
        print(deck)
        input("Press enter to continue!")
    return {"players": players, "deck":deck}

def load(saveFile:str =None):
    '''Loads game, automatically if called with a file name as string'''
    loading=True
    while(loading):
        # For unittests, or coded files
        if saveFile:
            filename = saveFile
        else:
            filename = "What file would you like to load?"
            filename = promptUser(str, filename,0)
        try:
            f = open(filename, 'r')
            data = json.load(f)

        except FileNotFoundError as e:
            # If file errors give player option to just start new game
            print(f'Error: the file was not found! {e}')
            if promptUser(userPrompt="Would you like to start a "\
                              "new game instead?",\
                              ynChoice=True):
                loading = False
                return setUpGame()
        else:
            # Start of game state unpacking
            players= []
            for p in data['players']:
                cards = []
                for c in p['grid']:
                    cards.append(Card(c['suit'],c['rank'],c['faceUp']))
                players.append(Player(cards,p['name']))

            tempdiscard = []
            for c in data['discard']:
                tempdiscard.append(Card(c['suit'],c['rank'],c['faceUp']))
            discard = Deck(tempdiscard)
            tempdeck = []
            for c in data['deck']:
                tempdeck.append(Card(c['suit'],c['rank'],c['faceUp']))
            deck = Deck(tempdeck)
            f.close()
            # Returns for **args unpacking
            return {
                "players": players,
                "deck": deck,
                "discard": discard,
                "lastRound": data["lastRound"],
                "currentPlayer": data["currentPlayer"],
                "rowLength": data["rowLength"],
                "message": data["message"],
                "ended": data["ended"],
                "savePath": filename
            }

if __name__ == "__main__":
    '''Plays a game of golf, with out four corners rule.'''
    savedPrompt = "Would you like resume a previously saved game? (y/n)"
    if promptUser(typed=str, 
                  userPrompt=savedPrompt, 
                  ynChoice=True
                  ):
        gameState = load()
    else:
        gameState = setUpGame()
        
    game = Game(**gameState)
    
    while not game.lastRound:
        game.playTurn()
    # Once last round triggered wait for the turn of the player who ended the game
    while game.currentPlayer != game.ended:
        game.playTurn()

    game.score()