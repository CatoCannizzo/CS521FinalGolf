import unittest
import json
import os
from Golf import load
from GameObjects import *

class testGolfRules(unittest.TestCase):
    def setUp(self):
        self.k = Card('♠', 'K', True)
        self.q = Card('♠','Q',True)
        self.j = Card('♠','J',True)
        self.a = Card('♠', 'A', True)
        self.two = Card('♠', '2', True)
        self.cards = [self.k,self.q,self.a,self.k,self.j,self.two]
        self.player = Player(self.cards, "TestPlayer")
        self.deck = Deck()
        self.game = Game([self.player],self.deck)
        self.testSave = "dummySave.txt"

    def testCardValues(self):
        self.assertEqual(self.k.getValue(), 0)
        self.assertEqual(self.q.getValue(), 10)
        self.assertEqual(self.j.getValue(), 10)
        self.assertEqual(self.a.getValue(), 1)
        self.assertEqual(self.two.getValue(), 2)

    def testVertScore(self):
        p = self.player
        self.assertEqual(p.calcScore(),23)

        cards2=[self.k,self.a,self.q,self.k,self.two,self.q]
        p2 = Player(cards2)
        self.assertEqual(p2.calcScore(),3)

    def testSave(self):
        self.game.save(self.testSave)
        self.assertTrue(os.path.exists(self.testSave))

    def testLoad(self):
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



