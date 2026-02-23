from GeneralFunctions import promptUser
import random

def start_game():
    print("Welcome to the card game Golf!")
    rulesPrompt = "Would you like a rules overviewfor this game? (y/n)"
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

def deal():
    suits = ['S', 'C', 'H', 'D']
    ranks = ['2','3','4','5','6','7','8','9','10','K','Q','J','A']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(Card(suit,rank,True))
    
    random.shuffle(deck)
    hand = []
    for x in range(6):
        hand.append(deck.pop())
    TestHand = Hand(hand)
    print(TestHand)
    print("Should be 3 columns and two rows  ?")

class Card:
    def __init__(self, suit, rank, faceDown = True):
        self.__suit = suit
        self.__rank = rank
        self.faceDown = faceDown
    
    def __str__(self):
        if(not self.faceDown):
            return f"{self.rank} of {self.suit}"
        else:
            return "?"

class Hand:
    def __init__(self, cards: list):
        if len(cards) != 6:
            raise ValueError(f"Invalid hand size, expected 6 cards but recieved {len(cards)}")
        self.grid = [cards[0:3],cards[3:6]]
    def swap(self, position):
        pass
    def peek(self, position):
        pass
    def __str__(self):
        rowStr="Current Hand:"
        for row in self.grid:
            rowStr += "\n|"
            for card in row:
                rowStr += str(card) + " | "
        return rowStr


            

if __name__ == "__main__":
    # start_game()
    deal()