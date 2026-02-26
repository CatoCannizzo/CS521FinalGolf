"""
Golf Objects
By Cato Cannizzo
02/2026
This file contains the objects and object methods for a game of golf

These are Deck, Card, Player, Game
The Game object handles majority of work such as:
displaying state to user, scoring, and saving.
"""
import random
import json
from GeneralFunctions import prompt_user

class Deck:
    '''A container object of cards.
      Takes a card or list of cards, 
      creates itself shuffled if not given arguments
      '''
    def __init__(self, order=None):
        '''Creates a deck, if order if provided uses that,
        otherwise creates a shuffled deck'''
        # Definition of a deck as private sets
        __suits = {'♠', '♣', '♡', '♢'}
        __ranks = {'2','3','4','5','6','7','8','9','10','K','Q','J','A'}
        if order:
            if isinstance(order, list):
                self.deck = order
            else:
                self.deck = [order]
        else:
            self.deck = []
            for suit in __suits:
                for rank in __ranks:
                    self.deck.append(Card(suit,rank, False))
            random.shuffle(self.deck)
        
    def __str__(self):
        '''Returns a user understandable deck of cards.
        Basically what you would see if you looked at a stack
        of cards on a table.'''
        return f"A deck of {len(self.deck)} playing cards"
    
    def __repr__(self):
        '''Returns a deconstructed deck of card for reproduction'''
        return str([str(card) for card in self.deck])
    
    def deal(self, flip:bool = False):
        ''''Removes and returns the top card from deck.
        Takes arg for if the card should be flipped as well.
        '''
        try:
            card: Card = self.deck.pop()
            if flip:
                card.flip()
            return card
        except IndexError:
            print("Error: Attempted to draw from an empty deck!")
        return None
    
    def add(self, card):
        '''Adds a card to the deck'''
        self.deck.append(card)

    def __getitem__(self, index):
        '''Allows for list-style indexing of a deck'''
        return self.deck[index]
    
    def __len__(self):
        '''Returns the number of cards in deck'''
        return len(self.deck)

class Card:
    '''Represents a playing card with suite, rank, and ability to be flipped'''

    # Private attribute to prvent other code from changing values
    __rank_values = {
        'K':0, 'Q':10, 'J':10, 'A':1
    }

    def __init__(self, suit, rank, face_up = False):
        '''Inits a card with suite, rank, and optional status of flipped'''
        self.suit = suit
        self.rank = rank
        self.face_up = face_up
    
    def __str__(self):
        '''Returns a  user friendly version of a card, as a string.'''
        if(self.face_up):
            return f"{self.rank} of {self.suit}. Currently face_up"
        else:
            return f"{self.rank} of {self.suit}"
    
    def flip(self):
        '''Flips card:
        Toggles status of card face_up'''
        self.face_up = not self.face_up

    def get_value(self):
        '''Returns score value of card not considering vertical pairs 
        in golf rules.
        Kings = 0, Queen and J = 10, Aces = 1
        '''
        if self.rank in self.__rank_values:
            return self.__rank_values[self.rank]
        
        else: return int(self.rank) 

    def __repr__(self):
        '''Returns a deconstructed card for packing (Save & Load)'''
        return{"suit": self.suit, "rank":self.rank, "face_up":self.face_up}

