import random
from GeneralFunctions import promptUser
from os import system

class Deck:
    def __init__(self, order=None):
        suits = ['♠', '♣', '♡', '♢']
        ranks = ['2','3','4','5','6','7','8','9','10','K','Q','J','A']
        if order:
            self.deck = [order]
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
    def deal(self, flip:bool = False):
        card: Card = self.deck.pop()
        if flip:
            card.flip()
        return card
    def add(self, card):
        self.deck.append(card)

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
    
    def flip(self):
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
        self.discard = discard if discard else Deck(self.deck.deal(True))
        self.lastRound = False
        self.currentPlayer = players[0]
        self.rowLength = 9*3+5*3
        self.activeCard = None
        self.playerNotActive = False
        self.message = None

    def getCardbyLine(self, card:Card):
        width = 9
        # Filler must be one chacter to work with center below
        filler = "·"

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

    def displayByLine(self, cards:list, playerHand:int = 0):
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

    def displayGameState(self, player:Player=None):
        system("clear||cls")        
        print(self.deck)
        if player:
            p = player
        else:
            p = self.currentPlayer

        if self.activeCard:
            print('You drew:'.center(self.rowLength,'-'))
            self.displayByLine([self.activeCard])
        else:
            deckNames = "Deck:"+"-"*7+"Discard:"
            print(deckNames.center(self.rowLength,'-'))
            self.displayByLine([self.deck[-1], self.discard[-1]])
        if self.playerNotActive:
            print(f"{p.name}'s hand (NOT ACTIVE PLAYER'S HAND)".center(self.rowLength,'-'))
        else:
            print(f"{p.name}'s hand".center(self.rowLength,'-'))
        for index, row in enumerate(p.grid):
            self.displayByLine(row, index+1)

    
    def swapCard(self, target:int=None):
        if target:
            col = (target-1)//3
            row = (target-1)%3
            targetCard:Card = self.currentPlayer.grid[col][row]
            self.currentPlayer.grid[col][row] = self.activeCard
            if not targetCard.faceUp:
                targetCard.flip()
            self.activeCard = targetCard

        self.discard.add(self.activeCard)
        self.activeCard = None
    
    def placeCard(self):
        actionList=['1','2','3', '4', '5', '6', 'q']
        turnPrompt="What would you like to do? \n"\
        "(1-6) Replace cards 1-6 from your hand with the card you drew\n"\
        "(q) Discard the card you drew into the discard pile"

        userInput: str = promptUser(str,turnPrompt,0,2,False,actionList).lower()
        if userInput.isnumeric():
            self.swapCard(int(userInput))
        elif userInput == 'q':
             self.swapCard()
        else:
            raise ValueError(f"User input here should have only exepted 1-6 and q. You managed to break the game!")

    def draw(self,drawFromDeck:bool = True):
        if drawFromDeck:
            self.activeCard = self.deck.deal(True)
        else:
            self.activeCard = self.discard.deal()

    def changeView(self):
        otherPlayers = [player.name for player in self.players].remove(self.currentPlayer.name)
        if otherPlayers:
            playersList = enumerate(otherPlayers)
            playersStr = ", ".join([f"{k+1}: {v}" for k, v in playersList])
            choosePlayer="Please choose select the number of the following players to see the board state of:\n"\
            f"{playersStr}"
            pNum = promptUser(int,choosePlayer,0,5,inList = [k+1 for k in playersList])
            self.playerNotActive = True
            self.displayGameState(self.players[pNum-1])
        else:
            self.message= "You can't view other players hands when playing by youself!"

    def getAction(self):
        actionList=['v','q','w']
        turnPrompt="What would you like to do? \n"\
        "(V) View another players hand\n"\
        "(Q) Draw from the deck\n"\
        "(W) Draw from the discard"
        if self.playerNotActive:
            turnPrompt+="\n(R) Return to your hand view"
            actionList.append("r")
        if self.message:
            print(self.message)
            self.message = None
        userInput = promptUser(str,turnPrompt,0,2,False,actionList).lower()

        return userInput
    

    def playTurn(self):
        currentTurn = True
        while currentTurn:
            self.displayGameState()
           
            if self.activeCard:
                self.placeCard()
            
            else:
                userInput = self.getAction()

                if userInput == 'v':
                    self.changeView()
                self.playerNotActive
                if userInput == 'r':
                    self.displayGameState()
                if userInput == 'q':
                    self.draw(drawFromDeck=True)
                if userInput == 'w':
                    self.draw(drawFromDeck=False)

        

            


  