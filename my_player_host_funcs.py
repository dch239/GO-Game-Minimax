from copy import deepcopy
import random
import sys
from tabnanny import verbose
from read import readInput
from write import writeOutput

from host import GO

class RandomPlayer():
    def __init__(self, piece_type):
        self.type = 'random'
        self.piece_type = piece_type
        if piece_type == 1:
            self.opponent_piece_type = 2
        else:
            self.opponent_piece_type = 1
        self.verbose = False

    def detect_neighbor(self, go_obj, i, j):
        '''
        Detect all the neighbors of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbors row and column (row, column) of position (i, j).
        '''
        board = go_obj.board
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    def detect_neighbor_ally(self, go_obj, i, j):
        '''
        Detect the neighbor allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
        '''
        board = go_obj.board
        neighbors = self.detect_neighbor(go_obj, i, j)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    def ally_dfs(self, go_obj, i, j):
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
            neighbor_allies = self.detect_neighbor_ally(go_obj, piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    def count_liberty(self, go_obj, i, j):
        '''
        Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: boolean indicating whether the given stone still has liberty.
        '''
        board = go_obj.board
        count = 0
        ally_members = self.ally_dfs(go_obj, i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(go_obj, member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    count+=1
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return count

    def evaluation(self, go_obj):
        score = 0
        our_piece_count = 0
        opponent_piece_count = 0
        our_liberty_count = 0
        opponent_liberty_count = 0
        for i in range(go_obj.size):
            for j in range(go_obj.size):
                if go_obj.board[i][j] == self.piece_type:
                    our_piece_count += 1
                    our_liberty_count += self.count_liberty(go_obj, i, j)
                elif go_obj.board[i][j] == self.opponent_piece_type:
                    opponent_piece_count += 1
                    opponent_liberty_count += self.count_liberty(go_obj, i, j)
        
        score = our_piece_count-opponent_piece_count+our_liberty_count-opponent_liberty_count
        if self.verbose:
            print(f"our_piece_count: {our_piece_count}")
            print(f"opponent_piece_count: {opponent_piece_count}")
            print(f"our_liberty_count: {our_liberty_count}")
            print(f"opponent_liberty_count: {opponent_liberty_count}")
        return score


    def minimax(self, go_obj, depth, isMaximizing):
        #need to check terminal condition
        if depth == 3:
            return self.evaluation(go_obj)
        
        if isMaximizing:
            bestScore = -float("inf")

            for i in range(go_obj.size):
                for j in range(go_obj.size):
                    if go_obj.valid_place_check(i, j, self.piece_type, test_check = True):
                        go_obj_before_move_max = deepcopy(go_obj)
                        placed_or_not_bool = go_obj.place_chess(i, j, self.piece_type)
                        score = self.minimax(go_obj, depth+1, False)
                        go_obj = go_obj_before_move_max
                        bestScore = max(score, bestScore)
            return bestScore
        
        else:
            bestScore = float("inf")
            for i in range(go_obj.size):
                for j in range(go_obj.size):
                    if go_obj.valid_place_check(i, j, self.opponent_piece_type, test_check = True):
                        go_obj_before_move_min = deepcopy(go_obj)
                        placed_or_not_bool = go_obj.place_chess(i, j, self.opponent_piece_type)
                        score = self.minimax(go_obj, depth+1, True)
                        go_obj = go_obj_before_move_min
                        bestScore = min(score, bestScore)
            return bestScore

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

        if self.verbose:
            print(f"possible placements: {possible_placements}")

        go_obj = deepcopy(go)
        # self.minimax(go_obj)


        if not possible_placements:
            return "PASS"
        else:
            move = "PASS"
            bestScore = -float("inf")
            for (x,y) in possible_placements:
                go_obj_copy = deepcopy(go_obj)
                go_obj.place_chess(x, y, piece_type)
                score = self.minimax(go_obj, 0, True)
                go_obj = go_obj_copy
                if score > bestScore:
                    bestScore = score
                    move = (x,y)
                if self.verbose:
                    print(f"score: {score} best_score: {bestScore}")
                    print(f"move: {move}")
            
            return move

            #return random.choice(possible_placements)

if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer(piece_type)
    action = player.get_input(go, piece_type)
    writeOutput(action)