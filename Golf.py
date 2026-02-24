from GeneralFunctions import promptUser
from GameObjects import *

def start_game():
    print("Welcome to the card game Golf!")
    rulesPrompt = "Would you like a rules overview for this game? (y/n)"
    if promptUser(typed=str, userPrompt=rulesPrompt, ynChoice=True):
        #!!! Bring in the ability to access this at any time
        print("The game starts with each player having 6 face down cards in front of them.")
        print("The cards for each player are in 2 rows of 3 columns, this is there hand.")
        print("You take your turn by swapping a card in your hand for a card from the deck or discard pile.")
        print("Any card you swap into your hand become face up.")
        print("The game ends when one player has all 6 cards in their hand face up.")
        print("The goal of the game is to have the lowest number of points.")
        print("All cards are worth their number, with Jacks & Queens worth 10")
        print("Kings are worth 0, as well as getting verital pairs.")
    playerPrompt = "How many players will there be today? (max 4)"
    return promptUser(int,playerPrompt,0,5)

def setUpGame(numPlayers):
    deck=Deck()
    print("Deck shuffled!")
    print(deck)
    players=[]
    for player in range(0,numPlayers):
        namePrompt = f"What is the name of player {player+1}? (Name must be between 1-14 chars)"
        # name = promptUser(str,namePrompt,1,14)
        name = "Player " + str(player)
        hand = []
        for x in range(6):
            hand.append(deck.deal())
        players.append(Player(hand, name))
        print(players[player])
        print(deck)
    return {"players": players, "deck":deck}

def load():
    loading=True
    while(loading):
        filename = "What file would you like to load?"
        filename = promptUser(str, filename,0)
        try:
            f = open(filename, 'r')
            data = json.load(f)

        except FileNotFoundError as e:
            print(f'Error: the file was not found! {e}')
            if not promptUser(userPrompt="Would you like to try again?",ynChoice=True):
                loading = False
                return setUpGame(start_game())
        players= []
        for p in data['players']:
            cards = []
            for row in p['grid']:
                for c in row:
                    cards.append(Card(c['suit'],c['rank'],c['faceUp']))
            players.append(cards,p['name'])
        discard = []
        for c in data['discard']:
            discard.append(Card(c['suit'],c['rank'],c['faceUp']))
        deck = []
        for c in data['deck']:
            deck.append(Card(c['suit'],c['rank'],c['faceUp']))
        currentPlayer = data['currentPlayer']
        lastRound = data["lastRound"]
        ended = data["ended"]
        message = data["message"]
        rowLength = data["rowLength"]
        args = [players,deck,discard,lastRound,currentPlayer,rowLength,message,ended]
        return args

if __name__ == "__main__":
    savedPrompt = "Would you like resume a previously saved game? (y/n)"
    if promptUser(typed=str, userPrompt=savedPrompt, ynChoice=True).lower() == "y":
        gameState = load()
    else:
        # gameState = setUpGame(start_game())
        pass
    gameState = setUpGame(2)

    game = Game(**gameState)
    
    while not game.lastRound:
        game.playTurn()
    
    while game.currentPlayer != game.ended:
        game.playTurn()

    game.score()