class Player:
    '''Represents all variables of a player in the game. 
    Their hand is a 2x3 grid of cards'''
    # Tuple constant for grid shape for programtic changes to hand size
    GRID_SHAPE = (2,3)

    def __init__(self, cards: list, name:str="player"):
        '''Inits a player with names, 
        takes 6 cards and turns it into a 2x3 hand'''
        self.name = name
        hand_size = Player.GRID_SHAPE[0]*Player.GRID_SHAPE[1]
        if len(cards) != (hand_size):
            raise ValueError(f"Invalid hand size, expected {hand_size}"\
                             f" cards but recieved {len(cards)}")
        self.grid = []
        for row_index in range(self.GRID_SHAPE[0]):
            row_start = row_index * Player.GRID_SHAPE[1]
            row_end = row_start + Player.GRID_SHAPE[1]
            self.grid.append(cards[row_start:row_end])

    def check_finished(self):
        '''If hand is all face up, returns True (and if so game should end)'''
        hand = self.get_hand()
        print("checking finished")
        if all(card.face_up for card in hand):
            return True
        return False

    def get_hand(self):
        '''Flattens 2x3 hand structure back to list of 6 cards (returned)'''
        cards = []
        for row in self.grid:
            for card in row:
                cards.append(card)
        return cards

    def __str__(self):
        '''Displays user friendly string for a players hand'''
        hand_str=f"{self.name}'s hand:"
        hand = self.get_hand()
        for i in range(len(hand)):
            hand_str += str(hand[i]) + "|"
            if i%3 == 0:
                hand_str += "\n|"
        return hand_str
    
    def calc_score(self):
        '''Calculates a hand's Golf score
        So vertical pairs become 0 points'''
        total = 0
        hand = self.grid
        for col in range(Player.GRID_SHAPE[1]):
            card_top = hand[0][col]
            card_bot = hand[1][col]
            if card_top.rank == card_bot.rank:
                #Does nothing because the cards cancel
                # !!! Revise if adding Jokers
                pass
            else:
                total += card_top.get_value()
                total += card_bot.get_value()
        return total
    
    def __repr__(self):
        '''Returns a deconstructed representation of player for reproduction
        E.g. Save and Load mechanics'''
        cards = self.get_hand()
        cards_JSON = []
        for c in cards:
            cards_JSON.append(c.__repr__())
        return {
            "name": self.name,
            "grid": cards_JSON
        }
    
