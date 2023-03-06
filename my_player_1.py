import itertools
from pprint import pprint as pp
from copy import deepcopy
import random
f = open('input.txt')

my_color = f.readline().strip()
print(my_color)

if my_color == '2':
    opp_color='1'
else:
    opp_color = '2'

prev_state = []
for line in itertools.islice(f,0,5):
    prev_state.append(list(line.strip()))

curr_state = []
for line in itertools.islice(f,0,5):
    curr_state.append(list(line.strip()))

f.close()


'''
 elif self.curr_state[i][j]!=color:
                    opp_score +=1

                else:
                    my_score +=1
                if self.curr_state[i][j] != self.prev_state[i][j]:
                    last_move = (i,j)
        if color == '2':
            opp_score = 0.0
            my_score = 2.5
        else:
            opp_score = 2.5
            my_score = 0.0


'''
class Node:

    def __init__(self,state,p_state,color):
        self.curr_state = state
        self.prev_state = p_state
        self.color = color
        self.newStates = []
        self.eval = 0.0
        self.pm = []
        self.newNodes = []
        self.alpha = float('-inf')
        self.beta = float('inf')
        print(self.color, 's turn')
        print('Previous State')
        #pp(self.prev_state)
        print('Current State')
        #pp(self.curr_state)

    def poss_moves(self):
        possible_moves = []

        for i in range(5):
            for j in range(5):
                if self.curr_state[i][j]=='0':
                    possible_moves.append((i,j))
         


        #pp(possible_moves)
        self.pm = possible_moves

    def getLastMove(self):
        last_move='PASS'
        for i in range(5):
            for j in range(5):
                if self.curr_state[i][j] != self.prev_state[i][j]:
                    last_move = (i,j)

        return last_move

    def new_states(self,possible_moves):
        for pm in possible_moves:
            cs = deepcopy(self.curr_state)
            cs[pm[0]][pm[1]] = self.color
            #pp(cs)
            self.newStates.append(cs)

    def DFS(self,i,j,visited,grp,colr):
        print(i,j,visited)
        grp.append((i,j))
        neighbor = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        for n in neighbor:
            if 0<=n[0]<5 and 0<=n[1]<5 and visited[n[0]][n[1]] == 0 and self.curr_state[n[0]][n[1]]==colr:
                visited[n[0]][n[1]] = 1
                self.DFS(n[0],n[1],visited,grp,colr)



    def find_groups(self,colr):
        mygrp = []
        visited = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        for i in range(5):
            for j in range(5):
                grp = []
                if self.curr_state[i][j]==colr and visited[i][j]==0:
                    visited[i][j] = 1
                    self.DFS(i,j,visited,grp,colr)
                    mygrp.append(grp)
                    print()
        print(mygrp)
        return mygrp

    def find_liberties(self):
        my_libs = 0
        opp_libs = 0
        for i in range(5):
            for j in range(5):
                if self.curr_state[i][j]==my_color:
                    #print('Found',i,j)
                    if 0 <= i-1 < 5 and 0 <= j < 5 and self.curr_state[i-1][j]=='0':
                            my_libs+=1
                    if 0 <= i < 5 and 0 <= j-1 < 5 and self.curr_state[i][j-1]=='0':
                            my_libs+=1
                    if 0 <= i+1 < 5 and 0 <= j < 5 and self.curr_state[i+1][j]=='0':
                            my_libs+=1
                    if 0 <= i < 5 and 0 <= j+1 < 5 and self.curr_state[i][j+1]=='0':
                            my_libs+=1
                if self.curr_state[i][j]==opp_color:
                    #print('Found',i,j)
                    if 0 <= i-1 < 5 and 0 <= j < 5 and self.curr_state[i-1][j]=='0':
                            opp_libs+=1
                    if 0 <= i < 5 and 0 <= j-1 < 5 and self.curr_state[i][j-1]=='0':
                            opp_libs+=1
                    if 0 <= i+1 < 5 and 0 <= j < 5 and self.curr_state[i+1][j]=='0':
                            opp_libs+=1
                    if 0 <= i < 5 and 0 <= j+1 < 5 and self.curr_state[i][j+1]=='0':
                            opp_libs+=1

        print(my_libs,opp_libs)
        if my_color == '2':
            return min(max(opp_libs-my_libs,-4),4)
        else:
            return min(max(my_libs-opp_libs,-4),4)

    def getPieces(self):
        total = 0
        for i in range(5):
            for j in range(5):
                if self.curr_state[i][j]!='0':
                    total+=1
        return total

    def getEdgePieces(self):
        edge = 0
        for i in range(5):
            for j in range(5):
                if self.curr_state[i][j]!='0' and (i == 0 or i == 4 or j==0 or j == 4 ):
                    edge+=1
        return edge

    def scanEye(self):
        q1 = 0
        q3 = 0
        qd = 0
        print(my_color)
        for i in range(4):
            for j in range(4):
                window = [[self.curr_state[i][j],self.curr_state[i][j+1]],
                        [self.curr_state[i+1][j],self.curr_state[i+1][j+1]]]
                #pp(window)
                if (window[0][0] == '0' and window[0][1] == '0' and window[1][0] == '0' and window[1][1] == my_color) or (window[0][0] == '0' and window[0][1] == '0' and window[1][0] == my_color and window[1][1] == '0') or (window[0][0] == '0' and window[0][1] == my_color and window[1][0] == '0' and window[1][1] == '0') or (window[0][0] == my_color and window[0][1] == '0' and window[1][0] == '0' and window[1][1] == '0'):
                    q1+=1
                if (window[0][0] == '0' and window[0][1] == my_color and window[1][0] == my_color and window[1][1] == my_color) or (window[0][0] == my_color and window[0][1] == '0' and window[1][0] == my_color and window[1][1] == my_color) or (window[0][0] == my_color and window[0][1] == my_color and window[1][0] == '0' and window[1][1] == my_color) or (window[0][0] == my_color and window[0][1] == my_color and window[1][0] == my_color and window[1][1] == '0'):
                    q3+=1
                if (window[0][0] == my_color and window[0][1] == '0' and window[1][0] == '0' and window[1][1] == my_color) or (window[0][0] == '0' and window[0][1] == my_color and window[1][0] == my_color and window[1][1] == '0'):
                    qd+=1
        return -1*(q1-q3+2*qd)



    def evaluate(self):
        if my_color == '2':
            self.opp_score = 0.0
            self.my_score = 2.5
        else:
            self.opp_score = 2.5
            self.my_score = 0.0

        for i in range(5):
            for j in range(5):
                if self.curr_state[i][j]==my_color:
                    self.my_score+=1
                elif self.curr_state[i][j]==opp_color:
                    self.opp_score+=1
        lib = self.find_liberties()
        tot = self.getPieces()
        ed = self.getEdgePieces()
        eye = self.scanEye()

        print(lib,tot,ed,eye,self.my_score,self.opp_score)

        my_groups = self.find_groups(my_color)
        opp_groups = self.find_groups(opp_color)
        print(my_groups)
        print(opp_groups)
        E1 = 0
        E2 = 0
        for group in my_groups:
            E1 += len(group)
            E2 += len(group)**2

        for group in opp_groups:
            E1 -= len(group)
            E2 -= len(group)**2
        self.eval = E1+E2+(self.my_score-self.opp_score) + lib + eye + 5*tot+ed


