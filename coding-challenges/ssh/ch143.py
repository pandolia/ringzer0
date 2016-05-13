'''
> python ch143.py
============================================================
Ringzer ssh challenge solver
    <https://ringzer0team.com/challenges/143>
============================================================
[+] Geting ssh server info from web page... Done.
    hostname=ringzer0team.com, port=12643
    username=sudoku, password=dg43zz6R0E
[+] Login to ssh server... Done
[+] Start challenging
    Got sudoku board:
    +---+---+---+---+---+---+---+---+---+
    |   | 3 | 4 | 8 | 7 |   |   |   | 1 |
    +---+---+---+---+---+---+---+---+---+
    |   |   | 9 |   |   |   | 5 |   | 4 |
    +---+---+---+---+---+---+---+---+---+
    | 2 | 6 |   | 5 |   | 4 | 8 |   |   |
    +---+---+---+---+---+---+---+---+---+
    | 3 |   |   |   |   | 2 | 6 | 1 | 5 |
    +---+---+---+---+---+---+---+---+---+
    | 7 | 9 | 2 | 6 |   | 5 |   |   | 8 |
    +---+---+---+---+---+---+---+---+---+
    |   |   | 5 |   | 4 |   |   |   | 2 |
    +---+---+---+---+---+---+---+---+---+
    | 4 | 8 | 7 | 9 | 2 | 6 |   | 5 |   |
    +---+---+---+---+---+---+---+---+---+
    | 9 |   | 6 |   | 5 | 3 | 4 |   | 7 |
    +---+---+---+---+---+---+---+---+---+
    | 1 | 5 | 3 |   | 8 | 7 |   | 2 | 6 |
    +---+---+---+---+---+---+---+---+---+
    Solved sudoku board:
    +---+---+---+---+---+---+---+---+---+
    | 5 | 3 | 4 | 8 | 7 | 9 | 2 | 6 | 1 |
    +---+---+---+---+---+---+---+---+---+
    | 8 | 7 | 9 | 2 | 6 | 1 | 5 | 3 | 4 |
    +---+---+---+---+---+---+---+---+---+
    | 2 | 6 | 1 | 5 | 3 | 4 | 8 | 7 | 9 |
    +---+---+---+---+---+---+---+---+---+
    | 3 | 4 | 8 | 7 | 9 | 2 | 6 | 1 | 5 |
    +---+---+---+---+---+---+---+---+---+
    | 7 | 9 | 2 | 6 | 1 | 5 | 3 | 4 | 8 |
    +---+---+---+---+---+---+---+---+---+
    | 6 | 1 | 5 | 3 | 4 | 8 | 7 | 9 | 2 |
    +---+---+---+---+---+---+---+---+---+
    | 4 | 8 | 7 | 9 | 2 | 6 | 1 | 5 | 3 |
    +---+---+---+---+---+---+---+---+---+
    | 9 | 2 | 6 | 1 | 5 | 3 | 4 | 8 | 7 |
    +---+---+---+---+---+---+---+---+---+
    | 1 | 5 | 3 | 4 | 8 | 7 | 9 | 2 | 6 |
    +---+---+---+---+---+---+---+---+---+
[+] Challenge done, result is:
    5,3,4,8,7,9,2,6,1,8,7,9,2,6,...
Great! FLAG-???

    Challenge success!!!
[+] Submitting the flag... Done
============================================================
'''

from ringzerSSH import SshChallenge

UNKNOWN = ' '
NUMSTR  = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

class LeetSolution:    
    def solve(self, board, rows_avb, cols_avb, sqrs_avb, row, col):
        if row == 8 and col == 9:
            return True
        
        if col == 9:
            row, col = row + 1, 0

        if board[row][col] != UNKNOWN:
            return self.solve(board, rows_avb, cols_avb, sqrs_avb, row, col + 1)
        
        sqr = (0 if row < 3 else 3 if row < 6 else 6) \
               + (0 if col < 3 else 1 if col < 6 else 2)

        available = rows_avb[row] & cols_avb[col] & sqrs_avb[sqr]
        trynum = 0
        while available:
            if available & 1:
                cellBitmask = 1 << trynum
                rows_avb[row] ^= cellBitmask
                cols_avb[col] ^= cellBitmask
                sqrs_avb[sqr] ^= cellBitmask
                
                if self.solve(board, rows_avb, cols_avb, sqrs_avb, row, col + 1):
                    board[row][col] = NUMSTR[trynum]
                    return True
                    
                rows_avb[row] |= cellBitmask
                cols_avb[col] |= cellBitmask
                sqrs_avb[sqr] |= cellBitmask
                
            available >>= 1
            trynum += 1
        
        return False
        
    # @param board, a 9x9 2D array
    # Solve the Sudoku by modifying the input board in-place.
    # Do not return any value.
    def solveSudoku(self, board):
        allAvailable = 0b111111111
        rows_avb = [allAvailable] * 9
        cols_avb = [allAvailable] * 9
        sqrs_avb = [allAvailable] * 9
        
        for row in range(9):
            sqrRow = (0 if row < 3 else 3 if row < 6 else 6)
            for col in range(9):
                if board[row][col] != UNKNOWN:                                        
                    sqr = sqrRow + (0 if col < 3 else 1 if col < 6 else 2)
                    cellBitmask = 1 << (ord(board[row][col]) - ord('1'))
                    rows_avb[row] ^= cellBitmask
                    cols_avb[col] ^= cellBitmask
                    sqrs_avb[sqr] ^= cellBitmask
        
        self.solve(board, rows_avb, cols_avb, sqrs_avb, 0, 0)

def toString(board):
    Row = ['| ' + ' | '.join(row) + ' |' for row in board]
    return '    +---+---+---+---+---+---+---+---+---+\n    ' + \
           '\n    +---+---+---+---+---+---+---+---+---+\n    '.join(Row) + \
           '\n    +---+---+---+---+---+---+---+---+---+'
  

def chall_func(firstmessage):
    info = firstmessage.split('\r\n')
    board = [[info[i][j] for j in range(2, 35, 4)] for i in range(6,23,2)]
    print '    Got sudoku board:\n%s' % toString(board)
    LeetSolution().solveSudoku(board)
    print '    Solved sudoku board:\n%s' % toString(board)
    return ','.join(','.join(row) for row in board)

SshChallenge(143, chall_func, firstexpect='Solution:')
