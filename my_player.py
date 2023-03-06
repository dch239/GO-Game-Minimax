# from copy import deepcopy
# import random
# import sys
# from tabnanny import verbose
# from read import readInput
# from write import writeOutput
# import pdb

# from host import GO

# class RandomPlayer():
#     def __init__(self, previous_board, board, piece_type, n):
#         self.type = 'random'
#         self.piece_type = piece_type
#         if piece_type == 1:
#             self.opponent_piece_type = 2
#         else:
#             self.opponent_piece_type = 1
        
#         # self.piece_pointer = None

#         self.size = n
#         #self.previous_board = None # Store the previous board
#         self.X_move = True # X chess plays first
#         self.died_pieces = [] # Intialize died pieces to be empty
#         self.n_move = 0 # Trace the number of moves
#         self.max_move = n * n - 1 # The max movement of a Go game
#         self.komi = n/2 # Komi rule
#         self.verbose = False # Verbose only when there is a manual player

#         #set board first
#         self.set_board(piece_type=piece_type,previous_board=previous_board,board=board)


#     def init_board(self, n):
#         '''
#         Initialize a board with size n*n.

#         :param n: width and height of the board.
#         :return: None.
#         '''
#         board = [[0 for x in range(n)] for y in range(n)]  # Empty space marked as 0
#         # 'X' pieces marked as 1
#         # 'O' pieces marked as 2
#         self.board = board
#         self.previous_board = deepcopy(board)

#     def set_board(self, piece_type, previous_board, board):
#         '''
#         Initialize board status.
#         :param previous_board: previous board state.
#         :param board: current board state.
#         :return: None.
#         '''

#         # 'X' pieces marked as 1
#         # 'O' pieces marked as 2

#         for i in range(self.size):
#             for j in range(self.size):
#                 if previous_board[i][j] == piece_type and board[i][j] != piece_type:
#                     self.died_pieces.append((i, j))

#         # self.piece_type = piece_type
#         self.previous_board = previous_board
#         self.board = board

#     def compare_board(self, board1, board2):
#         for i in range(self.size):
#             for j in range(self.size):
#                 if board1[i][j] != board2[i][j]:
#                     return False
#         return True

#     def copy_board(self):
#         '''
#         Copy the current board for potential testing.

#         :param: None.
#         :return: the copied board instance.
#         '''
#         return deepcopy(self)

#     def detect_neighbor(self, i, j):
#         '''
#         Detect all the neighbors of a given stone.

#         :param i: row number of the board.
#         :param j: column number of the board.
#         :return: a list containing the neighbors row and column (row, column) of position (i, j).
#         '''
#         board = self.board
#         neighbors = []
#         # Detect borders and add neighbor coordinates
#         if i > 0: neighbors.append((i-1, j))
#         if i < len(board) - 1: neighbors.append((i+1, j))
#         if j > 0: neighbors.append((i, j-1))
#         if j < len(board) - 1: neighbors.append((i, j+1))
#         return neighbors

#     def detect_neighbor_ally(self, i, j):
#         '''
#         Detect the neighbor allies of a given stone.

#         :param i: row number of the board.
#         :param j: column number of the board.
#         :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
#         '''
#         board = self.board
#         neighbors = self.detect_neighbor(i, j)  # Detect neighbors
#         group_allies = []
#         # Iterate through neighbors
#         for piece in neighbors:
#             # Add to allies list if having the same color
#             if board[piece[0]][piece[1]] == board[i][j]:
#                 group_allies.append(piece)
#         return group_allies

#     def ally_dfs(self, i, j):
#         '''
#         Using DFS to search for all allies of a given stone.

#         :param i: row number of the board.
#         :param j: column number of the board.
#         :return: a list containing the all allies row and column (row, column) of position (i, j).
#         '''
#         stack = [(i, j)]  # stack for DFS serach
#         ally_members = []  # record allies positions during the search
#         while stack:
#             piece = stack.pop()
#             ally_members.append(piece)
#             neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
#             for ally in neighbor_allies:
#                 if ally not in stack and ally not in ally_members:
#                     stack.append(ally)
#         return ally_members

#     def find_liberty(self, i, j):
#         '''
#         Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

#         :param i: row number of the board.
#         :param j: column number of the board.
#         :return: boolean indicating whether the given stone still has liberty.
#         '''
#         board = self.board
#         ally_members = self.ally_dfs(i, j)
#         for member in ally_members:
#             neighbors = self.detect_neighbor(member[0], member[1])
#             for piece in neighbors:
#                 # If there is empty space around a piece, it has liberty
#                 if board[piece[0]][piece[1]] == 0:
#                     return True
#         # If none of the pieces in a allied group has an empty space, it has no liberty
#         return False