'''
def minimax(node,colr):
    if not node.newNodes:
        print()
        pp(node.curr_state)
        node.evaluate()
        print(node.eval)
        return node.eval

    elif colr == my_color:
        maxeval = float('-inf')
        for nd in node.newNodes:
            evalu = minimax(nd,opp_color)
            maxeval = max(maxeval,evalu)
        node.eval = maxeval
        return maxeval

    elif colr == opp_color:
        mineval = float('inf')
        for nd in node.newNodes:
            evalu = minimax(nd,my_color)
            mineval = min(mineval,evalu)
        node.eval = mineval
        return mineval
'''
def ab_minimax(node,alpha,beta,colr):
    if not node.newNodes:
        print()
        pp(node.curr_state)
        node.evaluate()
        print(node.eval)
        return node.eval

    elif colr == my_color:
        maxeval = float('-inf')
        for nd in node.newNodes:
            evalu = ab_minimax(nd,alpha,beta,opp_color)
            maxeval = max(maxeval,evalu)
            alpha = max(alpha,evalu)
            if beta <= alpha:
                break
        node.eval = maxeval
        node.alpha = alpha
        return maxeval

    elif colr == opp_color:
        mineval = float('inf')
        for nd in node.newNodes:
            evalu = ab_minimax(nd,alpha,beta,my_color)
            mineval = min(mineval,evalu)
            beta = min(beta,evalu)
            if beta <= alpha:
                break
        node.eval = mineval
        node.beta = beta
        return mineval


