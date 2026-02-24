from GeneralFunctions import promptUser
from CardObjects import *

def start_game():
    print("Welcome to the card game Golf!")
    rulesPrompt = "Would you like a rules overview for this game? (y/n)"
    if promptUser(typed=str, userPrompt=rulesPrompt, ynChoice=True).lower() == "y":
        #!!! Bring in the ability to access this at any time
        print("The game starts with each player having 6 face down cards in front of them.")
        print("The cards for each player are in 2 rows of 3 columns, this is there hand.")
        print("You take your turn by swapping a card in your hand for a card from the deck or discard pile.")
        print("Any card you swap into your hand become face up.")
        print("The game ends when one player has all 6 cards in their hand face up.")
        print("The goal of the game is to have the lowest number of points.")
        print("All cards are worth their number, with Jacks & Queens worth 10")
        print("Kings are worth 0, as well as getting verital pairs.")
    playerPrompt = "How many players will there be today?"
    return promptUser(int,playerPrompt,0,5)

def setUpGame(numPlayers):
    deck=Deck()
    print("Deck shuffled!")
    print(deck)
    players=[]
    for player in range(0,numPlayers):
        namePrompt = f"What is the name of player {player+1}? (Name must be between 1-14 chars)"
        # name = promptUser(str,namePrompt,1,14)
        name = "asd"
        hand = []
        for x in range(6):
            hand.append(deck.deal())
        players.append(Player(hand, name))
        print(players[player])
        print(deck)
    return {"players": players, "deck":deck}
          

if __name__ == "__main__":
    # gameState = setUpGame(start_game())
    gameState = setUpGame(1)

    game = Game(**gameState)
    
    # while not game.lastRound:
    game.playTurn()