#     def return_liberty(self, i , j):
#         board = self.board
#         #count = 0
#         liberties = set()
#         if j>0 and board[i][j-1] == 0:
#             liberties.add((i, j-1))
#         if j<self.size-1 and board[i][j+1] == 0:
#             liberties.add((i, j+1))
#         if i>0 and board[i-1][j] == 0:
#             liberties.add((i-1, j))
#         if i<self.size-1 and board[i+1][j] == 0:
#             liberties.add((i+1, j))
        

#         # ally_members = self.ally_dfs(i, j)
#         # for member in ally_members:
#         #     neighbors = self.detect_neighbor(member[0], member[1])
#         #     for piece in neighbors:
#         #         # If there is empty space around a piece, it has liberty
#         #         if board[piece[0]][piece[1]] == 0:
#         #             #count+=1
#         #             liberties.add((piece[0], piece[1]))
#         # # If none of the pieces in a allied group has an empty space, it has no liberty
#         return liberties
        

#     def count_liberty(self, i, j):
#         '''
#         Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

#         :param i: row number of the board.
#         :param j: column number of the board.
#         :return: boolean indicating whether the given stone still has liberty.
#         '''
#         board = self.board
#         #count = 0
#         liberties = set()
#         ally_members = self.ally_dfs(i, j)
#         for member in ally_members:
#             neighbors = self.detect_neighbor(member[0], member[1])
#             for piece in neighbors:
#                 # If there is empty space around a piece, it has liberty
#                 if board[piece[0]][piece[1]] == 0:
#                     #count+=1
#                     liberties.add((piece[0], piece[1]))
#         # If none of the pieces in a allied group has an empty space, it has no liberty
#         return len(liberties)    

#     def find_died_pieces(self, piece_type):
#         '''
#         Find the died stones that has no liberty in the board for a given piece type.

#         :param piece_type: 1('X') or 2('O').
#         :return: a list containing the dead pieces row and column(row, column).
#         '''
#         board = self.board
#         died_pieces = []

#         for i in range(len(board)):
#             for j in range(len(board)):
#                 # Check if there is a piece at this position:
#                 if board[i][j] == piece_type:
#                     # The piece die if it has no liberty
#                     if not self.find_liberty(i, j):
#                         died_pieces.append((i,j))
#         return died_pieces

#     def remove_died_pieces(self, piece_type):
#         '''
#         Remove the dead stones in the board.

#         :param piece_type: 1('X') or 2('O').
#         :return: locations of dead pieces.
#         '''

#         died_pieces = self.find_died_pieces(piece_type)
#         if not died_pieces: return []
#         self.remove_certain_pieces(died_pieces)
#         return died_pieces

#     def remove_certain_pieces(self, positions):
#         '''
#         Remove the stones of certain locations.

#         :param positions: a list containing the pieces to be removed row and column(row, column)
#         :return: None.
#         '''
#         board = self.board
#         for piece in positions:
#             board[piece[0]][piece[1]] = 0
#         self.update_board(board)

#     def place_chess(self, i, j, piece_type):
#         '''
#         Place a chess stone in the board.

#         :param i: row number of the board.
#         :param j: column number of the board.
#         :param piece_type: 1('X') or 2('O').
#         :return: boolean indicating whether the placement is valid.
#         '''
#         board = self.board

#         valid_place = self.valid_place_check(i, j, piece_type)
#         if not valid_place:
#             return False
#         self.previous_board = deepcopy(board)
#         board[i][j] = piece_type
#         self.update_board(board)
#         # Remove the following line for HW2 CS561 S2020
#         # self.n_move += 1
#         return True

#     def valid_place_check(self, i, j, piece_type, test_check=False):
#         '''
#         Check whether a placement is valid.

#         :param i: row number of the board.
#         :param j: column number of the board.
#         :param piece_type: 1(white piece) or 2(black piece).
#         :param test_check: boolean if it's a test check.
#         :return: boolean indicating whether the placement is valid.
#         '''   
#         board = self.board
#         verbose = self.verbose
#         if test_check:
#             verbose = False

#         # Check if the place is in the board range
#         if not (i >= 0 and i < len(board)):
#             if verbose:
#                 print(('Invalid placement. row should be in the range 1 to {}.').format(len(board) - 1))
#             return False
#         if not (j >= 0 and j < len(board)):
#             if verbose:
#                 print(('Invalid placement. column should be in the range 1 to {}.').format(len(board) - 1))
#             return False
        
#         # Check if the place already has a piece
#         if board[i][j] != 0:
#             if verbose:
#                 print('Invalid placement. There is already a chess in this position.')
#             return False
        
#         # Copy the board for testing
#         test_go = self.copy_board()
#         test_board = test_go.board

#         # Check if the place has liberty
#         test_board[i][j] = piece_type
#         test_go.update_board(test_board)
#         if test_go.find_liberty(i, j):
#             return True