def countlibs(state,move):
    lbs = 0
    lib_pos = []
    if 0 <= move[0] < 5 and 0<= move[1]-1 < 5 and state[move[0]][move[1]-1]=='0':
        lbs+=1
        lib_pos.append((move[0],move[1]-1))
    if 0 <= move[0] < 5 and 0<= move[1]+1 < 5 and state[move[0]][move[1]+1]=='0':
        lbs+=1
        lib_pos.append((move[0],move[1]+1))
    if 0 <= move[0]-1 < 5 and 0<= move[1] < 5 and state[move[0]-1][move[1]]=='0':
        lbs+=1
        lib_pos.append((move[0]-1,move[1]))
    if 0 <= move[0]+1 < 5 and 0<= move[1] < 5 and state[move[0]+1][move[1]]=='0':
        lbs+=1
        lib_pos.append((move[0]+1,move[1]))
    return lbs,lib_pos

def suicide(state,move):
    if (0 <= move[0] < 5 and 0<= move[1]-1 < 5 and state[move[0]][move[1]-1]==opp_color) and (0 <= move[0] < 5 and 0<= move[1]+1 < 5 and state[move[0]][move[1]+1]==opp_color) and (0 <= move[0]-1 < 5 and 0<= move[1] < 5 and state[move[0]-1][move[1]]==opp_color) and (0 <= move[0]+1 < 5 and 0<= move[1] < 5 and state[move[0]+1][move[1]]==opp_color) :
        return True
    return False


def grp_libs(state,group):
    glib = 0
    glib_pos = []
    for move in group:
        lib, pos = countlibs(state,move)
        glib+=lib
        glib_pos.extend(pos)
    return glib,glib_pos

n = Node(curr_state,prev_state,my_color)

if n.getPieces() < 16:
    n.poss_moves()
    n.new_states(n.pm)

    first_node = n

    parents = [first_node]
    print()


    ply = [parents]

    max_ply = 3
    for x in range(max_ply):
        if x % 2 == 0:
            colr = opp_color
        else:
            colr = my_color
        interply = []

        for parnt in ply[x]:

            base_prev = deepcopy(parnt.curr_state)
            nnd = Node(base_prev,base_prev,colr)

            pr = [nnd]
            i = 0
            for newstate in parnt.newStates:
                print('New State',i)
                ns = deepcopy(newstate)
                #pp(ns)

                n = Node(ns,base_prev,colr)
                if x < max_ply-1:
                    n.poss_moves()
                    n.new_states(n.pm)
                #print('First child')
                #pp(NS[0])
                #print(len(NS))
                print()
                pr.append(n)
                i+=1
            #print(len(pr))

            parnt.newNodes=pr
            interply.extend(pr)
        ply.append(interply)
        print()

    #print(ply)
    #print(len(ply[0]),len(ply[1]),len(ply[2]))

    #pp(len(first_node.newNodes[0].newNodes))

    print(first_node.eval)
    first_node.eval = ab_minimax(first_node,first_node.alpha,first_node.beta,my_color)
    #first_node.eval = minimax(first_node,my_color)
    print(first_node.eval)

    best_moves = []
    for nd in first_node.newNodes:
        lm = nd.getLastMove()

        if lm == (2,2):
            lm_score = 20
        elif lm == (1,1) or lm == (1,2) or lm == (1,3) or lm == (2,1) or lm == (2,3) or lm == (3,1) or lm == (3,2) or lm == (3,3):
            lm_score = 10
        elif lm == (0,1) or lm == (0,2) or lm == (0,3) or lm == (1,0) or lm == (2,0) or lm == (3,0) or lm == (1,4) or lm == (2,4) or lm == (3,4) or lm == (4,1) or lm == (4,2) or lm == (4,3):
            lm_score = 5
        elif lm == 'PASS':
            lm_score = -5
        else:
            lm_score = 0

        print(nd.eval,lm,lm_score)
        best_moves.append((lm,nd.eval+lm_score))

    best_moves.sort(key=lambda tup: tup[1])



    best_moves = best_moves[-4:]
    bm_lib = 0
    print(best_moves)

    my_move = 'PASS'

    pp(first_node.curr_state)
    for (move,evalu) in best_moves:
        print(move)
        lb,lbpos = countlibs(first_node.curr_state,move)
        print(lb)
        if lb > bm_lib:
            bm_lib = lb
            my_move = move

    if bm_lib == 0:
        non_suicidal = []
        for (move,evalu) in best_moves:
            if not suicide(first_node.curr_state,move):
                non_suicidal.append(move)

        opp_grps = first_node.find_groups()

        attack_points = []
        for og in opp_grps:
            attack_points.append(grp_libs(first_node.curr_state,og))

        print(attack_points)

        print(non_suicidal)
        for (lib,att) in attack_points:
            if lib > bm_lib:
                bm_lib = lib
                for m in att:
                    if m in non_suicidal:
                        my_move = m
                        
