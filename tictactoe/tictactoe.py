"""
The module tictactoe contains the Game class which holds a game of Tic Tac Toe.

game = Game()          constructs a new game with an empty board
game = Game(state)     constructs a game in the given <state>
game.getState()        retrieves the same <state>
game.executeMove(move) makes the current player execute the given <move>;
                       returns True if this move is legal, False otherwise
game.board             contains the game board as a list of integers, where
                       0 = empty, 1&2 = occupied by the respective player
self.data              contains some interpretations of the current game state:
self.data["whosTurn"]  is 1, 2, or None if the game is finished
self.data["winner"]    is 1, 2, or None if the game is not finished or drawn
self.data["finished"]  is True or False

See below the class for test code; do "python <thisfile>" to run
"""

##############################################################################
##############################################################################

class Game:
    def getState(self):
        '''Output a single number between 0 and 19682, which completely identifies the game state'''
        return int(''.join([str(code) for code in self.board]), base = 3)
    
    def move(self, move):
        if move < 0 or move > 8 \
        or self.board[move] or self.data["whosTurn"] is None:
           return False 

        self.board[move] = self.data["whosTurn"]
        self.__interpretPosition__()
        return True



    def __init__(self, setup = None):
        self.board = [0] * 9
        if setup:
            for pos in range(9).__reversed__():
                self.board[pos] = setup % 3
                setup = int(setup / 3)
        self.__interpretPosition__()

    def __interpretPosition__(self):
        self.data = { "whosTurn": None, "winner": None, "finished": False }

        # Check victory conditions:
        self.data["winner"] = self.__findWinner__()

        # Check game end (victory or board is full)
        if self.data["winner"] or not self.board.count(0):
            self.data["finished"] = True
        else:
            # Find out who is up next
            self.data["whosTurn"] = 1 if self.board.count(1) <= self.board.count(2) else 2

    def __findWinner__(self):
        winners = []
        # I) columns
        winners.append(Game.isWinner(self.board[0:3]))
        winners.append(Game.isWinner(self.board[3:6]))
        winners.append(Game.isWinner(self.board[6:9]))
        # II) rows
        winners.append(Game.isWinner(self.board[0::3]))
        winners.append(Game.isWinner(self.board[1::3]))
        winners.append(Game.isWinner(self.board[2::3]))
        # III) diagonals
        winners.append(Game.isWinner(self.board[0::4]))
        winners.append(Game.isWinner(self.board[2:7:2]))

        for winner in [1, 2]:
            if winners.count(winner):
                return winner

    @staticmethod
    def isWinner(line):
        for winner in [1, 2]:
            if line.count(winner) == 3:
                return winner

##############################################################################
##############################################################################

import unittest

class TestGame(unittest.TestCase):
    def testInit(self):
        game = Game()
        self.assertListEqual(game.board, [0] * 9)
        self.assertDictEqual(game.data, {'whosTurn': 1, 'winner': None, 'finished': False})
        self.assertEqual(game.getState(), 0)

    def testValidMoves(self):
        game = Game()
        self.assertEqual(game.board, [0] * 9)
        self.assertTrue(game.move(4))
        self.assertTrue(game.move(0))
        self.assertTrue(game.move(1))
        self.assertEqual(game.board, [2, 1, 0, 0, 1, 0, 0, 0, 0])
        self.assertDictEqual(game.data, {'whosTurn': 2, 'winner': None, 'finished': False})
        self.assertEqual(game.getState(), 15390)

    def testRestore(self):
        game = Game(15390)
        self.assertEqual(game.board, [2, 1, 0, 0, 1, 0, 0, 0, 0])
        self.assertDictEqual(game.data, {'whosTurn': 2, 'winner': None, 'finished': False})
        self.assertEqual(game.getState(), 15390)

    def testInvalidMoves(self):
        game = Game(15390)
        self.assertFalse(game.move(4))
        self.assertFalse(game.move(0))
        self.assertFalse(game.move(1))
        self.assertTrue(game.move(3))
        self.assertTrue(game.move(7))
        for i in range(9):
            self.assertFalse(game.move(i))

    def testGameEndWinner1(self):
        game = Game(15390)
        self.assertTrue(game.move(3))
        self.assertTrue(game.move(7))
        self.assertEqual(game.board, [2, 1, 0, 2, 1, 0, 0, 1, 0])
        self.assertDictEqual(game.data, {'whosTurn': None, 'winner': 1, 'finished': True})

    def testGameEndWinner2(self):
        game = Game(15390)
        self.assertTrue(game.move(3))
        self.assertTrue(game.move(8))
        self.assertTrue(game.move(6))
        self.assertEqual(game.board, [2, 1, 0, 2, 1, 0, 2, 0, 1])
        self.assertDictEqual(game.data, {'whosTurn': None, 'winner': 2, 'finished': True})

    def testGameEndDraw(self):
        game = Game(17214)
        self.assertTrue(game.move(8))
        self.assertEqual(game.board, [2, 1, 2, 1, 2, 1, 1, 2, 1])
        self.assertDictEqual(game.data, {'whosTurn': None, 'winner': None, 'finished': True})
        

if __name__ == '__main__':
    unittest.main()