#         # If not, remove the died pieces of opponent and check again
#         test_go.remove_died_pieces(3 - piece_type)
#         if not test_go.find_liberty(i, j):
#             if verbose:
#                 print('Invalid placement. No liberty found in this position.')
#             return False

#         # Check special case: repeat placement causing the repeat board state (KO rule)
#         else:
#             if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
#                 if verbose:
#                     print('Invalid placement. A repeat move not permitted by the KO rule.')
#                 return False
#         return True
        
#     def update_board(self, new_board):
#         '''
#         Update the board with new_board

#         :param new_board: new board.
#         :return: None.
#         '''   
#         self.board = new_board

#     def visualize_board(self):
#         '''
#         Visualize the board.

#         :return: None
#         '''
#         board = self.board

#         print('-' * len(board) * 2)
#         for i in range(len(board)):
#             for j in range(len(board)):
#                 if board[i][j] == 0:
#                     print(' ', end=' ')
#                 elif board[i][j] == 1:
#                     print('X', end=' ')
#                 else:
#                     print('O', end=' ')
#             print()
#         print('-' * len(board) * 2)

#     def no_of_empty_places(self):
#         count = 0
#         for i in range(self.size):
#             for j in range(self.size):
#                 if self.board[i][j] == 0:
#                     count += 1
#         return count


#     # CREDITS: INSPIRED BY Using Search Techniques in the Board Game Go Kindel et al.
#     def evaluation(self, empty, piece_pointer):
#         our_piece_pointer = piece_pointer
#         opponent_piece_pointer = 3 - our_piece_pointer
#         score = 0
#         our_piece_count = 0
#         opponent_piece_count = 0
#         our_liberty_count = 0
#         our_liberties = set()
#         opponent_liberty_count = 0
#         opponent_liberties = set()
#         #edge counts
#         our_edge_count = 0
#         opponent_edge_count = 0 
#         #window euler counts
#         for i in range(self.size):
#             for j in range(self.size):
#                 #edge count
#                 if i == 0 or j==0 or i==self.size-1 or j==self.size-1:
#                     if self.board[i][j] == our_piece_pointer:
#                         our_edge_count += 1
#                     elif self.board[i][j] == opponent_piece_pointer:
#                         opponent_edge_count += 1


#                 if self.board[i][j] == our_piece_pointer:
#                     our_piece_count += 1
#                     #our_liberty_count += self.count_liberty(i, j)
#                     temp = self.return_liberty(i, j)
#                     for e in temp:
#                         our_liberties.add(e)
#                 elif self.board[i][j] == opponent_piece_pointer:
#                     opponent_piece_count += 1
#                     #opponent_liberty_count += self.count_liberty(i, j)
#                     temp = self.return_liberty(i, j)
#                     for e in temp:
#                         opponent_liberties.add(e)
#                     #opponent_liberties.add(self.return_liberty(i, j))

#         #liberty count
#         our_liberty_count = len(our_liberties)
#         opponent_liberty_count = len(opponent_liberties)
#         #euler count
#         our_q1 = 0
#         opponent_q1 = 0
#         our_q3 = 0
#         opponent_q3 = 0
#         our_qd = 0
#         opponent_qd = 0
#         for i in range(self.size-1):
#             for j in range(self.size-1):
#                 p1 = self.board[i][j]
#                 p2 = self.board[i][j+1]
#                 p3 = self.board[i+1][j]
#                 p4 = self.board[i+1][j+1]
#                 #case 1: one corner piece
#                 #a
#                 if p1 == 0 and p2 == 0 and p3==0 and p4 == our_piece_pointer:
#                     our_q1 += 1
#                 if p1 == 0 and p2 == 0 and p3==0 and p4 == opponent_piece_pointer:
#                     opponent_q1 += 1
#                 #b
#                 if p1 == 0 and p2 == 0 and p3==our_piece_pointer and p4 == 0:
#                     our_q1 += 1
#                 if p1 == 0 and p2 == 0 and p3==opponent_piece_pointer and p4 == 0:
#                     opponent_q1 += 1
#                 #c
#                 if p1 == 0 and p2 == our_piece_pointer and p3==0 and p4 == 0:
#                     our_q1 += 1
#                 if p1 == 0 and p2 == opponent_piece_pointer and p3==0 and p4 == 0:
#                     opponent_q1 += 1
#                 #d
#                 if p1 == our_piece_pointer and p2 == 0 and p3==0 and p4 == 0:
#                     our_q1 += 1
#                 if p1 == opponent_piece_pointer and p2 == 0 and p3==0 and p4 == 0:
#                     opponent_q1 += 1
                
