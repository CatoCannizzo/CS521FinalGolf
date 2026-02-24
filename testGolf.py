import unittest
from GameObjects import *

class testGolfRules(unittest.TestCase):
    def setUp(self):
        self.k = Card('♠', 'K', True)
        self.q = Card('♠','Q',True)
        self.j = Card('♠','J',True)
        self.a = Card('♠', 'A', True)
        self.two = Card('♠', '2', True)

    def testCardValues(self):
        self.assertEqual(self.k.getValue(), 0)
        self.assertEqual(self.q.getValue(), 10)
        self.assertEqual(self.j.getValue(), 10)
        self.assertEqual(self.a.getValue(), 1)
        self.assertEqual(self.two.getValue(), 2)

    def testVertScore(self):
        cards = [self.k,self.q,self.a,self.k,self.j,self.two]
        p = Player(cards)
        self.assertEqual(p.calcScore(),23)

        cards2=[self.k,self.a,self.q,self.k,self.two,self.q]
        p2 = Player(cards2)
        self.assertEqual(p2.calcScore(),3)

if __name__ == '__main__':
    unittest.main()



