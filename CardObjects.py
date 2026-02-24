import random

class Deck:
    def __init__(self, order=None):
        suits = ['♠', '♣', '♡', '♢']
        ranks = ['2','3','4','5','6','7','8','9','10','K','Q','J','A']
        if order:
            self.deck = order
        else:
            self.deck = []
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit,rank, False))
            random.shuffle(self.deck)
    def __str__(self):
        return f"A deck of {len(self.deck)} playing cards"
    def __repr__(self):
        return str([str(card) for card in self.deck])
    def deal(self, faceup:bool = False):
        card: Card = self.deck.pop()
        if faceup:
            card.turn()
        return card

        return    
    def __getitem__(self, index):
        return self.deck[index]
    def __len__(self):
        return len(self.deck)

class Card:
    def __init__(self, suit, rank, faceUp = False):
        self.suit = suit
        self.rank = rank
        self.faceUp = faceUp
    
    def __str__(self):
        if(self.faceUp):
            return f"{self.rank} of {self.suit}. Currently faceup"
        else:
            return f"{self.rank} of {self.suit}"
    
    def turn(self):
        self.faceUp = not self.faceUp
        
class Player:
    def __init__(self, cards: list, name="player"):
        self.name = name
        if len(cards) != 6:
            raise ValueError(f"Invalid hand size, expected 6 cards but recieved {len(cards)}")
        self.grid = [cards[0:3],cards[3:6]]

    def swap(self, position):
        pass
    def peek(self, position):
        pass
    def getHand(self):
        return self.grid

    def __str__(self):
        rowStr=f"{self.name}'s hand:"
        for row in self.grid:
            rowStr += "\n|"
            for card in row:
                rowStr += str(card) + " | "
        return rowStr


class Game:
    def __init__(self, players:list[Player], deck:Deck, discard: list[Card]=None):
        self.players = players
        self.deck = deck
        self.discard = discard if discard else [self.deck.deal(True)]
        self.lastRound = False
        self.currentPlayer = players[0]
        self.rowLength = 9*3+5*3

    def getCardbyLine(self, card):
        width = 9
        # Filler must be one chacter to work with center below
        filler = "·"
        if not isinstance(card,Card):
           card:Card = card[-1] 

        if card.faceUp:
            topRank = "|" + str(card.rank).ljust(width) + "|"
            midLine = "|" + str(card.suit).center(width) + "|"
            botRank = "|" + str(card.rank).rjust(width) + "|"
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

    def displayLine(self, cards:list, playerHand:int = 0):
        cardsDisplay = [""for i in range(7)]
        if playerHand:
            for i in range(0,len(cards)):
                cardByLine = self.getCardbyLine(cards[i])
                for j in range(0,len(cardsDisplay)):
                    if playerHand == 1 and j == 0:
                        cardsDisplay[j] +=f"{i+1})"+cardByLine[j] + "   "
                    elif playerHand == 2 and j == 0:
                        cardsDisplay[j] +=f"{i+4})"+cardByLine[j] + "   "
                    else:
                        cardsDisplay[j] +="  " +cardByLine[j] + "   "
        else:  
            for card in cards:
                cardByLine = self.getCardbyLine(card)
                for i in range(0,len(cardsDisplay)):
                    cardsDisplay[i] +=cardByLine[i] + "   "

        for line in cardsDisplay:
            print(line.center(self.rowLength))

    def displayGameState(self):
        p = self.currentPlayer
        deckNames = "Deck:"+"-"*7+"Discard:"
        print(deckNames.center(self.rowLength,'-'))
        self.displayLine([self.deck, self.discard])
        print(f"{p.name}'s hand".center(self.rowLength,'-'))
        for index, row in enumerate(p.grid):
            self.displayLine(row, index+1)

    def playTurn(self):
        self.displayGameState()
        

            


  