#                 #case 2: 3 piece
#                 #a
#                 if p1 == 0 and p2 == our_piece_pointer and p3==our_piece_pointer and p4 == our_piece_pointer:
#                     our_q3 += 1
#                 if p1 == 0 and p2 == opponent_piece_pointer and p3==opponent_piece_pointer and p4 == opponent_piece_pointer:
#                     opponent_q3 += 1
#                 #b
#                 if p1 == our_piece_pointer and p2 == 0 and p3==our_piece_pointer and p4 == our_piece_pointer:
#                     our_q3 += 1
#                 if p1 == opponent_piece_pointer and p2 == 0 and p3==opponent_piece_pointer and p4 == opponent_piece_pointer:
#                     opponent_q3 += 1
#                 #c
#                 if p1 == our_piece_pointer and p2 == our_piece_pointer and p3==0 and p4 == our_piece_pointer:
#                     our_q3 += 1
#                 if p1 == opponent_piece_pointer and p2 == opponent_piece_pointer and p3==0 and p4 == opponent_piece_pointer:
#                     opponent_q3 += 1
#                 #d
#                 if p1 == our_piece_pointer and p2 == our_piece_pointer and p3==our_piece_pointer and p4 == 0:
#                     our_q3 += 1
#                 if p1 == opponent_piece_pointer and p2 == opponent_piece_pointer and p3==opponent_piece_pointer and p4 == 0:
#                     opponent_q3 += 1

#                 #case 3: twins
#                 #a
#                 if p1 == our_piece_pointer and p2 == 0 and p3 == 0 and p4 == our_piece_pointer:
#                     our_qd += 1
#                 if p1 == opponent_piece_pointer and p2 == 0 and p3 == 0 and p4 == opponent_piece_pointer:
#                     opponent_qd += 1    
#                 #b
#                 if p1 == 0 and p2 == our_piece_pointer and p3 == our_piece_pointer and p4 == 0:
#                     our_qd += 1
#                 if p1 == 0 and p2 == opponent_piece_pointer and p3 == opponent_piece_pointer and p4 == 0:
#                     opponent_qd += 1 
        
#         our_euler_score = (our_q1 - our_q3 + 2*our_qd)/4
#         opponent_euler_score = (opponent_q1 - opponent_q3 + 2*opponent_qd)/4

#         score1 = our_piece_count - opponent_piece_count
#         score2 = our_liberty_count - opponent_liberty_count
#         score3 = opponent_edge_count - our_edge_count
#         score4 = our_euler_score - opponent_euler_score     
    
#         # if piece_pointer == 1:
#         #     score -= 5
#         # else:
#         #     score += 5
#         # score = min(max(score2, -4), 4) + (-4)*score4 + 5 * score1 + 3*score3
#         if empty>10:
#             # black strategy
#             if piece_pointer == 1:
#                 # print(our_liberty_count, our_euler_score, our_piece_count, opponent_edge_count)
#                 # print(opponent_liberty_count, opponent_euler_score, our_piece_count, our_edge_count)
#                 our_score = 7*our_liberty_count + (-6)*our_euler_score + 15*our_piece_count + 5*opponent_edge_count
#                 opponent_score = 10*opponent_liberty_count + (-3) * opponent_euler_score+ 12*opponent_piece_count + 4*our_edge_count

#             # #white strategy
#             if piece_pointer == 2:
#                 our_score = 5*our_liberty_count + (-6)*our_euler_score + 15 * our_piece_count + 5*opponent_edge_count
#                 opponent_score = 8*opponent_liberty_count + (-3) * opponent_euler_score + 11 * opponent_piece_count + 4*our_edge_count

#         #     # self.visualize_board()
#         #     # print(f"piece pointer = {piece_pointer}")
#         #     # print(f"{our_liberty_count}+{our_euler_score}+{our_piece_count}+{opponent_edge_count}")
#         #     # print(f"{opponent_liberty_count}+{opponent_euler_score}+{opponent_piece_count}+{our_edge_count}")
#         #     # print(f"score: {score}")
#         #     score += our_score - opponent_score
        
#         else:
#             our_score = 10*(our_piece_count+our_liberty_count)
#             opponent_score = 5*(opponent_piece_count+opponent_liberty_count)
#             score += our_score - opponent_score
        
#         return score

#     def negaMax(self, depth, piece_pointer):
#         empty = self.no_of_empty_places()
#         if(empty < 10):
#             it = 3
#         else:
#             it = 2 
#         if depth == it:
#             return self.evaluation(empty, piece_pointer)
#         mx = -float("inf")
#         for i in range(self.size):
#             for j in range(self.size):
#                 if self.valid_place_check(i, j, piece_pointer, test_check = True):
#                     old_board = deepcopy(self.board)
#                     old_died_pieces = deepcopy(self.died_pieces)
#                     old_previous_board = deepcopy(self.previous_board)
#                     placed_or_not_bool = self.place_chess(i, j, piece_pointer)
#                     if self.verbose:
#                         print("max")
#                         self.visualize_board()
#                     score = -self.negaMax(depth+1, 3-piece_pointer)
#                     self.board = deepcopy(old_board)
#                     self.died_pieces = deepcopy(old_died_pieces)
#                     self.previous_board = deepcopy(old_previous_board)
#                     mx = max(score, mx)
#         return mx

