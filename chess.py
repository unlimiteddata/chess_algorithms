# Amira Isenberg

from enum import Enum
from collections import namedtuple
# from abc import ABC, abstractmethod
from typing import Union, List, Tuple
import unittest
import copy


class PieceType(Enum):
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5
    DUMMY = 6


class Color(Enum):
    BLACK = 0
    WHITE = 1


# helper function that translates the chess position to its
# position in the 2d list:
def whatPosition(s: str) -> tuple[int, int]:
    x = 0
    y = 0

    s = s.lower()

    # first checking the letter:
    if s[0] == "a":
        y = 0
    elif s[0] == "b":
        y = 1
    elif s[0] == "c":
        y = 2
    elif s[0] == "d":
        y = 3
    elif s[0] == "e":
        y = 4
    elif s[0] == "f":
        y = 5
    elif s[0] == "g":
        y = 6
    elif s[0] == "h":
        y = 7

    # and then the number:
    if s[1] == "1":
        x = 0
    elif s[1] == "2":
        x = 1
    elif s[1] == "3":
        x = 2
    elif s[1] == "4":
        x = 3
    elif s[1] == "5":
        x = 4
    elif s[1] == "6":
        x = 5
    elif s[1] == "7":
        x = 6
    elif s[1] == "8":
        x = 7

    return x, y


# converting from where it is in the 2d array to what it is in chess
# terms:
def whatPositionReverse(pos: str) -> str:
    ans = ""
    x = ""
    y = ""

    # checking letter position:
    if pos[0] == "0":
        y = "1"
    elif pos[0] == "1":
        y = "2"
    elif pos[0] == "2":
        y = "3"
    elif pos[0] == "3":
        y = "4"
    elif pos[0] == "4":
        y = "5"
    elif pos[0] == "5":
        y = "6"
    elif pos[0] == "6":
        y = "7"
    elif pos[0] == "7":
        y = "8"

    if pos[1] == "0":
        x = "a"
    elif pos[1] == "1":
        x = "b"
    elif pos[1] == "2":
        x = "c"
    elif pos[1] == "3":
        x = "d"
    elif pos[1] == "4":
        x = "e"
    elif pos[1] == "5":
        x = "f"
    elif pos[1] == "6":
        x = "g"
    elif pos[1] == "7":
        x = "h"

    ans += x
    ans += y

    return ans


ChessPiece = namedtuple("ChessPiece", ["piece_type", "color"])
BK = ChessPiece(piece_type=PieceType.KING, color=Color.BLACK)
BQ = ChessPiece(piece_type=PieceType.QUEEN, color=Color.BLACK)
BR = ChessPiece(piece_type=PieceType.ROOK, color=Color.BLACK)
BB = ChessPiece(piece_type=PieceType.BISHOP, color=Color.BLACK)
BN = ChessPiece(piece_type=PieceType.KNIGHT, color=Color.BLACK)
BP = ChessPiece(piece_type=PieceType.PAWN, color=Color.BLACK)
WK = ChessPiece(piece_type=PieceType.KING, color=Color.WHITE)
WQ = ChessPiece(piece_type=PieceType.QUEEN, color=Color.WHITE)
WR = ChessPiece(piece_type=PieceType.ROOK, color=Color.WHITE)
WB = ChessPiece(piece_type=PieceType.BISHOP, color=Color.WHITE)
WN = ChessPiece(piece_type=PieceType.KNIGHT, color=Color.WHITE)
WP = ChessPiece(piece_type=PieceType.PAWN, color=Color.WHITE)


def isOkay(start: tuple, target: tuple, board) -> bool:
    # if the target piece is beyond the bounds of the board:
    if target[0] < 0 or target[0] > 7 or target[1] < 0 or target[1] > 7:
        return False
    # if the start piece is beyond the bounds of the board:
    elif start[0] < 0 or start[0] > 7 or start[1] < 0 or start[1] > 7:
        return False
    # if the target is not empty and contains a piece of the same color
    # as the source, return False:
    elif board[target[0]][target[1]] is not None \
            and board[start[0]][start[1]].color == board[target[0]][target[1]].color:
        return False

    # otherwise, it must be okay:
    return True


