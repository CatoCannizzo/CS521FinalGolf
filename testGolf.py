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

class testGolfRules(unittest.TestCase):
    '''Suite of unit tests for core rules 
    and data persistence of Golf card Game'''
    def setUp(self):
        '''Initializes variables to check a standard game of golf'''
        self.k = Card('♠', 'K', True)
        self.kFlipped = Card('♠', 'K', False)
        self.q = Card('♠','Q',False)
        self.j = Card('♠','J',True)
        self.a = Card('♠', 'A', False)
        self.two = Card('♠', '2', True)
        self.cards = [self.k,self.q,self.a,self.kFlipped,self.j,self.two]
        self.player = Player(self.cards, "TestPlayer")
        self.deck = Deck()
        self.game = Game([self.player],self.deck)
        self.testSave = "dummySave.txt"

    def testCardValues(self):
        '''Checks that cards can score themselves correctly within golf rules. 
        For Example: Kings = 0, Queens and Jacks = 10, Aces = 1'''
        self.assertEqual(self.k.getValue(), 0)
        self.assertEqual(self.q.getValue(), 10)
        self.assertEqual(self.j.getValue(), 10)
        self.assertEqual(self.a.getValue(), 1)
        self.assertEqual(self.two.getValue(), 2)

    def testVertScore(self):
        '''Checks the game player object can calculate hand score 
        correctly within golf rules. E.G. Vertical pairs = 0'''
        # Defined above, but checking that flipped card do not effect score
        # Also checks that none matching faces & numbers do not cancel
        p = self.player
        self.assertEqual(p.calcScore(),23)

        cards2=[self.k,self.a,self.q,self.k,self.two,self.q]
        p2 = Player(cards2)
        self.assertEqual(p2.calcScore(),3)

    def testSave(self):
        '''Test the ability to save to a file'''
        self.game.save(self.testSave)
        self.assertTrue(os.path.exists(self.testSave))

    def testLoad(self):
        '''Tests the ability to load game state correctly 
        when combined with the testSave above'''
        loadedGame = Game(**load(self.testSave))
        self.assertEqual(loadedGame.players[0].name, self.player.name)
        for i in range(len(self.cards)):
            self.assertEqual(loadedGame.players[0].getHand()[i].rank, self.player.getHand()[i].rank)
        # !!! Create magic fun of __eq__ for Deck
        self.assertEqual(len(loadedGame.discard), len(self.game.discard))
        self.assertEqual(len(loadedGame.deck), len(self.game.deck))
        self.assertEqual(loadedGame.currentPlayer, self.game.currentPlayer)


if __name__ == '__main__':
    unittest.main()