#     def minimax(self, depth, isMaximizing, piece_pointer):
#         #need to check terminal condition
#         empty = self.no_of_empty_places()
#         if(empty < 10):
#             it = 3
#         else:
#             it = 2 
#         if depth == it:
#             return self.evaluation(empty, piece_pointer)
        
#         if isMaximizing:
#             bestScore = -float("inf")

#             for i in range(self.size):
#                 for j in range(self.size):
#                     if self.valid_place_check(i, j, self.piece_type, test_check = True):
#                         old_board = deepcopy(self.board)
#                         old_died_pieces = deepcopy(self.died_pieces)
#                         old_previous_board = deepcopy(self.previous_board)
#                         placed_or_not_bool = self.place_chess(i, j, self.piece_type)

#                         if self.verbose:
#                             print("max place")
#                             self.visualize_board()

#                         # self.piece_pointer = self.opponent_piece_type    

#                         score = self.minimax(depth+1, False, self.piece_type)
                        
#                         self.board = deepcopy(old_board)
#                         self.died_pieces = deepcopy(old_died_pieces)
#                         self.previous_board = deepcopy(old_previous_board)

#                         bestScore = max(score, bestScore)
#             return bestScore
        
#         else:
#             bestScore = float("inf")
#             for i in range(self.size):
#                 for j in range(self.size):
#                     if self.valid_place_check(i, j, self.opponent_piece_type, test_check = True):
#                         old_board = deepcopy(self.board)
#                         old_died_pieces = deepcopy(self.died_pieces)
#                         old_previous_board = deepcopy(self.previous_board)
#                         placed_or_not_bool = self.place_chess(i, j, self.opponent_piece_type)
                        
#                         if self.verbose:
#                             print("min place")
#                             self.visualize_board()

#                         # self.piece_pointer = self.piece_type

#                         score = self.minimax(depth+1, True, self.piece_type)
#                         self.board = deepcopy(old_board)
#                         self.died_pieces = deepcopy(old_died_pieces)
#                         self.previous_board = deepcopy(old_previous_board)
                        
#                         bestScore = min(score, bestScore)
#             return bestScore


#     def get_input(self):
#         '''
#         Get one input.

#         :param go: Go instance.
#         :param piece_type: 1('X') or 2('O').
#         :return: (row, column) coordinate of input.
#         '''        
#         possible_placements = []
#         for i in range(self.size):
#             for j in range(self.size):
#                 if self.valid_place_check(i, j, self.piece_type, test_check = True):
#                     possible_placements.append((i,j))

#         if self.verbose:
#             print(f"possible placements: {possible_placements}")

#         # go_obj = deepcopy(go)
#         # self.minimax(go_obj)


#         if not possible_placements:
#             return "PASS"
#         else:
#             move = "PASS"
#             bestScore = -float("inf")
#             for (x,y) in possible_placements:
#                 old_board = deepcopy(self.board)
#                 old_died_pieces = deepcopy(self.died_pieces)
#                 old_previous_board = deepcopy(self.previous_board)

#                 # self.visualize_board()
#                 # print(f"checking placement at {x, y}")

                

#                 self.place_chess(x, y, self.piece_type)
                
#                 # self.piece_pointer = self.piece_type #new heuristic
#                 # score = self.negaMax(0, piece_type)
#                 score = self.minimax(0, True, piece_type)
                
#                 self.board = deepcopy(old_board)
#                 self.died_pieces = deepcopy(old_died_pieces)
#                 self.previous_board = deepcopy(old_previous_board)
                
#                 # print("After")
#                 # self.visualize_board()

#                 if score > bestScore:
#                     bestScore = score
#                     move = (x,y)
#                 if self.verbose:
#                     print(f"score: {score} best_score: {bestScore}")
#                     print(f"move: {move}")
            
#             return move

#             #return random.choice(possible_placements)

# if __name__ == "__main__":
#     N = 5
#     piece_type, previous_board, board = readInput(N)
#     go = GO(N)
#     go.set_board(piece_type, previous_board, board)
#     player = RandomPlayer(previous_board=previous_board, board=board, piece_type=piece_type, n=N)
#     action = player.get_input()
#     writeOutput(action)

from copy import deepcopy
import random
import sys
from tabnanny import verbose
from read import readInput
from write import writeOutput
import pdb

from host import GO