class ChessBoard(object):
    def __init__(self):
        self.ChessPiece = namedtuple("ChessPiece", ["piece_type", "color"])
        self.board = [[WR, WN, WB, WQ, WK, WB, WN, WR],
                      [WP, WP, WP, WP, WP, WP, WP, WP],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [BP, BP, BP, BP, BP, BP, BP, BP],
                      [BR, BN, BB, BQ, BK, BB, BN, BR]]

    # @abstractmethod
    def move(self, source: str, target: str) -> None:
        # figure out where the source and target are in the 2d array (returns a tuple of the location- e.g.: 0,0 would be 1a):
        start = whatPosition(source)
        end = whatPosition(target)

        sourcePiece = self.board[start[0]][start[1]]

        # clear the source:
        self.board[start[0]][start[1]] = None

        # replace whatever is in the target with what was in the source:
        self.board[end[0]][end[1]] = sourcePiece

    def reset(self) -> None:
        self.__init__()

    def clear_board(self) -> None:
        self.board = []

        for i in range(8):
            self.board.append([None] * 8)

    def set_piece(self, location: str, piece_type: ChessPiece) -> None:
        file = ord(location[0]) - 97
        rank = int(location[1]) - 1
        self.board[rank][file] = piece_type

    def get_piece(self, cell: str) -> Union[ChessPiece, None]:
        # figure out where the cell is in the 2d array (returns a tuple of the location- e.g.: 0,0 is 1a):
        pos = whatPosition(cell)

        # return whatever is at that location:
        return self.board[pos[0]][pos[1]]

    def possible_moves(self, piece) -> List[Tuple[str, str]]:
        board = self.board
        ans = []

        # get the coordinates of the piece within the 2d array:
        pos = whatPosition(piece)
        row = pos[0]
        col = pos[1]

        # pawn possible moves (changes depending on color):
        if board[row][col] is not None:
            if board[row][col].piece_type == PieceType.PAWN:
                if board[row][col].color == Color.WHITE:
                    # if it's in the second row (i.e. a pawn that hasn't moved yet),
                    # and both spots in front of it are empty and isOkay, add it
                    # to the ans list:
                    if row == 1:
                        x = row + 2
                        end = (x, col)

                        if not board[row + 1][col] and not board[row + 2][col] \
                                and isOkay(pos, end, board):
                            test = str(x)
                            test += str(col)
                            targetPiece = whatPositionReverse(test)

                            ans.append((piece, targetPiece))

                    # it can move diagonally only if there is a black piece in the
                    # target spot:
                    captureDeltas = [(1, 1), (1, -1)]

                    for tup in captureDeltas:
                        x = row + tup[0]
                        y = col + tup[1]
                        target = (x, y)

                        if isOkay(pos, target, board) and self.board[target[0]][target[1]] and \
                                self.board[target[0]][target[1]].color == Color.BLACK:
                            test = str(x)
                            test += str(y)
                            targetPiece = whatPositionReverse(test)

                            ans.append((piece, targetPiece))

                    # otherwise, just check if it can move 1 spot ahead, as normal:
                    x = row + 1
                    target = (x, col)

                    if isOkay(pos, target, board) and \
                            not board[row + 1][col]:
                        test = str(x)
                        test += str(col)
                        targetPiece = whatPositionReverse(test)

                        ans.append((piece, targetPiece))

                elif board[row][col].color == Color.BLACK:
                    # if it's in the second row (i.e. a pawn that hasn't moved yet),
                    # and both spots in front of it are empty and isOkay, add it
                    # to the ans list:
                    if row == 6:
                        x = row - 2
                        end = (x, col)

                        if not board[row - 1][col] and not board[row - 2][col] \
                                and isOkay(pos, end, board):
                            test = str(x)
                            test += str(col)
                            targetPiece = whatPositionReverse(test)

                            ans.append((piece, targetPiece))

                    # it can move diagonally only if there is a white piece in the
                    # target spot:
                    captureDeltas = [(-1, 1), (-1, -1)]

                    for tup in captureDeltas:
                        x = row + tup[0]
                        y = col + tup[1]
                        target = (x, y)

                        if isOkay(pos, target, board) and self.board[target[0]][target[1]] and \
                                self.board[target[0]][target[1]].color == Color.WHITE:
                            test = str(x)
                            test += str(y)
                            targetPiece = whatPositionReverse(test)

                            ans.append((piece, targetPiece))

                    # otherwise, just check if it can move 1 spot ahead, as normal:
                    x = row - 1
                    target = (x, col)

                    if not board[row - 1][col] and \
                            isOkay(pos, target, board):
                        test = str(x)
                        test += str(col)
                        targetPiece = whatPositionReverse(test)

                        ans.append((piece, targetPiece))

            # knight possible moves:
            elif board[row][col].piece_type == PieceType.KNIGHT:
                knightDeltas = [(2, 1), (1, 2), (-1, -2), (-2, -1),
                                (-1, 2), (2, -1), (-2, 1), (1, -2)]

                for tup in knightDeltas:
                    x = row + tup[0]
                    y = col + tup[1]
                    target = (x, y)

                    if isOkay(pos, target, self.board):
                        test = str(x)
                        test += str(y)
                        targetPiece = whatPositionReverse(test)

                        ans.append((piece, targetPiece))

            # bishop possible moves:
            elif board[row][col].piece_type == PieceType.BISHOP:
                bishopDeltas1 = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                                 (6, 6), (7, 7)]
                bishopDeltas2 = [(-1, -1), (-2, -2), (-3, -3), (-4, -4),
                                 (-5, -5), (-6, -6), (-7, -7)]
                bishopDeltas3 = [(1, -1), (2, -2), (3, -3), (4, -4),
                                 (5, -5), (6, -6), (7, -7)]
                bishopDeltas4 = [(-1, 1), (-2, 2), (-3, 3), (-4, 4),
                                 (-5, 5), (-6, 6), (-7, 7)]
                bishopDeltas = [bishopDeltas1, bishopDeltas2, bishopDeltas3, bishopDeltas4]

                for li in bishopDeltas:
                    blocked = False
                    for tup in li:
                        x = row + tup[0]
                        y = col + tup[1]
                        target = (x, y)

                        if not blocked:
                            if isOkay(pos, target, self.board):
                                test = str(x)
                                test += str(y)
                                targetPiece = whatPositionReverse(test)

                                ans.append((piece, targetPiece))
                            elif not isOkay(pos, target, self.board):
                                blocked = True

            # rook possible moves:
            elif board[row][col].piece_type == PieceType.ROOK:
                rookDeltas1 = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                               (6, 0), (7, 0)]
                rookDeltas2 = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                               (0, 6), (0, 7)]
                rookDeltas3 = [(-1, 0), (-2, 0), (-3, 0), (-4, 0),
                               (-5, 0), (-6, 0), (-7, 0)]
                rookDeltas4 = [(0, -1), (0, -2), (0, -3), (0, -4),
                               (0, -5), (0, -6), (0, -7)]

                rookDeltas = [rookDeltas1, rookDeltas2, rookDeltas3, rookDeltas4]

                for li in rookDeltas:
                    blocked = False
                    for tup in li:
                        x = row + tup[0]
                        y = col + tup[1]
                        target = (x, y)

                        if not blocked:
                            if isOkay(pos, target, self.board):
                                test = str(x)
                                test += str(y)
                                targetPiece = whatPositionReverse(test)

                                ans.append((piece, targetPiece))
                            elif not isOkay(pos, target, self.board):
                                blocked = True

            # queen possible moves:
            elif board[row][col].piece_type == PieceType.QUEEN:
                queenDeltas1 = [(1, 1), (2, 2), (3, 3), (4, 4),
                                (5, 5), (6, 6), (7, 7)]
                queenDeltas2 = [(-1, -1), (-2, -2), (-3, -3), (-4, -4),
                                (-5, -5), (-6, -6), (-7, -7)]
                queenDeltas3 = [(1, -1), (2, -2), (3, -3), (4, -4),
                                (5, -5), (6, -6), (7, -7)]
                queenDeltas4 = [(-1, 1), (-2, 2), (-3, 3), (-4, 4),
                                (-5, 5), (-6, 6), (-7, 7)]
                queenDeltas5 = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                                (6, 0), (7, 0)]
                queenDeltas6 = [(0, 1), (0, 2), (0, 3), (0, 4),
                                (0, 5), (0, 6), (0, 7)]
                queenDeltas7 = [(-1, 0), (-2, 0), (-3, 0), (-4, 0),
                                (-5, 0), (-6, 0), (-7, 0)]
                queenDeltas8 = [(0, -1), (0, -2), (0, -3),
                                (0, -4), (0, -5), (0, -6), (0, -7)]

                queenDeltas = [queenDeltas1, queenDeltas2, queenDeltas3,
                               queenDeltas4, queenDeltas5, queenDeltas6,
                               queenDeltas7, queenDeltas8]

                for li in queenDeltas:
                    blocked = False
                    for tup in li:
                        x = row + tup[0]
                        y = col + tup[1]
                        target = (x, y)

                        if not blocked:
                            if isOkay(pos, target, self.board):
                                test = str(x)
                                test += str(y)
                                targetPiece = whatPositionReverse(test)

                                ans.append((piece, targetPiece))
                            elif not isOkay(pos, target, self.board):
                                blocked = True

            # king possible moves:
            elif board[row][col].piece_type == PieceType.KING:
                kingDeltas = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1),
                              (-1, 0), (-1, -1), (0, -1)]

                for tup in kingDeltas:
                    x = row + tup[0]
                    y = col + tup[1]
                    target = (x, y)

                    if isOkay(pos, target, self.board):
                        test = str(x)
                        test += str(y)
                        targetPiece = whatPositionReverse(test)

                        ans.append((piece, targetPiece))

            return ans

    def eval_pieces(self, side="white"):
        sides = ["white", "black"]
        if side not in sides:
            raise ValueError("Invalid side. It must be white or black.")

        wScore = 0
        bScore = 0
        board = self.board

        # if board[row][col].piece_type == PieceType.PAWN
        for r in range(8):
            for c in range(8):
                if board[r][c]:
                    piece = board[r][c]
                    if side == "white" and piece.color == Color.WHITE:
                        if piece.piece_type == PieceType.PAWN:
                            wScore += 1
                        elif piece.piece_type == PieceType.BISHOP:
                            wScore += 3
                        elif piece.piece_type == PieceType.KNIGHT:
                            wScore += 3.5
                        elif piece.piece_type == PieceType.ROOK:
                            wScore += 5
                        elif piece.piece_type == PieceType.QUEEN:
                            wScore += 9
                        elif piece.piece_type == PieceType.KING:
                            wScore += 1000
                    elif side == "black" and piece.color == Color.BLACK:
                        if piece.piece_type == PieceType.PAWN:
                            bScore += 1
                        elif piece.piece_type == PieceType.BISHOP:
                            bScore += 3
                        elif piece.piece_type == PieceType.KNIGHT:
                            bScore += 3.5
                        elif piece.piece_type == PieceType.ROOK:
                            bScore += 5
                        elif piece.piece_type == PieceType.QUEEN:
                            bScore += 9
                        elif piece.piece_type == PieceType.KING:
                            bScore += 1000
        if side == "white":
            return wScore - bScore
        elif side == "black":
            return bScore - wScore

    def eval_coverage(self, side="white"):
        sides = ["white", "black"]
        if side not in sides:
            raise ValueError("Invalid side. It must be white or black.")

        wLen = 0
        bLen = 0
        board = self.board

        for r in range(8):
            for c in range(8):
                if board[r][c]:
                    piece = board[r][c]
                    test = str(r) + str(c)
                    pos = whatPositionReverse(test)

                    if piece.color == Color.WHITE:
                        wLen += len(self.possible_moves(pos))
                    elif piece.color == Color.BLACK:
                        bLen += len(self.possible_moves(pos))

        if side == "black":
            return bLen - wLen
        elif side == "white":
            return wLen - bLen

    def select_move(self, side="white") -> Tuple:
        ans = ("", "")
        coverage = 0
        diffList = []

        blackPointList = []
        whitePointList = []

        board = self.board
        sides = ["white", "black"]
        if side not in sides:
            raise ValueError("Invalid side. It must be white or black.")

        for r in range(8):
            for c in range(8):
                if side == "white" and board[r][c] is not None \
                        and board[r][c].color == Color.WHITE:
                    # get the possible moves for that piece:
                    test = str(r) + str(c)
                    pos = whatPositionReverse(test)
                    moves = self.possible_moves(pos)

                    if moves:
                        for m in moves:
                            # Store the target for later:
                            targetPos = whatPosition(m[1])
                            temp = self.board[targetPos[0]][targetPos[1]]

                            # do the move:
                            self.move(m[0], m[1])
                            whiteCoverage = self.eval_coverage("white")

                            # if better coverage will result, add it to the possible moves list:
                            if coverage < abs(whiteCoverage):
                                coverage = whiteCoverage
                                tup = (m[0], m[1])
                                diffList.append(tup)

                            # move the piece back:
                            self.move(m[1], m[0])

                            # put the target piece back:
                            self.set_piece(m[1], temp)

                        # diffList now has all the moves with the best coverage. go through them
                        # and find which move results in the smallest amount of points for the
                        # opposing team:
                        for diff in diffList:
                            # Store the target for later:
                            targetPos = whatPosition(diff[1])
                            temp = self.board[targetPos[0]][targetPos[1]]

                            # do the move:
                            self.move(diff[0], diff[1])

                            # calculate how many points black would have and
                            # append it to a list:
                            blackPointsNew = self.eval_pieces("black")
                            blackPointList.append(blackPointsNew)

                            # move the piece back:
                            self.move(diff[1], diff[0])

                            # put the target piece back:
                            self.set_piece(diff[1], temp)

                        # get the index of the smallest possible amount of points for
                        # black and then find the corresponding move in the diffList:
                        minIndex = blackPointList.index(min(blackPointList))
                        ans = diffList[minIndex]

                elif side == "black" and board[r][c] is not None \
                        and board[r][c].color == Color.BLACK:
                    # get the possible moves for that piece:
                    test = str(r) + str(c)
                    pos = whatPositionReverse(test)
                    moves = self.possible_moves(pos)

                    if moves:
                        for m in moves:
                            # Store the target for later:
                            targetPos = whatPosition(m[1])
                            temp = self.board[targetPos[0]][targetPos[1]]

                            # do the move:
                            self.move(m[0], m[1])
                            blackCoverage = self.eval_coverage("black")

                            if coverage < abs(blackCoverage):
                                coverage = blackCoverage
                                tup = (m[0], m[1])
                                diffList.append(tup)

                            # move the piece back
                            self.move(m[1], m[0])

                            # put the target piece back:
                            self.set_piece(m[1], temp)

                        for diff in diffList:
                            # Store the target for later:
                            targetPos = whatPosition(diff[1])
                            temp = self.board[targetPos[0]][targetPos[1]]

                            # do the move:
                            self.move(diff[0], diff[1])

                            # calculate how many points white would have and append it
                            # to a list:
                            whitePointsNew = self.eval_pieces("white")
                            whitePointList.append(whitePointsNew)

                            # move the piece back:
                            self.move(diff[1], diff[0])

                            # put the target piece back:
                            self.set_piece(diff[1], temp)

                    # get the index of the smallest possible amount of points for
                    # white and then find the corresponding move in the diffList:
                    minIndex = whitePointList.index(min(whitePointList))
                    ans = diffList[minIndex]

        # return the move with maximum resultant board
        return ans


