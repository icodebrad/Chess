"""
This class is responsible for storing all the information about the current state of a chess game. It will also be responsible for
determining the valid moves at the current state. It will also keep a move log.
"""

class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list  has 2 characters
        #the first character represents the color of the piece (black/white)
        #the second character represents the type of piece (R = Rook, N = Knight, B = Bishop etc.)
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        # dictionary for assigning the appropriate move functions for each piece
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
    '''
    Takes a move as a parameter and executes it (This will not work for castling, en passant and pawn promotion)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Log the move to undo later and show history
        self.whiteToMove = not self.whiteToMove #swap players from white to black

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #swap players

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() #not worrying about checks for now

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #calls the appropriate move function based on piece
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    row +/- 1 = move forward or back, col +/- 1 = move to the left or right
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r, c),(r-1, c), self.board))

                if r == 6 and self.board[r-2][c] == "--": #2 square white pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))

            if c-1 >= 0: # captures to the left
                if self.board[r-1][c-1][0] == "b": #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))

            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == "b": #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else: #black pawn moves
            if self.board[r+1][c] == "--":  # 1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))

                if r == 1 and self.board[r+2][c] == "--":  # 2 square black pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board))

            if c-1 >= 0:  # captures to the left
                if self.board[r+1][c-1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))

            if c+1 <= 7:  # captures to the right
                if self.board[r+1][c+1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
        #add pawn promotions later

    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #(up, left, down, right) all possible move directions of the rook
        enemyColor = 'b' if self.whiteToMove else 'w' #determines the enemy color of white/black pieces using if statement within a variable
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break
    '''
    Get all the knight moves for the knight located at row, col and add these moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (2, -1), (2, 1), (1, 2))
        allyColor = 'w' if self.whiteToMove else 'b'
        for n in knightMoves:
            endRow = r + n[0]
            endCol = c + n[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece or empty space
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        bishopMoves = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for b in bishopMoves:
            for i in range(1,8):
                endRow = r + b[0] * i
                endCol = c + b[1] * i
                if 0 <= endRow < 8 and 0 <= endCol <8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':    # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:     # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:   # ally piece invalid
                        break
                else:   # off board
                    break
    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        queenMoves = ((-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for q in queenMoves:
            for i in range(1,8):
                endRow = r + q[0] * i
                endCol = c + q[1] * i
                if 0 <= endRow < 8 and 0 <= endCol <8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':    # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:     # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:   # ally piece invalid
                        break
                else:   # off board
                    break

    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        pass
class Move():
    # this class maps the keys to values
    # key : value (k = key, v = value)
    # a row is a rank in chess, and a column is a file. the first rank starts all the way from the right (last pos) whilst the files start from the left (first pos) ranks start from numbers 1-8 and files start from letters A-H.
    # in reversing library notation: (v: k for k, v in _.items())
    # basically how it works is that for each of the key and values in the .items() of ranksToRows for example; it reverses it and says each key and value make a value and key pair.
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0,}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7,}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol #generates a unique move id
        print(self.moveID)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

#In chess notation you do File + Rank e.g. (A1, E4, G8)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
