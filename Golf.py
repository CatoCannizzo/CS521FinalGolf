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
    suits = ['♠', '♣', '♡', '♢']
    ranks = ['2','3','4','5','6','7','8','9','10','K','Q','J','A']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(Card(suit,rank, random.randint(0,1)))
    
    random.shuffle(deck)
    hand = []
    for x in range(6):
        hand.append(deck.pop())
    TestHand = Hand(hand)
    print(TestHand)
    print("Should be 3 columns and two rows  cards, random each time")

class Card:
    def __init__(self, suit, rank, faceUp = False):
        self.__suit = suit
        self.__rank = rank
        self.faceUp = faceUp
    
    def __str__(self):
        if(self.faceUp):
            return f"{self.__rank} of {self.__suit}. Currently faceup"
        else:
            return f"{self.__rank} of {self.__suit}. Currently facedown"
        
    def displayCard(self):
        width = 9
        # Filler must be one chacter to work with center below
        filler = "·"
        if self.faceUp:
            topRank = "|" + str(self.__rank).ljust(width) + "|"
            midLine = "|" + str(self.__suit).center(width) + "|"
            botRank = "|" + str(self.__rank).rjust(width) + "|"
            spacer = "|" + " "*width + "|"

        else:
            spacer = "|" + filler*width + "|"
            topRank = spacer
            midLine = "|" + "GOLF".center(width, filler) + "|"
            botRank = spacer
            


        topLine = " " + "_"*width + " "
        botLine = " " + "‾"*width + " "

        stringDisplay =  [topLine,topRank,spacer,midLine,spacer,botRank,botLine]
        return stringDisplay


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
        rowStr="Current Hand:\n"
        for row in self.grid:
            cardsDisplay = [""for i in range(7)]
            for card in row:
                cardByLine=card.displayCard()
                for i in range(len(cardByLine)):
                    cardsDisplay[i] +=cardByLine[i] + "   "
            for line in cardsDisplay:
                print(line)
            
        return rowStr


            

if __name__ == "__main__":
    # start_game()
    deal()