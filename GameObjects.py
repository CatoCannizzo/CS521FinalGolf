import random
import json
from GeneralFunctions import promptUser

class Deck:
    def __init__(self, order=None):
        suits = ['♠', '♣', '♡', '♢']
        ranks = ['2','3','4','5','6','7','8','9','10','K','Q','J','A']
        if order:
            if isinstance(order, list):
                self.deck = order
            else:
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

    def getValue(self):
        '''Returns score value of card not considering vertical pairs'''
        if self.rank == 'K':
            return 0
        if self.rank == 'Q' or self.rank == 'J':
            return 10
        if self.rank == 'A':
            return 1
        else: return int(self.rank) 
    def __repr__(self):
        return{"suit": self.suit, "rank":self.rank, "faceUp":self.faceUp}

class Player:
    def __init__(self, cards: list, name="player"):
        self.name = name
        if len(cards) != 6:
            raise ValueError(f"Invalid hand size, expected 6 cards but recieved {len(cards)}")
        self.grid = [cards[0:3],cards[3:6]]

    def checkFinished(self):
        hand = self.getHand()
        print("checking finished")
        if all(card.faceUp for card in hand):
            return True
        return False

    def getHand(self):
        cards = []
        for row in self.grid:
            for card in row:
                cards.append(card)
        return cards

    def __str__(self):
        handStr=f"{self.name}'s hand:"
        hand = self.getHand()
        for i in range(len(hand)):
            handStr += str(hand[i]) + "|"
            if i%3 == 0:
                handStr += "\n|"
        return handStr
    
    def calcScore(self):
        total = 0
        hand = self.grid
        for col in range(3):
            cardTop = hand[0][col]
            cardBot = hand[1][col]
            if cardTop.rank == cardBot.rank:
                pass
            else:
                total += cardTop.getValue()
                total += cardBot.getValue()
        return total
    
    def __repr__(self):
        cards = self.getHand()
        cardsJSON = []
        for c in cards:
            cardsJSON.append(c.__repr__())
        return {
            "name": self.name,
            "grid": cardsJSON
        }
    


class Game:
    def __init__(self, players:list[Player], deck:Deck, discard: Deck=None,lastRound=False,currentPlayer=0,rowLength=(11*3+4*3),message=None,ended=None):
        self.players = players
        self.deck = deck
        self.discard = discard if discard else Deck(self.deck.deal(True))
        self.lastRound = lastRound
        self.currentPlayer = currentPlayer
        self.rowLength = rowLength
        self.activeCard = None
        self.message = message
        self.ended = ended

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

    def displayGameState(self, player:Player=None, playerNotActive=False):
        # clears terminal according to:
        # https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
        print("\033[H\033[J", end="")
        
        print(self.deck)
        if player:
            p = player
        else:
            p = self.players[self.currentPlayer]
        
        if self.activeCard:
            print('You drew:'.center(self.rowLength,'-'))
            self.displayByLine([self.activeCard])
        else:
            deckNames = "Deck:"+"-"*7+"Discard:"
            print(deckNames.center(self.rowLength,'-'))
            self.displayByLine([self.deck[-1], self.discard[-1]])
        if playerNotActive:
            print(f"{p.name}'s hand (NOT ACTIVE PLAYER'S HAND)".center(self.rowLength,'-'))
        else:
            print(f"{p.name}'s hand".center(self.rowLength,'-'))
        for index, row in enumerate(p.grid):
            self.displayByLine(row, index+1)
   
    def swapCard(self, target:int=None):
        if target:
            row = (target-1)//3
            col = (target-1)%3
            player = self.players[self.currentPlayer]
            playerCards = player.grid
            targetCard = playerCards[row][col]
            playerCards[row][col] = self.activeCard
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
        current = self.players[self.currentPlayer]
        others = [player for player in self.players if player != current]
        if others:
            playersList = enumerate(others)
            playersStr = ", ".join([f"{k+1}: {v.name}" for k, v in playersList])
            choosePlayer="Please choose select the number of the following players to see the board state of:\n"\
            f"{playersStr}"
            pNum = promptUser(int,choosePlayer,0,5,inList = [k+1 for k in playersList])
            self.displayGameState(others[pNum-1], True)
        else:
            self.message= "You can't view other players hands when playing by youself!"

    def getAction(self):
        if self.lastRound:
            print(f"{self.players[self.ended].name} ended the game!\n"\
            "All other players: This is your last round.")
        actionList=['e','q','w','r']
        turnPrompt="What would you like to do? \n"\
        "(E) View another players hand\n"\
        "(Q) Draw from the deck\n"\
        "(W) Draw from the discard\n"\
        "(R) Save game state"
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
                currentTurn = False
            
            else:
                userInput = self.getAction()
                if userInput == 'e':
                    self.changeView()
                    input("\nViewing other player. Press Enter to return to your hand...")
                    continue
                if userInput == 'q':
                    self.draw(drawFromDeck=True)
                if userInput == 'w':
                    self.draw(drawFromDeck=False)
                if userInput == 'r':
                    self.save()

        print("self.lastround check")
        if  self.lastRound:
            hand = self.players[self.currentPlayer].getHand()
            for card in hand:
                if not card.faceUp:
                    card.flip()

        else:
            print("In Else")
            if self.players[self.currentPlayer].checkFinished():
                self.lastRound = True
                self.ended = self.currentPlayer

        self.displayGameState()
        print(f"\n{self.players[self.currentPlayer].name}, your turn is complete.")
        if self.lastRound and self.currentPlayer!= self.ended:
            print("\nAll cards flipped for game end scoring!")
        input("Press enter to pass the turn to the next player...")  
            
        self.currentPlayer = (self.currentPlayer+1) % len(self.players)

    def score(self):
        print("\033[H\033[J", end="")
        print("Final Scores:".center(self.rowLength,'='))
            
        scores = [{"player":player.name, "score":player.calcScore()} for player in self.players]  
        scores.sort(key=lambda x:x["score"])
        for i in range(len(scores)):

            if i != 0 and scores[i]['score'] == scores[i-1]['score']:
                continue
            elif i != len(scores)-1 and scores[i]['score'] == scores[i+1]['score']:
                tieScore = scores[i]['score']
                tiePlayers = [j for j in scores if j['score'] == tieScore]
                for player in tiePlayers:
                    print(f"{i+1}) TIE! {player['player']} got {tieScore} points!")
            else: print(f"Rank: {i+1} {scores[i]['player']} got {scores[i]['score']} points!")
    
    def save(self, saveFile:str =None):
        data = {
            "currentPlayer":self.currentPlayer,
            "lastRound": self.lastRound,
            "ended":self.ended,
            "message":self.message,
            "rowLength":self.rowLength,
            "players": [p.__repr__() for p in self.players],
            "discard": [c.__repr__() for c in self.discard],
            "deck": [c.__repr__() for c in self.deck]
        }
        
        while True:
            if saveFile:
               gameName = saveFile
            else:
                gameName = promptUser(str, "Input save name:", 1, 14, notList=["*","/","\\", "?"])
            try:
                with open(gameName, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                self.message=f'Successfully saved to {gameName}! Press Cntl + C to leave program'
                f.close()
                break 
                
            except PermissionError as e:
                print(f"Error: Permission denied. {e}")
                break 
            except OSError as e:
                print(f"Error: Invalid filename. {e}")

        
