"""
Golf Unit Tests
By Cato Cannizzo
02/2026
This file contains the unit tests some of the classes 
and methods used in my golf game objects.

It checks that the cards calculate their own score correctly.
The game calculates hand score correctly.
The game loads and saves correctly.
"""

import unittest
import os
from Golf import load
from GameObjects import *

class TestGolfRules(unittest.TestCase):
    '''Suite of unit tests for core rules 
    and data persistence of Golf card Game'''
    def setUp(self):
        '''Initializes variables to check a standard game of golf'''
        self.k = Card('♠', 'K', True)
        self.k_flipped = Card('♠', 'K', False)
        self.q = Card('♠','Q',False)
        self.j = Card('♠','J',True)
        self.a = Card('♠', 'A', False)
        self.two = Card('♠', '2', True)
        self.cards = [self.k,self.q,self.a,self.k_flipped,self.j,self.two]
        self.player = Player(self.cards, "TestPlayer")
        self.deck = Deck()
        self.game = Game([self.player],self.deck)
        self.test_save_ = "dummySave.txt"

    def test_card_values(self):
        '''Checks that cards can score themselves correctly within golf rules. 
        For Example: Kings = 0, Queens and Jacks = 10, Aces = 1'''
        self.assertEqual(self.k.get_value(), 0)
        self.assertEqual(self.q.get_value(), 10)
        self.assertEqual(self.j.get_value(), 10)
        self.assertEqual(self.a.get_value(), 1)
        self.assertEqual(self.two.get_value(), 2)

    def test_vert_score(self):
        '''Checks the game player object can calculate hand score 
        correctly within golf rules. E.G. Vertical pairs = 0'''
        # Defined above, but checking that flipped card do not effect score
        # Also checks that none matching faces & numbers do not cancel
        p = self.player
        self.assertEqual(p.calc_score(),23)

        cards2=[self.k,self.a,self.q,self.k,self.two,self.q]
        p2 = Player(cards2)
        self.assertEqual(p2.calc_score(),3)

    def test_save(self):
        '''Test the ability to save to a file'''
        self.game.save(self.test_save_)
        self.assertTrue(os.path.exists(self.test_save_))

    def test_load(self):
        '''Tests the ability to load game state correctly 
        when combined with the test_save above'''
        self.game.save(self.test_save_)
        loaded_game = Game(**load(self.test_save_))
        self.assertEqual(loaded_game.players[0].name, self.player.name)
        for i in range(len(self.cards)):
            self.assertEqual(loaded_game.players[0].get_hand()[i].rank, self.player.get_hand()[i].rank)
        # !!! Create magic fun of __eq__ for Deck
        self.assertEqual(len(loaded_game.discard), len(self.game.discard))
        self.assertEqual(len(loaded_game.deck), len(self.game.deck))
        self.assertEqual(loaded_game.current_player, self.game.current_player)
    
    def tearDown(self):
        try:
            os.remove(self.test_save_)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()