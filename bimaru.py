# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 103808 João Miguel Nogueira
# 10____ João Rocha

WATER   = "W"
UNDONE_BOAT = "1"
CIRCLE  = "C"
TOP     = "T"
MIDDLE  = "M"
BOTTOM  = "B"
LEFT    = "L"
RIGHT   = "R"

CIRCLE_INDEX = 0
SMALL_BOAT_INDEX = 1
MEDIUM_BOAT_INDEX = 2
BIG_BOAT_INDEX = 3

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
        
        matrix = np.full((10, 10), ".")
        
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
        
        for i in range(num_hints):
            hint = stdin.readline()
            hint = hint.rstrip().split("\t")
            hint.pop(0)
            hint = [int(hint[0]), int(hint[1]), hint[2]]
            
            hints += [hint]

            row = hint[0]
            col = hint[1]

            matrix[row][col] = hint[2]
        
        return Board(matrix, rows, columns, hints)

    def post_parse(self):
        """Preenche os valores adjacentes às peças com água."""
        # preenchimento de água à volta da peça e possivel preenchimento de peça caso seja possível
        
        for hint in self.hints:
            
            row = hint[0]
            col = hint[1]
        
            if hint[2] == TOP:
                
                self.matrix[row + 1][col] = UNDONE_BOAT
                
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
            
        for i in range(0, 10):
            if self.columns[i] == 0:
                self.matrix[:,i] = WATER
            column = self.matrix[:,i]
            non_zeros = np.nonzero((column == TOP) | (column == BOTTOM) | (column == CIRCLE) | (column == UNDONE_BOAT))
            print("non zeros for column {}: ".format(i), non_zeros)
            if np.count_nonzero((column == ".") | (column == WATER)) == 10 - self.columns[i]:
                for j in range(0, 10):
                    if self.matrix[j][i] == '.':
                        self.matrix[j][i] = WATER
                    if self.matrix[j][i] == UNDONE_BOAT:
                        #TODO
                        pass
                
        for i in range(0, 10):
            if self.rows[i] == 0:
                self.matrix[i] = WATER
            row = self.matrix[i]
            non_zeros = np.nonzero((row == LEFT) | (row == RIGHT) | (row == CIRCLE) | (row == UNDONE_BOAT))
            print("non zeros for row {}: ".format(i), non_zeros)
            if np.count_nonzero((row == ".") | (row == WATER)) == 10 - self.rows[i]:
                for j in range(0, 10):
                    if self.matrix[i][j] == '.':
                        self.matrix[i][j] = WATER
                    if self.matrix[i][j] == UNDONE_BOAT:
                        #TODO
                        pass
                    
        # IMPORTANT: cenas extra
        
        # for i in range(10):
        #     for j in range(10):
        #         if np.count_nonzero((self.matrix[i] == WATER) | (matrix[i] == '.')) == 10 - rows[i]:
        #             for k in range(10):
        #                 if matrix[i][k] == '.':
        #                     matrix[i][k] = WATER
        #         if np.count_nonzero((matrix[i] == WATER)) == 10 - rows[i]:
        #             for k in range(10):
        #                 if matrix[i][k] == '.':
        #                     matrix[i][k] = UNDONE_BOAT
        #         if np.count_nonzero((matrix[:,i] == WATER)) == 10 - columns[i]:
        #             for k in range(10):
        #                 if matrix[k][i] == '.':
        #                     matrix[k][i] = UNDONE_BOAT
        #         if np.count_nonzero((matrix[:,i] == WATER) | (matrix[:,i] == '.')) == 10 - columns[i]:
        #             for k in range(10):
        #                 if matrix[k][i] == '.':
        #                     matrix[k][i] = WATER
        #         if matrix[i][j] == MIDDLE:
        #             adjacent_values = Board.adjacent_horizontal_values(matrix, i, j)
        #             if adjacent_values[0] != WATER and adjacent_values[1] != WATER:
        #                 matrix[i][j - 1] = UNDONE_BOAT
        #                 matrix[i][j + 1] = UNDONE_BOAT
        #                 # preencher espaço à volta com água
        #                 matrix[i - 1][j - 1] = WATER
        #                 matrix[i - 1][j + 1] = WATER
        #                 matrix[i + 1][j] = WATER
        #                 matrix[i - 1][j] = WATER
        #                 if i + 2 <= 9:
        #                     matrix[i + 2][j + 1] = WATER
        #                     matrix[i + 2][j - 1] = WATER
        #                 if i - 2 >= 0:
        #                     matrix[i - 2][j + 1] = WATER
        #                     matrix[i - 2][j - 1] = WATER
        #             adjacent_values = Board.adjacent_vertical_values(matrix, i, j)
        #             if adjacent_values[0] != WATER and adjacent_values[1] != WATER:
        #                 matrix[i - 1][j] = UNDONE_BOAT
        #                 matrix[i + 1][j] = UNDONE_BOAT
        #                 # preencher espaço à volta com água
        #                 matrix[i - 1][j - 1] = WATER
        #                 matrix[i - 1][j + 1] = WATER
        #                 matrix[i][j + 1] = WATER
        #                 matrix[i][j - 1] = WATER
        #                 matrix[i + 1][j - 1] = WATER
        #                 matrix[i + 1][j + 1] = WATER
        #                 if i + 2 <= 9:
        #                     matrix[i + 2][j + 1] = WATER
        #                     matrix[i + 2][j - 1] = WATER
        #                 if i - 2 >= 0:
        #                     matrix[i - 2][j + 1] = WATER
        #                     matrix[i - 2][j - 1] = WATER
        #             if np.count_nonzero((matrix[i] == WATER) | (matrix[i] == '.')) == 10 - rows[i]:
        #                 for k in range(0, 10):
        #                     if matrix[i][k] == '.':
        #                         matrix[i][k] = WATER
        
        return self


    def count_boats(self):
        """Retorna o maior barco que ainda não foi colocado"""
        boats={1:4, 2:3, 3:2, 4:1}
        badbad = (WATER,  '.')
        for row in range(0, 10):
            for col in range(0, 10):
                count = 1
                if self.board[row][col] == TOP:
                    for i in range(0, 10):
                        if self.board[row + i][col] not in badbad:
                            count += 1
                        if self.board[row + i][col] == BOTTOM:
                            boats[count] -= 1
                            break
                elif self.board[row][col] == LEFT:
                    for i in range(0, 10):
                        if self.board[row][col + i] not in badbad:
                            count += 1
                        if self.board[row][col + i] == RIGHT:
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
        #TODO add more attributes


    def is_valid_position(self, board, row, col):
        """Verifica se colocar uma parte de barco na horizontal na posição dada é válido"""
        
        tuple_cells = self.board.adjacent_values(board, row, col)

        if (self.board[row][col] = LEFT)
            if tuple_cells[0] == WATER and tuple_cells[1] == WATER and tuple_cells[2] == WATER and tuple_cells[3] == '.':
                return True
        
        if tuple_cells[0] == WATER and tuple_cells[1] == WATER:
            return True
        
        return False