class Game:
    '''Has methods for all controls of game state
      and saves all game states!'''
    def __init__(self, 
                 players:list[Player], 
                 deck:Deck, 
                 discard: Deck=None,
                 last_round=False,
                 current_player=0,
                 row_length=((11+4)*Player.GRID_SHAPE[1]),
                 message=None,
                 ended=None,
                 save_path=None):
        '''Inits the game state with players, deck mandatory'''
        # row_length = card length (11) + space between cards (4) * cards in row

        self.players = players
        self.deck = deck
        self.discard = discard if discard else Deck(self.deck.deal(True))
        self.last_round = last_round
        self.current_player = current_player
        self.row_length = row_length
        self.active_card = None
        self.message = message
        self.ended = ended
        self.__savePath = save_path

    def __get_card_by_line(self, card:Card):
        '''A private helper function to return a list of strings for cards in ASCII'''
        width = 9
        # Filler must be one chacter to work with center below
        filler = "·"
        # If check here to create a 'back' for face down cards
        if card.face_up:
            top_rank = "|" + str(card.rank).ljust(width) + "|"
            mid_line = "|" + str(card.suit).center(width) + "|"
            bot_rank = "|" + str(card.rank).rjust(width) + "|"
            spacer = "|" + " "*width + "|"

        else:
            spacer = "|" + filler*width + "|"
            top_rank = spacer
            mid_line = "|" + "GOLF".center(width, filler) + "|"
            bot_rank = spacer

        top_line = " " + "_"*width + " "
        bot_line = " " + "‾"*width + " "

        string_display =  [top_line,top_rank,spacer,mid_line,spacer,bot_rank,bot_line]
        return string_display

    def __display_by_line(self, cards:list, player_hand:int = 0):
        '''A private helper function that prints multiple cards side by side 
        (for displaying a hand)'''
        # Cards are currently 7 lines tall
        cards_display = [""for i in range(7)]

        # Need to print card number next to a players hand for UI intuitiveness
        if player_hand:
            for i in range(0,len(cards)):
                card_by_line = self.__get_card_by_line(cards[i])
                for j in range(0,len(cards_display)):
                    if player_hand == 1 and j == 0:
                        cards_display[j] +=f"{i+1})"+card_by_line[j] + "   "
                    elif player_hand == 2 and j == 0:
                        cards_display[j] +=f"{i+4})"+card_by_line[j] + "   "
                    else:
                        cards_display[j] +="  " +card_by_line[j] + "   "

        # Otherwise prints list of cards given
        else:  
            for card in cards:
                card_by_line = self.__get_card_by_line(card)
                for i in range(0,len(cards_display)):
                    cards_display[i] +=card_by_line[i] + "   "

        for line in cards_display:
            print(line.center(self.row_length))

    def display_game_state(self, player:Player=None, not_active=False):
        '''Clears terminal and displays the current game board and active hand
        Does not handle score displays'''
        # clears terminal according to:
        # https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
        print("\033[H\033[J", end="")
        
        # Lets user know how many more cards there are in the deck
        print(self.deck)

        # Define the player if given a non active player
        if player:
            p = player
        else:
            p = self.players[self.current_player]
        
        # If in the middle of an action stop displaying decks
        if self.active_card:
            print('You drew:'.center(self.row_length,'-'))
            self.__display_by_line([self.active_card])
        else:
            deck_names = "Deck:"+"-"*7+"Discard:"
            print(deck_names.center(self.row_length,'-'))
            self.__display_by_line([self.deck[-1], self.discard[-1]])
        
        # Prints warning if not looking at own hand
        if not_active:
            print(f"{p.name}'s hand (NOT ACTIVE PLAYER'S HAND)".center(self.row_length,'-'))
        else:
            print(f"{p.name}'s hand".center(self.row_length,'-'))
        for index, row in enumerate(p.grid):
            self.__display_by_line(row, index+1)
   
    def swap_card(self, target:int=None):
        '''Swaps the active card 
        with a card in the player's grid or discard
        Optional arg allows targeting of things other than discard pile'''
        if target:
            row = (target-1)//Player.GRID_SHAPE[1]
            col = (target-1)%Player.GRID_SHAPE[1]
            player = self.players[self.current_player]
            player_cards = player.grid
            target_card = player_cards[row][col]
            player_cards[row][col] = self.active_card
            if not target_card.face_up:
                target_card.flip()
            self.active_card = target_card

        self.discard.add(self.active_card)
        self.active_card = None
    
    def place_card(self):
        '''Gets user input for where to put a new card
        Calls swap card'''
        action_list=['1','2','3', '4', '5', '6', 'q']
        turn_prompt="What would you like to do? \n"\
        "(1-6) Replace cards 1-6 from your hand with the card you drew\n"\
        "(q) Discard the card you drew into the discard pile"

        user_input: str = prompt_user(str,turn_prompt,0,2,False,action_list).lower()
        if user_input.isnumeric():
            self.swap_card(int(user_input))
        elif user_input == 'q':
             self.swap_card()
        else:
            raise ValueError(f"User input here should have only exepted 1-6 and q. You managed to break the game!")

    def draw(self,from_deck:bool = True):
        '''Draws a card from deck, optional arg to draw from discard instead'''
        if from_deck:
            self.active_card = self.deck.deal(True)
        else:
            self.active_card = self.discard.deal()

    def change_view(self):
        '''Allows the current player to view hand of another'''
        current = self.players[self.current_player]
        # Removes current player from list
        others = [player for player in self.players if player != current]
        if others:
            players_list = enumerate(others)
            players_str = ", ".join([f"{k+1}: {v.name}" for k, v in players_list])
            choose_player="Please choose select the number of the following players to see the board state of:\n"\
            f"{players_str}"
            p_num = prompt_user(int,choose_player,0,5,in_list = [k+1 for k in players_list])
            self.display_game_state(others[p_num-1], True)
            input("\nViewing other player. Press Enter to return to your hand...")
        # Prevents call if playing by self
        else:
            self.message= "You can't view other players hands when playing by youself!"

    def get_action(self):
        '''Collects user input for which action to take in a game'''

        action_list=['e','q','w','r']
        turn_prompt="What would you like to do? \n"\
        "(Q) Draw from the deck\n"\
        "(W) Draw from the discard\n"\
        "(E) View another players hand\n"\
        "(R) Save game state"
        if self.message:
            print(self.message)
            self.message = None
        user_input = prompt_user(str,turn_prompt,0,2,False,action_list).lower()

        return user_input
    
    def play_turn(self):
        '''Handles turn logic, and which method to call from which state'''
        # While loop to allow user to view and safe freely
        current_turn = True
        while current_turn:
            # 1st displays game state to user
            self.display_game_state()
           
            # If user takes action to grab card (below) handle that here
            if self.active_card:
                self.place_card()
                current_turn = False

            # Get user input 
            else:
                # Checks if round is ending and provides message if so
                if self.last_round:
                    print(f"{self.players[self.ended].name} ended the game!\n"\
                    "All other players: This is your last round.")
                user_input = self.get_action()
                if user_input == 'e':
                    self.change_view()
                    continue
                if user_input == 'q':
                    self.draw(from_deck=True)
                if user_input == 'w':
                    self.draw(from_deck=False)
                if user_input == 'r':
                    self.save(self.__savePath)
        # If game ended after player action flip all cards
        if  self.last_round:
            hand = self.players[self.current_player].get_hand()
            for card in hand:
                if not card.face_up:
                    card.flip()
        # After player selects action check if trigger last round
        # Don't need to check if game already ended
        else:
            if self.players[self.current_player].check_finished() or len(self.deck) == len(self.players):
                self.last_round = True
                self.ended = self.current_player
        # Last game state display to show what the player changed
        # Includes warning if game is ending soon
        self.display_game_state()
        print(f"\n{self.players[self.current_player].name}, your turn is complete.")
        if self.last_round and self.current_player!= self.ended:
            print("\nAll cards flipped for game end scoring!")
        input("Press enter to pass the turn to the next player...")  
        # Move next player
        self.current_player = (self.current_player+1) % len(self.players)

    def score(self):
        '''Calculates and displays game ending scores'''
        print("\033[H\033[J", end="")
        print("Final Scores:".center(self.row_length,'='))
            
        scores = [{"player":player.name, "score":player.calc_score()}\
                   for player in self.players]  
        scores.sort(key=lambda x:x["score"])
        for i in range(len(scores)):
            # Tie logic
            # If not the first player and in tie skip display
            if i != 0 and scores[i]['score'] == scores[i-1]['score']:
                continue
            # If in tie collect all tieing players and display all at once
            elif i != len(scores)-1 and scores[i]['score'] == scores[i+1]['score']:
                tie_score = scores[i]['score']
                tie_players = [j for j in scores if j['score'] == tie_score]
                for player in tie_players:
                    print(f"{i+1}) TIE! {player['player']} got {tie_score} points!")
            # If not in tie display rank as normal
            else: print(f"Rank: {i+1} {scores[i]['player']} got {scores[i]['score']} points!")
    
    def save(self, save_file:str =None):
        '''Saves game state as JSON file'''
        # Collect game state
        data = {
            "current_player":self.current_player,
            "last_round": self.last_round,
            "ended":self.ended,
            "message":self.message,
            "row_length":self.row_length,
            "players": [p.__repr__() for p in self.players],
            "discard": [c.__repr__() for c in self.discard],
            "deck": [c.__repr__() for c in self.deck]
        }
        # Save state
        while True:
            if save_file:
               game_name = save_file
            else:
                game_name = prompt_user(str, "Input save name:", 1, 14, not_list=["*","/","\\", "?"])
            # If save successful go back to main game loop
            try:
                with open(game_name, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                
            except PermissionError as e:
                print(f"Error: Permission denied. {e}")
                break 
            except OSError as e:
                print(f"Error: Invalid filename. {e}")
            else:
                self.message=f'Successfully saved to {game_name}! Press Cntl + C to leave program'
                break
