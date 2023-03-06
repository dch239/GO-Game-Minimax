from audioop import minmax
from copy import deepcopy
import random
import sys
from time import sleep
from read import readInput
from write import writeOutput
import pdb

from host import GO

class RandomPlayer():
    def __init__(self, board, piece_type):
        self.type = 'random'
        self.komi = 5/2 # Komi rule
        self.previous_board = deepcopy(board)
        self.board = board
        self.piece_type = piece_type
        if piece_type == 1:
            self.opponent_piece_type = 2
        else:
            self.opponent_piece_type = 1
        self.n_move = 0
        self.size = 5
        self.max_move = 5 * 5 - 1
        self.verbose = False

        #needed to for valid_check_place
        self.died_pieces = []

    # def score(self, piece_type):
    #     '''
    #     Get score of a player by counting the number of stones.

    #     :param piece_type: 1('X') or 2('O').
    #     :return: boolean indicating whether the game should end.
    #     '''
    #     board = self.board
    #     cnt = 0
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             if board[i][j] == piece_type:
    #                 cnt += 1
    #     return cnt 

    def compare_board(self, board1, board2):
        for i in range(self.size):
            for j in range(self.size):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    # def game_end(self, piece_type, action="MOVE"):
    #     '''
    #     Check if the game should end.

    #     :param piece_type: 1('X') or 2('O').
    #     :param action: "MOVE" or "PASS".
    #     :return: boolean indicating whether the game should end.
    #     '''
    #     # Case 1: max move reached
    #     if self.n_move >= self.max_move:
    #         return True
    #     # Case 2: two players all pass the move.
    #     if self.compare_board(self.previous_board, self.board) and action == "PASS":
    #         return True
    #     return False

    # def judge_winner(self):
    #     '''
    #     Judge the winner of the game by number of pieces for each player.

    #     :param: None.
    #     :return: piece type of winner of the game (0 if it's a tie).
    #     '''        
    #     cnt_1 = self.score(1)
    #     cnt_2 = self.score(2)
    #     if cnt_1 > cnt_2 + self.komi: return 1
    #     elif cnt_1 < cnt_2 + self.komi: return 2
    #     else: return 0

    #needed for valid_place_check
    def copy_board(self):
        '''
        Copy the current board for potential testing.

        :param: None.
        :return: the copied board instance.
        '''
        return deepcopy(self)

    #needed for valid_place_check
    def update_board(self, new_board):
        '''
        Update the board with new_board

        :param new_board: new board.
        :return: None.
        '''   
        self.board = new_board

    #needed for detect_neighbor_ally
    def detect_neighbor(self, i, j):
        '''
        Detect all the neighbors of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbors row and column (row, column) of position (i, j).
        '''
        board = self.board
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors


    #needed for ally_dfs
    def detect_neighbor_ally(self, i, j):
        '''
        Detect the neighbor allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
        '''
        board = self.board
        neighbors = self.detect_neighbor(i, j)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies


    #needed for find_liberty
    def ally_dfs(self, i, j):
        '''
        Using DFS to search for all allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the all allies row and column (row, column) of position (i, j).
        '''
        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members


    #needed for valid_place_check
    def find_liberty(self, i, j):
        '''
        Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: boolean indicating whether the given stone still has liberty.
        '''
        board = self.board
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return False

    def find_died_pieces(self, piece_type):
        '''
        Find the died stones that has no liberty in the board for a given piece type.

        :param piece_type: 1('X') or 2('O').
        :return: a list containing the dead pieces row and column(row, column).
        '''
        board = self.board
        died_pieces = []

        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty(i, j):
                        died_pieces.append((i,j))
        return died_pieces


    def remove_certain_pieces(self, positions):
        '''
        Remove the stones of certain locations.

        :param positions: a list containing the pieces to be removed row and column(row, column)
        :return: None.
        '''
        board = self.board
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        self.update_board(board)


    def remove_died_pieces(self, piece_type):
        '''
        Remove the dead stones in the board.

        :param piece_type: 1('X') or 2('O').
        :return: locations of dead pieces.
        '''

        died_pieces = self.find_died_pieces(piece_type)
        if not died_pieces: return []
        self.remove_certain_pieces(died_pieces)
        return died_pieces



    def valid_place_check(self, i, j, piece_type, test_check=False):
        '''
        Check whether a placement is valid.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1(white piece) or 2(black piece).
        :param test_check: boolean if it's a test check.
        :return: boolean indicating whether the placement is valid.
        '''   
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False

        # Check if the place is in the board range
        if not (i >= 0 and i < len(board)):
            if verbose:
                print(('Invalid placement. row should be in the range 1 to {}.').format(len(board) - 1))
            return False
        if not (j >= 0 and j < len(board)):
            if verbose:
                print(('Invalid placement. column should be in the range 1 to {}.').format(len(board) - 1))
            return False
        
        # Check if the place already has a piece
        if board[i][j] != 0:
            if verbose:
                print('Invalid placement. There is already a chess in this position.')
            return False
        
        # Copy the board for testing
        test_go = self.copy_board()
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go.update_board(test_board)
        if test_go.find_liberty(i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            if verbose:
                print('Invalid placement. No liberty found in this position.')
            return False

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                if verbose:
                    print('Invalid placement. A repeat move not permitted by the KO rule.')
                return False
        return True
 
    
    def evaluation(self, piece_type):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == piece_type:
                    score+=1
                else:
                    score-=1
        return score


    def minimax(self, depth, isMaximizing):
        #need to check terminal condition
        if depth == 5:
            return self.evaluation(self.board)
        
        if isMaximizing:
            bestScore = -float("inf")
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == 0 and self.valid_place_check(i,j,self.piece_type): #also check legal move
                        self.board[i][j] = self.piece_type
                        score = minmax(self.board, depth+1, False)
                        self.board[i][j] = 0
                        bestScore = max(score, bestScore)
            return bestScore
        
        else:
            bestScore = float("inf")
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == 0 and self.valid_place_check(i,j,self.opponent_piece_type): #also check legal move
                        self.board[i][j] = self.opponent_piece_type
                        score = self.minimax(self.board, depth+1, True)
                        self.board[i][j] = 0
                        bestScore = min(score, bestScore)
            return bestScore

        #result = self.judge_winner()
        



    def get_input(self, go, piece_type):
        '''
        Get one input.
        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))
                
        #minimax here
        
        #
        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer(board=board, piece_type=piece_type)
    action = player.get_input(go, piece_type)
    writeOutput(action)