elif n.getPieces()>=16 and n.getPieces()<22:
    opp_grps = n.find_groups(opp_color)

    attack_points = []
    for og in opp_grps:
        attack_points.append(grp_libs(n.curr_state,og))
    print(attack_points)

    poss_mov = []
    for (lib,att) in attack_points:
        poss_mov.extend(att)
    print(poss_mov)
    #my_move = random.choice(poss_mov)
    n.pm = poss_mov

    n.new_states(n.pm)

    first_node = n

    parents = [first_node]
    print()


    ply = [parents]

    max_ply = 2
    for x in range(max_ply):
        if x % 2 == 0:
            colr = opp_color
        else:
            colr = my_color
        interply = []

        for parnt in ply[x]:

            base_prev = deepcopy(parnt.curr_state)
            nnd = Node(base_prev,base_prev,colr)

            pr = [nnd]
            i = 0
            for newstate in parnt.newStates:
                print('New State',i)
                ns = deepcopy(newstate)
                #pp(ns)

                n = Node(ns,base_prev,colr)
                if x < max_ply-1:
                    n.poss_moves()
                    n.new_states(n.pm)
                #print('First child')
                #pp(NS[0])
                #print(len(NS))
                print()
                pr.append(n)
                i+=1
            #print(len(pr))

            parnt.newNodes=pr
            interply.extend(pr)
        ply.append(interply)
        print()

    #print(ply)
    #print(len(ply[0]),len(ply[1]),len(ply[2]))

    #pp(len(first_node.newNodes[0].newNodes))

    print(first_node.eval)
    first_node.eval = ab_minimax(first_node,first_node.alpha,first_node.beta,my_color)
    #first_node.eval = minimax(first_node,my_color)
    print(first_node.eval)

    best_moves = []
    for nd in first_node.newNodes:
        lm = nd.getLastMove()

        if lm == (2,2):
            lm_score = 20
        elif lm == (1,1) or lm == (1,2) or lm == (1,3) or lm == (2,1) or lm == (2,3) or lm == (3,1) or lm == (3,2) or lm == (3,3):
            lm_score = 10
        elif lm == (0,1) or lm == (0,2) or lm == (0,3) or lm == (1,0) or lm == (2,0) or lm == (3,0) or lm == (1,4) or lm == (2,4) or lm == (3,4) or lm == (4,1) or lm == (4,2) or lm == (4,3):
            lm_score = 5
        elif lm == 'PASS':
            lm_score = -5
        else:
            lm_score = 0

        print(nd.eval,lm,lm_score)
        best_moves.append((lm,nd.eval+lm_score))

    best_moves.sort(key=lambda tup: tup[1])



    best_moves = best_moves[-4:]
    bm_lib = 0
    print(best_moves)

    my_move = 'PASS'

    pp(first_node.curr_state)
    for (move,evalu) in best_moves:
        print(move)
        lb,lbpos = countlibs(first_node.curr_state,move)
        print(lb)
        if lb > bm_lib:
            bm_lib = lb
            my_move = move

    if bm_lib == 0:
        my_move = best_moves[-1][0]

else:
    n.poss_moves()
    opp_grps = n.find_groups()

    attack_points = []
    for og in opp_grps:
        attack_points.append(grp_libs(n.curr_state,og))

    print(attack_points)

    my_move = 'PASS'
    bm_lib = 0

    non_suicidal = []
    for move in n.pm:
        if not suicide(n.curr_state,move):
            non_suicidal.append(move)

    print(non_suicidal)
    for (lib,att) in attack_points:
        if lib > bm_lib:
            bm_lib = lib
            for m in att:
                if m in non_suicidal:
                    my_move = m




print(my_move)
fout = open('output.txt','w')
if my_move == 'PASS':
    fout.write('PASS\n')
else:
    fout.write(str(my_move[0])+','+str(my_move[1])+'\n')
fout.close()