# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 103808 João Miguel Nogueira
# 103465 João Rocha

HINT_WATER = "W"
WATER   = "."
EMPTY_SPACE = "!"
UNDONE_BOAT = "1"
CIRCLE  = "C"
TOP     = "T"
MIDDLE  = "M"
BOTTOM  = "B"
LEFT    = "L"
RIGHT   = "R"

HORIZONTAL = 0
VERTICAL = 1

#          1x1  2x1  3x1  4x1
PIECES = [  4 ,  3 ,  2 ,  1  ]

import sys
from sys import stdin
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    
    """Representação interna de um tabuleiro de Bimaru.""" 
    
    def __init__(self, matrix, rows, columns, hints):
        """Construtor da classe. Recebe como argumentos uma matriz que representa
        o tabuleiro, uma lista com os espaços preenchidos nas linhas, uma lista
        com os espaços preenchidos nas colunas e uma lista com o número de peças"""
        self.matrix = matrix
        self.rows = rows
        self.columns = columns
        self.hints = hints
        self.pieces = PIECES

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.matrix[row][col] == ".":
            return None
        return self.matrix[row][col]
    
    #TODO adjacent values parra ate 4 para verificar se 2 hints formam o mm barco
        
    def adjacent_vertical_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        cell1 = self.matrix[row-1][col]
        cell2 = self.matrix[row+1][col]
        if self.matrix[row-1][col] == "." or row - 1 < 0:
            cell1 = None
        if self.matrix[row+1][col] == "." or row + 1 > 9:
            cell2 = None
        return cell1, cell2
    

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        cell1 = self.matrix[row][col-1]
        cell2 = self.matrix[row][col+1]
        if self.matrix[row][col-1] == "." or col - 1 < 0:
            cell1 = None
        if self.matrix[row][col+1] == "." or col + 1 > 9:
            cell2 = None
        return cell1, cell2

    def adjacent_diagonal1_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        cell1 = self.matrix[row-1][col-1]
        cell2 = self.matrix[row+1][col+1]
        if self.matrix[row-1][col-1] == "." or row - 1 < 0 or col - 1 < 0:
            cell1 = None
        if self.matrix[row+1][col+1] == "." or row + 1 > 9 or col + 1 > 9:
            cell2 = None
        return cell1, cell2

    def adjacent_diagonal2_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        cell1 = self.matrix[row-1][col+1]
        cell2 = self.matrix[row+1][col-1]
        if self.matrix[row-1][col+1] == "." or row - 1 < 0 or col + 1 > 9:
            cell1 = None
        if self.matrix[row+1][col-1] == "." or row + 1 > 9 or col - 1 < 0:
            cell2 = None
        return cell1, cell2

    def adjacent_values(self, row: int, col: int) -> tuple: 
        """Devolve os valores imediatamente acima, abaixo, à esquerda e à direita,
        respectivamente."""
        return \
        self.adjacent_vertical_values(row, col) + \
        self.adjacent_horizontal_values(row, col) + \
        self.adjacent_diagonal1_values(row, col) + \
        self.adjacent_diagonal2_values(row, col)

        
    def __str__(self):
        """Devolve uma string que representa o tabuleiro."""
        
        str_ = ""
        
        i = 0
        
        for rows in self.matrix:
            for col in rows:
                str_ += col + " "
            str_ += str(self.rows[i]) + "\n"
            i+=1
        
        for elem in self.columns:
            str_ += str(elem) + " "
        str_ += "\n"
        return str_
    
    def print(self):
        """Imprime o tabuleiro."""
        return self.__str__()

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        
        matrix = np.full((10, 10), "!")
        
        rows = stdin.readline()
        rows = rows.rstrip().split("\t")
        rows.pop(0)
        rows = [int(i) for i in rows]
        
        columns = stdin.readline()
        columns = columns.rstrip().split("\t")
        columns.pop(0)
        columns = [int(i) for i in columns]
        
        num_hints = int(stdin.readline())
        
        hints = []
        
        for _ in range(num_hints):
            hint = stdin.readline()
            hint = hint.rstrip().split("\t")
            hint.pop(0)
            hint = [int(hint[0]), int(hint[1]), hint[2]]
            
            hints += [hint]

            row = hint[0]
            col = hint[1]

            matrix[row][col] = hint[2]
            
            # retirar 1 ao valor da linha e da coluna
            
            rows[row] -= 1
            columns[col] -= 1
        
        return Board(matrix, rows, columns, hints)

    def post_parse(self):
        """Preenche os valores adjacentes às peças com água."""
        
        for hint in self.hints:
            
            row = hint[0]
            col = hint[1]
        
            if hint[2] == TOP:
                
                self.matrix[row + 1][col] = UNDONE_BOAT
                
                # retirar 1 ao valor da linha e da coluna
                
                self.rows[row] -= 1
                self.columns[col] -= 1
                
                if row - 1 >= 0:
                    self.matrix[row-1][col] = WATER
                if col - 1 >= 0:
                    self.matrix[row][col-1] = WATER
                    self.matrix[row + 1][col-1] = WATER
                    if row - 1 >= 0:
                        self.matrix[row-1][col-1] = WATER
                    if row + 2 <= 9:
                        self.matrix[row+2][col-1] = WATER
                if col + 1 <= 9: 
                    self.matrix[row][col+1] = WATER
                    self.matrix[row + 1][col+1] = WATER
                    if row - 1 >= 0:
                        self.matrix[row-1][col+1] = WATER 
                    if row + 2 <= 9:
                        self.matrix[row+2][col+1] = WATER
                    
            if hint[2] == BOTTOM:
                
                self.matrix[row - 1][col] = UNDONE_BOAT
                
                # retirar 1 ao valor da linha e da coluna
                
                self.rows[row] -= 1
                self.columns[col] -= 1
                
                if row + 1 <= 9:
                    self.matrix[row+1][col] = WATER
                if col - 1 >= 0:
                    self.matrix[row][col-1] = WATER
                    self.matrix[row - 1][col-1] = WATER
                    if row + 1 <= 9: 
                        self.matrix[row+1][col-1] = WATER
                    if row - 2 >= 0:
                        self.matrix[row-2][col-1] = WATER
                if col + 1 <= 9:
                    self.matrix[row][col+1] = WATER
                    self.matrix[row - 1][col+1] = WATER
                    if row + 1 <= 9:
                        self.matrix[row+1][col+1] = WATER
                    if row - 2 >= 0:
                        self.matrix[row-2][col+1] = WATER
                    
            if hint[2] == CIRCLE:
                
                if row - 1 >= 0:
                    self.matrix[row-1][col] = WATER
                if row + 1 <= 9:
                    self.matrix[row+1][col] = WATER
                if col - 1 >= 0:
                    self.matrix[row][col-1] = WATER
                if col + 1 <= 9:
                    self.matrix[row][col+1] = WATER
                if row - 1 >= 0 and col - 1 >= 0:
                    self.matrix[row-1][col-1] = WATER
                if row - 1 >= 0 and col + 1 <= 9:
                    self.matrix[row-1][col+1] = WATER
                if row + 1 <= 9 and col - 1 >= 0:
                    self.matrix[row+1][col-1] = WATER
                if row + 1 <= 9 and col + 1 <= 9:
                    self.matrix[row+1][col+1] = WATER
                    
            if hint[2] == RIGHT:
                
                self.matrix[row][col - 1] = UNDONE_BOAT
                
                # retirar 1 ao valor da linha e da coluna
                
                self.rows[row] -= 1
                self.columns[col] -= 1
                
                if row - 1 >= 0:
                    self.matrix[row-1][col] = WATER
                    self.matrix[row-1][col - 1] = WATER
                if row + 1 <= 9:
                    self.matrix[row+1][col] = WATER
                    self.matrix[row+1][col - 1] = WATER
                if col + 1 <= 9:
                    self.matrix[row][col+1] = WATER
                if row - 1 >= 0 and col + 1 <= 9:
                    self.matrix[row-1][col+1] = WATER
                if row + 1 <= 9 and col + 1 <= 9:
                    self.matrix[row+1][col+1] = WATER
                if row - 1 >= 0 and col - 2 >= 0:
                    self.matrix[row-1][col-2] = WATER
                if row + 1 <= 9 and col - 2 >= 0:
                    self.matrix[row+1][col-2] = WATER
                    
            if hint[2] == LEFT:
                
                self.matrix[row][col + 1] = UNDONE_BOAT
                
                # retirar 1 ao valor da linha e da coluna
                
                self.rows[row] -= 1
                self.columns[col] -= 1
                
                if row - 1 >= 0:
                    self.matrix[row-1][col] = WATER
                    self.matrix[row-1][col + 1] = WATER
                if row + 1 <= 9:
                    self.matrix[row+1][col] = WATER
                    self.matrix[row+1][col + 1] = WATER
                if col - 1 >= 0:
                    self.matrix[row][col-1] = WATER
                if row - 1 >= 0 and col - 1 >= 0:
                    self.matrix[row-1][col-1] = WATER
                if row + 1 <= 9 and col - 1 >= 0:
                    self.matrix[row+1][col-1] = WATER
                if row - 1 >= 0 and col + 2 <= 9:
                    self.matrix[row-1][col+2] = WATER
                if row + 1 <= 9 and col + 2 <= 9:
                    self.matrix[row+1][col+2] = WATER
            
        # preenchimento de agua apos a colocacao de barcos e de mais barcos
          
        stop = False
        
        while not stop:
            
            copy = np.copy(self.matrix)
            
            for i in range(10):
                if self.columns[i] == 0:
                    self.matrix[:,i] = WATER
                column = self.matrix[:,i]
                non_zeros = np.nonzero((column == TOP) | (column == BOTTOM) | (column == CIRCLE) | (column == UNDONE_BOAT))
                if non_zeros[0].size == self.columns[i]:
                    for j in range(0, 10):
                        if self.matrix[j][i] == EMPTY_SPACE:
                            self.matrix[j][i] = WATER
                        if self.matrix[j][i] == UNDONE_BOAT:
                            #TODO
                            pass
                    
            for i in range(10):
                if self.rows[i] == 0:
                    self.matrix[i] = WATER
                row = self.matrix[i]
                non_zeros = np.nonzero((row == LEFT) | (row == RIGHT) | (row == CIRCLE) | (row == UNDONE_BOAT))
                if non_zeros[0].size == self.rows[i]:
                    for j in range(0, 10):
                        if self.matrix[i][j] == EMPTY_SPACE:
                            self.matrix[i][j] = WATER
                        if self.matrix[i][j] == UNDONE_BOAT:
                            #TODO
                            pass
            
            
            for i in range(10):
                # verificar linhas
                if np.count_nonzero((self.matrix[i] == WATER) | (self.matrix[i] == EMPTY_SPACE) | (self.matrix[i] == HINT_WATER)) == 10 - self.rows[i]:
                    for k in range(10):
                        if self.matrix[i][k] == EMPTY_SPACE:
                            self.matrix[i][k] = WATER
                # verificar colunas              
                if np.count_nonzero((self.matrix[:,i] == WATER) | (self.matrix[:,i] == EMPTY_SPACE) | (self.matrix[:,i] == HINT_WATER)) == 10 - self.columns[i]:
                    for k in range(10):
                        if self.matrix[k][i] == EMPTY_SPACE:
                            self.matrix[k][i] = WATER
                middle_index = np.nonzero((self.matrix[i] == MIDDLE))
                if middle_index[0].size > 0:
                    middle_index = middle_index[0][0]
                    
                    # verificar horizontalmente
                    
                    adjacent_values = self.adjacent_horizontal_values(i, middle_index)
                    if adjacent_values[0] != WATER and adjacent_values[1] != WATER:
                        # preencher em cada lado com uma peça de um barco
                        self.matrix[i][middle_index - 1] = UNDONE_BOAT
                        self.matrix[i][middle_index + 1] = UNDONE_BOAT
                        # preencher espaço à volta com água
                        self.matrix[i - 1][middle_index - 1] = WATER
                        self.matrix[i - 1][middle_index + 1] = WATER
                        self.matrix[i + 1][middle_index] = WATER
                        self.matrix[i - 1][middle_index] = WATER
                        self.matrix[i + 1][middle_index + 1] = WATER
                        self.matrix[i + 1][middle_index - 1] = WATER
                        # verificar se há espaço extra para as bordas do barco
                        if i + 2 <= 9:
                            self.matrix[i + 2][middle_index + 1] = WATER
                            self.matrix[i + 2][middle_index - 1] = WATER
                        if i - 2 >= 0:
                            self.matrix[i - 2][middle_index + 1] = WATER
                            self.matrix[i - 2][middle_index - 1] = WATER
                    
                    # verificar verticalmente
                            
                    adjacent_values = self.adjacent_vertical_values(i, middle_index)
                    if adjacent_values[0] != WATER and adjacent_values[1] != WATER:
                        # preencher em cima e em baixo com a peça de um barco
                        self.matrix[i - 1][middle_index] = UNDONE_BOAT
                        self.matrix[i + 1][middle_index] = UNDONE_BOAT
                        # preencher espaço à volta com água
                        self.matrix[i - 1][middle_index - 1] = WATER
                        self.matrix[i - 1][middle_index + 1] = WATER
                        self.matrix[i][middle_index + 1] = WATER
                        self.matrix[i][middle_index - 1] = WATER
                        self.matrix[i + 1][middle_index - 1] = WATER
                        self.matrix[i + 1][middle_index + 1] = WATER
                        # verificar se há espaço extra para as bordas do barco
                        if i + 2 <= 9:
                            self.matrix[i + 2][middle_index + 1] = WATER
                            self.matrix[i + 2][middle_index - 1] = WATER
                        if i - 2 >= 0:
                            self.matrix[i - 2][middle_index + 1] = WATER
                            self.matrix[i - 2][middle_index - 1] = WATER
                            
            print(self.matrix, "\nvs.\n", copy)
            
            stop = True #np.array_equal(copy, self.matrix)
        
        return self


    def count_boats(self):
        """Retorna o maior barco que ainda não foi colocado"""
        boats={1:4, 2:3, 3:2, 4:1}
        badbad = (WATER,  WATER)
        for row in range(0, 10):
            for col in range(0, 10):
                count = 1
                if self.matrix[row][col] == TOP:
                    for i in range(0, 10):
                        if self.matrix[row + i][col] not in badbad:
                            count += 1
                        if self.matrix[row + i][col] == BOTTOM:
                            boats[count] -= 1
                            break
                elif self.matrix[row][col] == LEFT:
                    for i in range(0, 10):
                        if self.matrix[row][col + i] not in badbad:
                            count += 1
                        if self.matrix[row][col + i] == RIGHT:
                            boats[count] -= 1
                            break
        for i in range(4,0,-1):
            if boats[i] != 0:
                return i
        return 0


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board

    def is_valid_position(self, row, col, boat_size, orientation):
        """Verifica se colocar uma parte de barco na horizontal na posição dada é válido"""
        count = 0
        
        if board[row][col] == WATER or board[row][col] == HINT_WATER:
            return False
      
         
        if (orientation == HORIZONTAL):
            if (self.board[row][col] == LEFT):
                count += 1
            elif (self.board[row][col] == EMPTY_SPACE):

                if self.board.columns[col] < 1:
                    return False
            else:
                return False
                
            for i in range(col +_1, col + boat_size - 1):
                if (self.board[row][i] == EMPTY_SPACE):
                    if self.board.columns[i] < 1:
                        return False
                elif (self.board[row][i] == MIDDLE):
                    count += 1
                else:
                    return False
                if self.board.adjacent_vertical_values(row, i)[0]  not in (WATER, HINT_WATER, EMPTY_SPACE):
                    return False
                if self.board.adjacent_vertical_values(row, i)[1]  not in (WATER, HINT_WATER, EMPTY_SPACE):
                    return False
                
            if (self.board[row][col + boat_size - 1] == RIGHT):
                count += 1
            elif (self.board[row][col + boat_size - 1] == EMPTY_SPACE):
                if self.board.columns[col + boat_size - 1] < 1:
                    return False
                
            if self.board.rows[row] < boat_size - count:
                return False 

        if (self.board[row][col] == LEFT):
            if  tuple_cells[3] == EMPTY_SPACE or tuple_cells[3] == MIDDLE :
                return True
        
    # (cima, baixo, esquerda, direita, esquedra_cima, direita_baixo, direita_cima, esquerda_baixo)
    
        if (self.board[row][col] == MIDDLE):
            if (tuple_cells[0] == TOP and tuple_cells[1] == EMPTY_SPACE) or \
            (tuple_cells[0] == MIDDLE and tuple_cells[1] == EMPTY_SPACE) or \
            (tuple_cells[1] == BOTTOM and tuple_cells[0] == EMPTY_SPACE) or \
            (tuple_cells[1] == MIDDLE and tuple_cells[0] == EMPTY_SPACE) or \
            (tuple_cells[2] == MIDDLE and tuple_cells[3] == EMPTY_SPACE) or \
            (tuple_cells[2] == LEFT and tuple_cells[3] == EMPTY_SPACE) or \
            (tuple_cells[3] == RIGHT and tuple_cells[2] == EMPTY_SPACE) or \
            (tuple_cells[3] == MIDDLE and tuple_cells[2] == EMPTY_SPACE) or \
            (tuple_cells[0] == EMPTY_SPACE and tuple_cells[1] == EMPTY_SPACE) or \
            (tuple_cells[2] == EMPTY_SPACE and tuple_cells[3] == EMPTY_SPACE):
                return True
        
        if (self.board[row][col] == TOP):   
            if  tuple_cells[1] == EMPTY_SPACE or tuple_cells[1] == MIDDLE :
                return True


        return False


    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        # IMPORTANT:
        
        # formato da ação: (cell_1, cell_2, boat_size, orientação)
        
        board = state.board
        actions = []
        boat_size = board.count_boats()
        count = 0
        for row in range(10):
            for col in range(10):
                if not self.is_valid_position(board, row, col, boat_size, HORIZONTAL):
                    count = 0
                else:
                    count += 1
                    if count == boat_size:
                        actions.append((row, col, boat_size, HORIZONTAL))
                        count = 0	
        for col in range(10):
            for row in range(10):
                if not self.is_valid_position(board, row, col, boat_size, VERTICAL):
                    count = 0
                else:
                    count += 1
                    if count == boat_size:
                        actions.append((row, col, boat_size, VERTICAL))
                        count = 0
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        # action = (row, col, boat_size, orientation)
        
        if(action[3] == HORIZONTAL):
            if(action[2] == 1):
                self.board.matrix[action[0]][action[1]] = MIDDLE
            elif(action[2] == 2):
                self.board.matrix[action[0]][action[1]] = LEFT
                self.board.matrix[action[0]][action[1] + 1] = RIGHT
            elif(action[2] == 3):
                self.board.matrix[action[0]][action[1]] = LEFT
                self.board.matrix[action[0]][action[1] + 1] = MIDDLE
                self.board.matrix[action[0]][action[1] + 2] = RIGHT
            elif(action[2] == 4):
                self.board.matrix[action[0]][action[1]] = LEFT
                self.board.matrix[action[0]][action[1] + 1] = MIDDLE
                self.board.matrix[action[0]][action[1] + 2] = MIDDLE
                self.board.matrix[action[0]][action[1] + 3] = RIGHT
        
        elif(action[3] == VERTICAL):
            if(action[2] == 1):
                self.board.matrix[action[0]][action[1]] = MIDDLE
            elif(action[2] == 2):
                self.board.matrix[action[0]][action[1]] = TOP
                self.board.matrix[action[0] + 1][action[1]] = BOTTOM
            elif(action[2] == 3):
                self.board.matrix[action[0]][action[1]] = TOP
                self.board.matrix[action[0] + 1][action[1]] = MIDDLE
                self.board.matrix[action[0] + 2][action[1]] = BOTTOM
            elif(action[2] == 4):
                self.board.matrix[action[0]][action[1]] = TOP
                self.board.matrix[action[0] + 1][action[1]] = MIDDLE
                self.board.matrix[action[0] + 2][action[1]] = MIDDLE
                self.board.matrix[action[0] + 3][action[1]] = BOTTOM
        
        
        # state.board.matrix[action[0]][action[1]] = action[2]
        
        # # ver se ao colocar a peça, o barco fica completo
        
        # column = state.board.matrix[:, action[1]]
        # row = state.board.matrix[action[0]]
        
        # non_zeros = np.nonzero((column == TOP) | (column == BOTTOM) | (column == UNDONE_BOAT) | (column == MIDDLE))
        # if len(non_zeros) == state.board.columns[action[1]]:
        #     # a ideia aqui era ver se se pode retirar alguma das peças das que faltam completar, mas nao sei se esta certo
        #     pass
            
        # non_zeros = np.nonzero((row == LEFT) | (row == RIGHT) | (row == UNDONE_BOAT) | (row == MIDDLE))
        # if len(non_zeros) == state.board.rows[action[0]]:
        #     # a ideia aqui era ver se se pode retirar alguma das peças das que faltam completar, mas nao sei se esta certo
        #     pass
        
        return BimaruState(state.board) 

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        matrix = state.board.matrix
        
        if not np.any(state.board.pieces) or not np.any(state.board.rows) or not np.any(state.board.columns):
            return False

        return True
                

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return -node.depth*2
    

if __name__ == "__main__":
    
    board = Board.parse_instance()
    
    board = Board.post_parse(board)
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    initial_state = BimaruState(board)
    
    print(initial_state.board.print())