# (cima, baixo, esquerda, direita, esquedra_cima, direita_baixo, direita_cima, esquerda_baixo)
    

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        # IMPORTANT:
        
        # formato da ação: (cell_1, cell_2, boat_size)
        
        board = state.board
        actions = []
        boat_size = board.count_boats()
        count = 0
        for row in range(10):
            for col in range(10):
                if (is_valid_position(board, row, col)):
                    count += 1



                
        
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        # action = (row, col, value)
        
        if state.board.get_value(action[0], action[1]) != None and state.board.get_value(action[0], action[1]) != WATER:
            return None
        else:
            state.board.matrix[action[0]][action[1]] = action[2]
        return BimaruState(state.board) 

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        matrix = state.board.matrix
        
        for i in range(10):
            for j in range(10):
                pass
                    
        return True
                

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    

if __name__ == "__main__":
    
    board = Board.parse_instance()
    
    board = Board.post_parse(board)
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    initial_state = BimaruState(board)
    # Mostrar valor na posição (3, 3):
    print(initial_state.board.get_value(3, 3))
    # Realizar acção de inserir o valor w (água) na posição da linha 3 e coluna 3
    result_state = problem.result(initial_state, (3, 3, 'w'))
    # Mostrar valor na posição (3, 3):
    print(result_state.board.get_value(3, 3))
    
    print(result_state.board.print())