# tests:
class TestBoard(unittest.TestCase):
    def test_setup(self):
        b = ChessBoard()
        self.assertEqual(b.get_piece("b2"), WP)
        self.assertEqual(b.get_piece("a7"), BP)

    def test_move(self):
        b = ChessBoard()

        # moving whatever is in b2 to b4:
        b.move("b2", "b4")

        # checking if the source was properly cleared:
        self.assertEqual(b.get_piece("b2"), None)

        # checking if the piece was actually moved:
        self.assertEqual(b.get_piece("b4"), WP)

    # testing the possible_moves method:
    def test_whitePawnCanMove(self):
        # try putting just white pawn in place
        b = ChessBoard()
        b.clear_board()
        b.set_piece("b2", WP)
        moves = b.possible_moves("b2")
        self.assertCountEqual(moves, [('b2', 'b3'), ('b2', 'b4')])

        b = ChessBoard()
        b.clear_board()
        # try putting white pawn in place, blocking white piece two in front
        b.set_piece("b2", WP)
        b.set_piece("b4", BP)
        moves = b.possible_moves("b2")
        # for the pawn, want to be sure that cannot move two ahead, just one ahead
        self.assertCountEqual(moves, [('b2', 'b3')])

    def test_whitePawnCannotMove(self):
        b = ChessBoard()
        b.clear_board()
        # try putting white pawn in place, blocking white piece in front
        # dummy pieces cannot move, just there for testing blocking
        b.set_piece("b2", WP)
        b.set_piece("b3", WP)
        moves = b.possible_moves("b2")
        # for the pawn, want to be sure that cannot move
        self.assertCountEqual(moves, [])

    def test_whitePawnCapture(self):
        b = ChessBoard()
        b.clear_board()
        # try putting white pawn in place, black piece on diagonal
        b.set_piece("b2", WP)
        b.set_piece("b3", BP)
        b.set_piece("c3", BP)
        moves = b.possible_moves("b2")
        # for the pawn, want to be sure that can take off piece
        self.assertCountEqual(moves, [('b2', 'c3')])

    def test_blackPawnCanMove(self):
        # try putting just black pawn in place
        b = ChessBoard()
        b.clear_board()
        b.set_piece("g7", BP)
        moves = b.possible_moves("g7")
        self.assertCountEqual(moves, [('g7', 'g6'), ('g7', 'g5')])

        b = ChessBoard()
        b.clear_board()
        # try putting black pawn in place, blocking the black piece two in front
        b.set_piece("g7", BP)
        b.set_piece("g5", WP)
        moves = b.possible_moves("g7")
        # for the pawn, want to be sure that cannot move two ahead, just one ahead
        self.assertCountEqual(moves, [('g7', 'g6')])

    #
    def test_blackPawnCannotMove(self):
        b = ChessBoard()
        b.clear_board()
        # try putting white pawn in place, blocking white piece in front
        # dummy pieces cannot move, just there for testing blocking
        b.set_piece("g7", BP)
        b.set_piece("g6", BP)
        moves = b.possible_moves("g7")
        # for the pawn, want to be sure that cannot move
        self.assertCountEqual(moves, [])

    def test_blackPawnCapture(self):
        b = ChessBoard()
        b.clear_board()
        # try putting black pawn in place, white piece on diagonal
        b.set_piece("g7", BP)
        b.set_piece("g6", WP)
        b.set_piece("h6", WP)
        moves = b.possible_moves("g7")
        # for the pawn, want to be sure that can take off piece
        self.assertCountEqual(moves, [('g7', 'h6')])

    def test_knightCanMoveSimple(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("e4", WN)

        moves = b.possible_moves("e4")
        li = [('e4', 'f6'), ('e4', 'g5'), ('e4', 'c3'),
              ('e4', 'd2'), ('e4', 'g3'), ('e4', 'd6'),
              ('e4', 'f2'), ('e4', 'c5')]
        self.assertCountEqual(moves, li)

    def test_knightCanMoveComplex(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("d3", WN)

        # putting pieces in all but one of the places it can go + some
        # other randomly selected places:
        b.set_piece("e5", WP)
        b.set_piece("d4", WP)
        b.set_piece("f3", WP)
        b.set_piece("f4", WK)
        b.set_piece("b2", WR)
        b.set_piece("c1", WP)
        b.set_piece("f2", WP)
        b.set_piece("c5", WP)
        b.set_piece("e1", WR)

        moves = b.possible_moves("d3")
        self.assertCountEqual(moves, [('d3', 'b4')])

    def test_knightCannotMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("d3", WN)

        # blocking all the paths for that knight:
        b.set_piece("e5", WP)
        b.set_piece("d4", WP)
        b.set_piece("f3", WP)
        b.set_piece("f4", WK)
        b.set_piece("b2", WR)
        b.set_piece("c1", WP)
        b.set_piece("f2", WP)
        b.set_piece("c5", WP)
        b.set_piece("e1", WR)
        b.set_piece("b4", WQ)

        moves = b.possible_moves("d3")
        self.assertCountEqual(moves, [])

    def test_bishopCanMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("d5", WB)

        moves = b.possible_moves("d5")
        li = [('d5', 'e6'), ('d5', 'f7'), ('d5', 'g8'),
              ('d5', 'c4'), ('d5', 'b3'), ('d5', 'a2'),
              ('d5', 'c6'), ('d5', 'b7'), ('d5', 'a8'),
              ('d5', 'e4'), ('d5', 'f3'), ('d5', 'g2'),
              ('d5', 'h1')]
        self.assertCountEqual(moves, li)

    def test_bishopCannotMove(self):
        b = ChessBoard()
        b.clear_board()

        # block all paths for that bishop:
        b.set_piece("d5", WB)
        b.set_piece("e4", WP)
        b.set_piece("c4", WP)
        b.set_piece("c6", WP)
        b.set_piece("e6", WP)

        moves = b.possible_moves("d5")
        self.assertCountEqual(moves, [])

    def test_rookCanMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("d5", BR)

        moves = b.possible_moves("d5")
        li = [('d5', 'd6'), ('d5', 'd7'), ('d5', 'd8'),
              ('d5', 'e5'), ('d5', 'f5'), ('d5', 'g5'),
              ('d5', 'h5'), ('d5', 'd4'), ('d5', 'd3'),
              ('d5', 'd2'), ('d5', 'd1'), ('d5', 'c5'),
              ('d5', 'b5'), ('d5', 'a5')]

        self.assertCountEqual(moves, li)

    def test_rookCannotMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("d5", BR)

        # blocking all paths for that rook:
        b.set_piece("e5", BP)
        b.set_piece("d4", BP)
        b.set_piece("d6", BP)
        b.set_piece("c5", BP)

        moves = b.possible_moves("d5")
        self.assertCountEqual(moves, [])

    def test_queenCanMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("b5", BQ)

        moves = b.possible_moves("b5")
        li = [('b5', 'c6'), ('b5', 'd7'), ('b5', 'e8'),
              ('b5', 'a4'), ('b5', 'a6'), ('b5', 'c4'),
              ('b5', 'd3'), ('b5', 'e2'), ('b5', 'f1'),
              ('b5', 'b6'), ('b5', 'b7'), ('b5', 'b8'),
              ('b5', 'c5'), ('b5', 'd5'), ('b5', 'e5'),
              ('b5', 'f5'), ('b5', 'g5'), ('b5', 'h5'),
              ('b5', 'b4'), ('b5', 'b3'), ('b5', 'b2'),
              ('b5', 'b1'), ('b5', 'a5')]

        self.assertCountEqual(moves, li)

    def test_queenCannotMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("b5", BQ)

        # blocking all the paths for that queen:
        b.set_piece("a4", BP)
        b.set_piece("b4", BN)
        b.set_piece("c4", BR)
        b.set_piece("c5", BQ)
        b.set_piece("c6", BR)
        b.set_piece("b6", BP)
        b.set_piece("a6", BP)
        b.set_piece("a5", BP)

        moves = b.possible_moves("b5")
        self.assertCountEqual(moves, [])

    def test_kingCanMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("f4", WK)

        moves = b.possible_moves("f4")
        li = [('f4', 'e5'), ('f4', 'f5'), ('f4', 'g5'),
              ('f4', 'g4'), ('f4', 'g3'), ('f4', 'f3'),
              ('f4', 'e3'), ('f4', 'e4')]

        self.assertCountEqual(moves, li)

    def test_kingCannotMove(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("f4", BK)

        # blocking all paths for that king:
        b.set_piece("e4", BP)
        b.set_piece("e5", BQ)
        b.set_piece("f5", BN)
        b.set_piece("g5", BP)
        b.set_piece("g4", BP)
        b.set_piece("g3", BP)
        b.set_piece("f3", BN)
        b.set_piece("e3", BR)

        moves = b.possible_moves("f4")
        self.assertCountEqual(moves, [])

    def test_evalPieces(self):
        b = ChessBoard()

        whiteScore = b.eval_pieces("white")
        blackScore = b.eval_pieces("black")
        # for a regular setup, should be: 1040.0 each
        # so the difference between them will be 0.0
        # tup = (1040.0, 1040.0)
        self.assertEqual(whiteScore - blackScore, 0.0)

    def test_evalPiecesBlackWinning(self):
        b = ChessBoard()
        b.clear_board()

        # white: 6
        b.set_piece("a2", WP)
        b.set_piece("a5", WR)

        # black: 11
        b.set_piece("b5", BP)
        b.set_piece("e7", BP)
        b.set_piece("h4", BQ)

        whiteScore = b.eval_pieces("white")
        blackScore = b.eval_pieces("black")
        # white's score should be 6, and black's score should be 11:
        self.assertEqual((blackScore, whiteScore), (11, 6))

    def test_evalPiecesWhiteWinning(self):
        b = ChessBoard()
        b.clear_board()

        # black: 6
        b.set_piece("a2", BP)
        b.set_piece("a5", BR)

        # white: 11
        b.set_piece("b5", WP)
        b.set_piece("e7", WP)
        b.set_piece("h4", WQ)

        whiteScore = b.eval_pieces("white")
        blackScore = b.eval_pieces("black")

        self.assertEqual((whiteScore, blackScore), (11, 6))

    def test_evalCoverageSimple(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("c7", BP)  # 2
        b.set_piece("f4", WK)  # 8
        moves1 = b.possible_moves("c7")
        moves2 = b.possible_moves("f4")
        test = len(moves1) - len(moves2)

        coverage = b.eval_coverage("black")
        self.assertEqual(coverage, test)

    def test_evalCoverageStartingWhite(self):
        # evaluate white's coverage at the beginning of the game:
        b = ChessBoard()
        b.clear_board()

        b.set_piece("a1", WR)
        b.set_piece("b1", WN)
        b.set_piece("c1", WB)
        b.set_piece("d1", WQ)
        b.set_piece("e1", WK)
        b.set_piece("f1", WB)
        b.set_piece("g1", WN)
        b.set_piece("h1", WR)

        b.set_piece("a2", WP)
        b.set_piece("b2", WP)
        b.set_piece("c2", WP)
        b.set_piece("d2", WP)
        b.set_piece("e2", WP)
        b.set_piece("f2", WP)
        b.set_piece("g2", WP)
        b.set_piece("h2", WP)

        # list of all possible moves for white:
        allPossibleMoves = [('a2', 'a4'), ('a2', 'a3'), ('b2', 'b4'),
                            ('b2', 'b3'), ('c2', 'c4'), ('c2', 'c3'),
                            ('d2', 'd4'), ('d2', 'd3'), ('e2', 'e4'),
                            ('e2', 'e3'), ('f2', 'f4'), ('f2', 'f3'),
                            ('g2', 'g4'), ('g2', 'g3'), ('h2', 'h4'),
                            ('h2', 'h3'), ('g1', 'h3'), ('g1', 'f3'),
                            ('b1', 'c3'), ('b1', 'a3')]

        coverage = b.eval_coverage("white")

        self.assertEqual(coverage, len(allPossibleMoves))

    def test_evalCoverageStartingBlack(self):
        # evaluate white's coverage at the beginning of the game:
        b = ChessBoard()
        b.clear_board()

        b.set_piece("a7", BP)
        b.set_piece("b7", BP)
        b.set_piece("c7", BP)
        b.set_piece("d7", BP)
        b.set_piece("e7", BP)
        b.set_piece("f7", BP)
        b.set_piece("g7", BP)
        b.set_piece("h7", BP)

        b.set_piece("a8", BR)
        b.set_piece("b8", BN)
        b.set_piece("c8", BB)
        b.set_piece("d8", BQ)
        b.set_piece("e8", BK)
        b.set_piece("f8", BB)
        b.set_piece("g8", BN)
        b.set_piece("h8", BR)

        # list of all possible moves for black
        allPossibleMoves = [('a7', 'a5'), ('a7', 'a6'), ('b7', 'b5'),
                            ('b7', 'b6'), ('c7', 'c5'), ('c7', 'c6'),
                            ('d7', 'd5'), ('d7', 'd6'), ('e7', 'e5'),
                            ('e7', 'e6'), ('f7', 'f5'), ('f7', 'f6'),
                            ('g7', 'g5'), ('g7', 'g6'), ('h7', 'h5'),
                            ('h7', 'h6'), ('b8', 'a6'), ('b8', 'c6'),
                            ('g8', 'f6'), ('g8', 'h6')]

        coverage = b.eval_coverage("black")
        self.assertEqual(coverage, len(allPossibleMoves))

    def test_evalCoverageStarting(self):
        b = ChessBoard()

        bCoverage = b.eval_coverage("black")
        wCoverage = b.eval_coverage("white")

        # at the beginning, black and white have equal coverage,
        # so bCoverage and wCoverage should both be 0:
        self.assertEqual(bCoverage, wCoverage)
        self.assertEqual(bCoverage, 0)
        self.assertEqual(wCoverage, 0)

    def test_selectMoveWhiteSimple(self):
        b = ChessBoard()
        b.clear_board()
        b.set_piece("b2", WP)

        moves = b.possible_moves("b2")
        select = b.select_move("white")
        self.assertIn(select, moves)

    def test_selectMoveBlackSimple(self):
        b = ChessBoard()
        b.clear_board()
        b.set_piece("c7", BP)

        moves = b.possible_moves("c7")
        select = b.select_move("black")
        self.assertIn(select, moves)

    def test_selectMoveWhiteStarting(self):
        b = ChessBoard()

        allPossibleMoves = [('a2', 'a4'), ('a2', 'a3'), ('b2', 'b4'),
                            ('b2', 'b3'), ('c2', 'c4'), ('c2', 'c3'),
                            ('d2', 'd4'), ('d2', 'd3'), ('e2', 'e4'),
                            ('e2', 'e3'), ('f2', 'f4'), ('f2', 'f3'),
                            ('g2', 'g4'), ('g2', 'g3'), ('h2', 'h4'),
                            ('h2', 'h3'), ('g1', 'h3'), ('g1', 'f3'),
                            ('b1', 'c3'), ('b1', 'a3')]

        select = b.select_move("white")
        self.assertIn(select, allPossibleMoves)

    def test_selectMoveCapture(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("g7", BP)
        b.set_piece("h6", WP)
        moves = b.possible_moves("g7")

        select = b.select_move("black")

        # assert that it's a valid move:
        self.assertIn(select, moves)

        # it should select the move that takes the other team's piece and reduces their coverage:
        self.assertEqual(select, ('g7', 'h6'))

    # if there are multiple moves that maximize the coverage,
    # test that it chooses the one that reduces the other
    # team's points:
    def test_selectMoveWhiteMultipleOptions(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("c3", WP)
        b.set_piece("d4", BN)
        b.set_piece("b4", BR)

        moves = b.possible_moves("c3")
        select = b.select_move("white")

        self.assertIn(select, moves)
        # it should select b4, because black losing a rook is
        # worse than losing a knight (in terms of points):
        self.assertEqual(select, ('c3', 'b4'))

    # if there are multiple moves that maximize the coverage,
    # test that it chooses the one that reduces the other
    # team's points:
    def test_selectMoveBlackMultipleOptions(self):
        b = ChessBoard()
        b.clear_board()

        b.set_piece("e6", BP)
        b.set_piece("f5", WN)
        b.set_piece("d5", WR)

        moves = b.possible_moves("e6")
        select = b.select_move("black")

        self.assertIn(select, moves)
        # it should select d5, because white losing a rook is
        # worse than losing a knight (in terms of points):
        self.assertEqual(select, ('e6', 'd5'))


if __name__ == "__main__":
    unittest.main()