class RandomPlayer():
    def __init__(self, previous_board, board, piece_type, n):
        self.type = 'random'
        self.piece_type = piece_type
        if piece_type == 1:
            self.opponent_piece_type = 2
        else:
            self.opponent_piece_type = 1
        
        # self.piece_pointer = None

        self.size = n
        #self.previous_board = None # Store the previous board
        self.X_move = True # X chess plays first
        self.died_pieces = [] # Intialize died pieces to be empty
        self.n_move = 0 # Trace the number of moves
        self.max_move = n * n - 1 # The max movement of a Go game
        self.komi = n/2 # Komi rule
        self.verbose = False # Verbose only when there is a manual player

        #set board first
        self.set_board(piece_type=piece_type,previous_board=previous_board,board=board)


    def init_board(self, n):
        '''
        Initialize a board with size n*n.

        :param n: width and height of the board.
        :return: None.
        '''
        board = [[0 for x in range(n)] for y in range(n)]  # Empty space marked as 0
        # 'X' pieces marked as 1
        # 'O' pieces marked as 2
        self.board = board
        self.previous_board = deepcopy(board)

    def set_board(self, piece_type, previous_board, board):
        '''
        Initialize board status.
        :param previous_board: previous board state.
        :param board: current board state.
        :return: None.
        '''

        # 'X' pieces marked as 1
        # 'O' pieces marked as 2

        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))

        # self.piece_type = piece_type
        self.previous_board = previous_board
        self.board = board

    def compare_board(self, board1, board2):
        for i in range(self.size):
            for j in range(self.size):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def copy_board(self):
        '''
        Copy the current board for potential testing.

        :param: None.
        :return: the copied board instance.
        '''
        return deepcopy(self)

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

    def return_liberty(self, i , j):
        board = self.board
        #count = 0
        liberties = set()
        if j>0 and board[i][j-1] == 0:
            liberties.add((i, j-1))
        if j<self.size-1 and board[i][j+1] == 0:
            liberties.add((i, j+1))
        if i>0 and board[i-1][j] == 0:
            liberties.add((i-1, j))
        if i<self.size-1 and board[i+1][j] == 0:
            liberties.add((i+1, j))
        

        # ally_members = self.ally_dfs(i, j)
        # for member in ally_members:
        #     neighbors = self.detect_neighbor(member[0], member[1])
        #     for piece in neighbors:
        #         # If there is empty space around a piece, it has liberty
        #         if board[piece[0]][piece[1]] == 0:
        #             #count+=1
        #             liberties.add((piece[0], piece[1]))
        # # If none of the pieces in a allied group has an empty space, it has no liberty
        return liberties
        

    def count_liberty(self, i, j):
        '''
        Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: boolean indicating whether the given stone still has liberty.
        '''
        board = self.board
        #count = 0
        liberties = set()
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    #count+=1
                    liberties.add((piece[0], piece[1]))
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return len(liberties)    

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

    def place_chess(self, i, j, piece_type):
        '''
        Place a chess stone in the board.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the placement is valid.
        '''
        board = self.board

        valid_place = self.valid_place_check(i, j, piece_type)
        if not valid_place:
            return False
        self.previous_board = deepcopy(board)
        board[i][j] = piece_type
        self.update_board(board)
        # Remove the following line for HW2 CS561 S2020
        # self.n_move += 1
        return True

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
        
    def update_board(self, new_board):
        '''
        Update the board with new_board

        :param new_board: new board.
        :return: None.
        '''   
        self.board = new_board

    def visualize_board(self):
        '''
        Visualize the board.

        :return: None
        '''
        board = self.board

        print('-' * len(board) * 2)
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    print(' ', end=' ')
                elif board[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        print('-' * len(board) * 2)

    def no_of_empty_places(self):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    count += 1
        return count


    # CREDITS: INSPIRED BY Using Search Techniques in the Board Game Go Kindel et al.
    def evaluation(self, empty, piece_pointer):
        our_piece_pointer = piece_pointer
        opponent_piece_pointer = 3 - our_piece_pointer
        score = 0
        our_piece_count = 0
        opponent_piece_count = 0
        our_liberty_count = 0
        our_liberties = set()
        opponent_liberty_count = 0
        opponent_liberties = set()
        #edge counts
        our_edge_count = 0
        opponent_edge_count = 0 
        #window euler counts
        for i in range(self.size):
            for j in range(self.size):
                #edge count
                if i == 0 or j==0 or i==self.size-1 or j==self.size-1:
                    if self.board[i][j] == our_piece_pointer:
                        our_edge_count += 1
                    elif self.board[i][j] == opponent_piece_pointer:
                        opponent_edge_count += 1


                if self.board[i][j] == our_piece_pointer:
                    our_piece_count += 1
                    #our_liberty_count += self.count_liberty(i, j)
                    temp = self.return_liberty(i, j)
                    for e in temp:
                        our_liberties.add(e)
                elif self.board[i][j] == opponent_piece_pointer:
                    opponent_piece_count += 1
                    #opponent_liberty_count += self.count_liberty(i, j)
                    temp = self.return_liberty(i, j)
                    for e in temp:
                        opponent_liberties.add(e)
                    #opponent_liberties.add(self.return_liberty(i, j))

        #liberty count
        our_liberty_count = len(our_liberties)
        opponent_liberty_count = len(opponent_liberties)
        #euler count
        our_q1 = 0
        opponent_q1 = 0
        our_q3 = 0
        opponent_q3 = 0
        our_qd = 0
        opponent_qd = 0
        for i in range(self.size-1):
            for j in range(self.size-1):
                p1 = self.board[i][j]
                p2 = self.board[i][j+1]
                p3 = self.board[i+1][j]
                p4 = self.board[i+1][j+1]
                #case 1: one corner piece
                #a
                if p1 == 0 and p2 == 0 and p3==0 and p4 == our_piece_pointer:
                    our_q1 += 1
                if p1 == 0 and p2 == 0 and p3==0 and p4 == opponent_piece_pointer:
                    opponent_q1 += 1
                #b
                if p1 == 0 and p2 == 0 and p3==our_piece_pointer and p4 == 0:
                    our_q1 += 1
                if p1 == 0 and p2 == 0 and p3==opponent_piece_pointer and p4 == 0:
                    opponent_q1 += 1
                #c
                if p1 == 0 and p2 == our_piece_pointer and p3==0 and p4 == 0:
                    our_q1 += 1
                if p1 == 0 and p2 == opponent_piece_pointer and p3==0 and p4 == 0:
                    opponent_q1 += 1
                #d
                if p1 == our_piece_pointer and p2 == 0 and p3==0 and p4 == 0:
                    our_q1 += 1
                if p1 == opponent_piece_pointer and p2 == 0 and p3==0 and p4 == 0:
                    opponent_q1 += 1
                
                #case 2: 3 piece
                #a
                if p1 == 0 and p2 == our_piece_pointer and p3==our_piece_pointer and p4 == our_piece_pointer:
                    our_q3 += 1
                if p1 == 0 and p2 == opponent_piece_pointer and p3==opponent_piece_pointer and p4 == opponent_piece_pointer:
                    opponent_q3 += 1
                #b
                if p1 == our_piece_pointer and p2 == 0 and p3==our_piece_pointer and p4 == our_piece_pointer:
                    our_q3 += 1
                if p1 == opponent_piece_pointer and p2 == 0 and p3==opponent_piece_pointer and p4 == opponent_piece_pointer:
                    opponent_q3 += 1
                #c
                if p1 == our_piece_pointer and p2 == our_piece_pointer and p3==0 and p4 == our_piece_pointer:
                    our_q3 += 1
                if p1 == opponent_piece_pointer and p2 == opponent_piece_pointer and p3==0 and p4 == opponent_piece_pointer:
                    opponent_q3 += 1
                #d
                if p1 == our_piece_pointer and p2 == our_piece_pointer and p3==our_piece_pointer and p4 == 0:
                    our_q3 += 1
                if p1 == opponent_piece_pointer and p2 == opponent_piece_pointer and p3==opponent_piece_pointer and p4 == 0:
                    opponent_q3 += 1

                #case 3: twins
                #a
                if p1 == our_piece_pointer and p2 == 0 and p3 == 0 and p4 == our_piece_pointer:
                    our_qd += 1
                if p1 == opponent_piece_pointer and p2 == 0 and p3 == 0 and p4 == opponent_piece_pointer:
                    opponent_qd += 1    
                #b
                if p1 == 0 and p2 == our_piece_pointer and p3 == our_piece_pointer and p4 == 0:
                    our_qd += 1
                if p1 == 0 and p2 == opponent_piece_pointer and p3 == opponent_piece_pointer and p4 == 0:
                    opponent_qd += 1 
        
        our_euler_score = (our_q1 - our_q3 + 2*our_qd)/4
        opponent_euler_score = (opponent_q1 - opponent_q3 + 2*opponent_qd)/4

        
    
        if piece_pointer == 1:
            score -= 15
        else:
            score += 15
        
        if empty>10:
            # black strategy
            if piece_pointer == 1:
                # print(our_liberty_count, our_euler_score, our_piece_count, opponent_edge_count)
                # print(opponent_liberty_count, opponent_euler_score, our_piece_count, our_edge_count)
                our_score = 7*our_liberty_count + (-6)*our_euler_score + 15*our_piece_count + 5*opponent_edge_count
                opponent_score = 10*opponent_liberty_count + (-3) * opponent_euler_score+ 12*opponent_piece_count + 4*our_edge_count

            # #white strategy
            if piece_pointer == 2:
                our_score = 5*our_liberty_count + (-6)*our_euler_score + 15 * our_piece_count + 5*opponent_edge_count
                opponent_score = 8*opponent_liberty_count + (-3) * opponent_euler_score + 11 * opponent_piece_count + 4*our_edge_count

            # self.visualize_board()
            # print(f"piece pointer = {piece_pointer}")
            # print(f"{our_liberty_count}+{our_euler_score}+{our_piece_count}+{opponent_edge_count}")
            # print(f"{opponent_liberty_count}+{opponent_euler_score}+{opponent_piece_count}+{our_edge_count}")
            # print(f"score: {score}")
            score += our_score - opponent_score
        
        else:
            our_score = 10*(our_piece_count+our_liberty_count)
            opponent_score = 5*(opponent_piece_count+opponent_liberty_count)
            score += our_score - opponent_score
        
        return score

    def negaMax(self, depth, piece_pointer):
        empty = self.no_of_empty_places()
        if(empty < 10):
            it = 3
        else:
            it = 2 
        if depth == it:
            return self.evaluation(empty, piece_pointer)
        mx = -float("inf")
        for i in range(self.size):
            for j in range(self.size):
                if self.valid_place_check(i, j, piece_pointer, test_check = True):
                    old_board = deepcopy(self.board)
                    old_died_pieces = deepcopy(self.died_pieces)
                    old_previous_board = deepcopy(self.previous_board)
                    placed_or_not_bool = self.place_chess(i, j, piece_pointer)
                    if self.verbose:
                        print("max")
                        self.visualize_board()
                    score = -self.negaMax(depth+1, 3-piece_pointer)
                    self.board = deepcopy(old_board)
                    self.died_pieces = deepcopy(old_died_pieces)
                    self.previous_board = deepcopy(old_previous_board)
                    mx = max(score, mx)
        return mx

    def minimax(self, depth, isMaximizing, piece_pointer):
        #need to check terminal condition
        empty = self.no_of_empty_places()
        if(empty < 10):
            it = 3
        else:
            it = 2 
        if depth == it:
            return self.evaluation(empty, piece_pointer)
        
        if isMaximizing:
            bestScore = -float("inf")

            for i in range(self.size):
                for j in range(self.size):
                    if self.valid_place_check(i, j, piece_pointer, test_check = True):
                        old_board = deepcopy(self.board)
                        old_died_pieces = deepcopy(self.died_pieces)
                        old_previous_board = deepcopy(self.previous_board)
                        placed_or_not_bool = self.place_chess(i, j, piece_pointer)

                        if self.verbose:
                            print("max place")
                            self.visualize_board()

                        # self.piece_pointer = self.opponent_piece_type    

                        score = self.minimax(depth+1, False, piece_pointer)
                        
                        self.board = deepcopy(old_board)
                        self.died_pieces = deepcopy(old_died_pieces)
                        self.previous_board = deepcopy(old_previous_board)

                        bestScore = max(score, bestScore)
            return bestScore
        
        else:
            bestScore = float("inf")
            for i in range(self.size):
                for j in range(self.size):
                    if self.valid_place_check(i, j, 3-piece_pointer, test_check = True):
                        old_board = deepcopy(self.board)
                        old_died_pieces = deepcopy(self.died_pieces)
                        old_previous_board = deepcopy(self.previous_board)
                        placed_or_not_bool = self.place_chess(i, j, 3-piece_pointer)
                        
                        if self.verbose:
                            print("min place")
                            self.visualize_board()

                        # self.piece_pointer = self.piece_type

                        score = self.minimax(depth+1, True, piece_pointer)
                        self.board = deepcopy(old_board)
                        self.died_pieces = deepcopy(old_died_pieces)
                        self.previous_board = deepcopy(old_previous_board)
                        
                        bestScore = min(score, bestScore)
            return bestScore


    def get_input(self):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
        possible_placements = []
        for i in range(self.size):
            for j in range(self.size):
                if self.valid_place_check(i, j, self.piece_type, test_check = True):
                    possible_placements.append((i,j))

        if self.verbose:
            print(f"possible placements: {possible_placements}")

        # go_obj = deepcopy(go)
        # self.minimax(go_obj)


        if not possible_placements:
            return "PASS"
        else:
            move = "PASS"
            bestScore = -float("inf")
            for (x,y) in possible_placements:
                old_board = deepcopy(self.board)
                old_died_pieces = deepcopy(self.died_pieces)
                old_previous_board = deepcopy(self.previous_board)

                # self.visualize_board()
                # print(f"checking placement at {x, y}")

                

                self.place_chess(x, y, self.piece_type)
                
                # self.piece_pointer = self.piece_type #new heuristic
                score = self.negaMax(0, piece_type)
                # score = self.minimax(0, True, piece_type)
                
                self.board = deepcopy(old_board)
                self.died_pieces = deepcopy(old_died_pieces)
                self.previous_board = deepcopy(old_previous_board)
                
                # print("After")
                # self.visualize_board()

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
    player = RandomPlayer(previous_board=previous_board, board=board, piece_type=piece_type, n=N)
    action = player.get_input()
    writeOutput(action)