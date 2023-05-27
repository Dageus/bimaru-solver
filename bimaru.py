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
    
    def __init__(self, matrix, rows, columns):
        """Construtor da classe. Recebe como argumentos uma matriz que representa
        o tabuleiro, uma lista com os espaços preenchidos nas linhas, uma lista
        com os espaços preenchidos nas colunas e uma lista com o número de peças"""
        self.matrix = matrix
        self.rows = rows
        self.columns = columns

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.matrix[row][col] == ".":
            return None
        return self.matrix[row][col]
    
    def fill_ship_adjacent_values(self, row: int, col: int):
            """Preenche os valores adjacentes à peça com água."""
            #TODO
        
        #TODO adjacent values parra ate 4 para verificar se 2 hints formam o mm barco
        
    @staticmethod
    def adjacent_vertical_values(matrix: list, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        cell1 = matrix[row-1][col]
        cell2 = matrix[row+1][col]
        if matrix[row-1][col] == "." or row - 1 < 0:
            cell1 = None
        if matrix[row+1][col] == "." or row + 1 > 9:
            cell2 = None
        return cell1, cell2
    
    

    @staticmethod
    def adjacent_horizontal_values(matrix: list, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        cell1 = matrix[row][col-1]
        cell2 = matrix[row][col+1]
        if matrix[row][col-1] == "." or col - 1 < 0:
            cell1 = None
        if matrix[row][col+1] == "." or col + 1 > 9:
            cell2 = None
        return cell1, cell2
    
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
        return print(self.__str__())

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
        
        for i in range(num_hints):
            hint = stdin.readline()
            hint = hint.rstrip().split("\t")
            hint.pop(0)
            hint = [int(hint[0]), int(hint[1]), hint[2]]

            row = hint[0]
            col = hint[1]

            matrix[row][col] = hint[2]
            
            # preenchimento de água à volta da peça e possivel preenchimento de peça caso seja possível
            
            if hint[2] == TOP:
                
                matrix[row + 1][col] = UNDONE_BOAT
                
                if row - 1 >= 0:
                    matrix[row-1][col] = WATER
                if col - 1 >= 0:
                    matrix[row][col-1] = WATER
                    matrix[row + 1][col-1] = WATER
                    if row - 1 >= 0:
                        matrix[row-1][col-1] = WATER
                    if row + 2 <= 9:
                        matrix[row+2][col-1] = WATER
                if col + 1 <= 9: 
                    matrix[row][col+1] = WATER
                    matrix[row + 1][col+1] = WATER
                    if row - 1 >= 0:
                        matrix[row-1][col+1] = WATER 
                    if row + 2 <= 9:
                        matrix[row+2][col+1] = WATER
                    
            if hint[2] == BOTTOM:
                
                matrix[row - 1][col] = UNDONE_BOAT
                
                if row + 1 <= 9:
                    matrix[row+1][col] = WATER
                if col - 1 >= 0:
                    matrix[row][col-1] = WATER
                    matrix[row - 1][col-1] = WATER
                    if row + 1 <= 9: 
                        matrix[row+1][col-1] = WATER
                    if row - 2 >= 0:
                        matrix[row-2][col-1] = WATER
                if col + 1 <= 9:
                    matrix[row][col+1] = WATER
                    matrix[row - 1][col+1] = WATER
                    if row + 1 <= 9:
                        matrix[row+1][col+1] = WATER
                    if row - 2 >= 0:
                        matrix[row-2][col+1] = WATER
                    
            if hint[2] == CIRCLE:
                
                if row - 1 >= 0:
                    matrix[row-1][col] = WATER
                if row + 1 <= 9:
                    matrix[row+1][col] = WATER
                if col - 1 >= 0:
                    matrix[row][col-1] = WATER
                if col + 1 <= 9:
                    matrix[row][col+1] = WATER
                if row - 1 >= 0 and col - 1 >= 0:
                    matrix[row-1][col-1] = WATER
                if row - 1 >= 0 and col + 1 <= 9:
                    matrix[row-1][col+1] = WATER
                if row + 1 <= 9 and col - 1 >= 0:
                    matrix[row+1][col-1] = WATER
                if row + 1 <= 9 and col + 1 <= 9:
                    matrix[row+1][col+1] = WATER
                    
            if hint[2] == RIGHT:
                
                matrix[row][col - 1] = UNDONE_BOAT
                
                if row - 1 >= 0:
                    matrix[row-1][col] = WATER
                    matrix[row-1][col - 1] = WATER
                if row + 1 <= 9:
                    matrix[row+1][col] = WATER
                    matrix[row+1][col - 1] = WATER
                if col + 1 <= 9:
                    matrix[row][col+1] = WATER
                if row - 1 >= 0 and col + 1 <= 9:
                    matrix[row-1][col+1] = WATER
                if row + 1 <= 9 and col + 1 <= 9:
                    matrix[row+1][col+1] = WATER
                if row - 1 >= 0 and col - 2 >= 0:
                    matrix[row-1][col-2] = WATER
                if row + 1 <= 9 and col - 2 >= 0:
                    matrix[row+1][col-2] = WATER
                    
            if hint[2] == LEFT:
                
                matrix[row][col + 1] = UNDONE_BOAT
                
                if row - 1 >= 0:
                    matrix[row-1][col] = WATER
                    matrix[row-1][col + 1] = WATER
                if row + 1 <= 9:
                    matrix[row+1][col] = WATER
                    matrix[row+1][col + 1] = WATER
                if col - 1 >= 0:
                    matrix[row][col-1] = WATER
                if row - 1 >= 0 and col - 1 >= 0:
                    matrix[row-1][col-1] = WATER
                if row + 1 <= 9 and col - 1 >= 0:
                    matrix[row+1][col-1] = WATER
                if row - 1 >= 0 and col + 2 <= 9:
                    matrix[row-1][col+2] = WATER
                if row + 1 <= 9 and col + 2 <= 9:
                    matrix[row+1][col+2] = WATER
            
        # preenchimento de agua apos a colocacao de barcos e de mais barcos
            
        for i in range(0, 10):
            if columns[i] == 0:
                matrix[:,i] = WATER
            column = matrix[:,i]
            if np.count_nonzero((column == WATER) | (column == '.')) == 10 - columns[i]:
                for j in range(0, 10):
                    if matrix[j][i] == '.':
                        matrix[j][i] = WATER
                    if matrix[j][i] == UNDONE_BOAT:
                        #TODO
                        pass
                
        for i in range(0, 10):
            if rows[i] == 0:
                matrix[i] = WATER
            row = matrix[i]
            if np.count_nonzero((row == WATER) | (row == '.')) == 10 - rows[i]:
                for j in range(0, 10):
                    if matrix[i][j] == '.':
                        matrix[i][j] = WATER
                    if matrix[i][j] == UNDONE_BOAT:
                        #TODO
                        pass
        
        for i in range(10):
            for j in range(10):
                if np.count_nonzero((matrix[i] == WATER) | (matrix[i] == '.')) == 10 - rows[i]:
                    for k in range(10):
                        if matrix[i][k] == '.':
                            matrix[i][k] = WATER
                if np.count_nonzero((matrix[i] == WATER)) == 10 - rows[i]:
                    for k in range(10):
                        if matrix[i][k] == '.':
                            matrix[i][k] = UNDONE_BOAT
                if np.count_nonzero((matrix[:,i] == WATER)) == 10 - columns[i]:
                    for k in range(10):
                        if matrix[k][i] == '.':
                            matrix[k][i] = UNDONE_BOAT
                if np.count_nonzero((matrix[:,i] == WATER) | (matrix[:,i] == '.')) == 10 - columns[i]:
                    for k in range(10):
                        if matrix[k][i] == '.':
                            matrix[k][i] = WATER
                if matrix[i][j] == MIDDLE:
                    adjacent_values = Board.adjacent_horizontal_values(matrix, i, j)
                    if adjacent_values[0] != WATER and adjacent_values[1] != WATER:
                        matrix[i][j - 1] = UNDONE_BOAT
                        matrix[i][j + 1] = UNDONE_BOAT
                        # preencher espaço à volta com água
                        matrix[i - 1][j - 1] = WATER
                        matrix[i - 1][j + 1] = WATER
                        matrix[i + 1][j] = WATER
                        matrix[i - 1][j] = WATER
                        if i + 2 <= 9:
                            matrix[i + 2][j + 1] = WATER
                            matrix[i + 2][j - 1] = WATER
                        if i - 2 >= 0:
                            matrix[i - 2][j + 1] = WATER
                            matrix[i - 2][j - 1] = WATER
                    adjacent_values = Board.adjacent_vertical_values(matrix, i, j)
                    if adjacent_values[0] != WATER and adjacent_values[1] != WATER:
                        matrix[i - 1][j] = UNDONE_BOAT
                        matrix[i + 1][j] = UNDONE_BOAT
                        # preencher espaço à volta com água
                        matrix[i - 1][j - 1] = WATER
                        matrix[i - 1][j + 1] = WATER
                        matrix[i][j + 1] = WATER
                        matrix[i][j - 1] = WATER
                        matrix[i + 1][j - 1] = WATER
                        matrix[i + 1][j + 1] = WATER
                        if i + 2 <= 9:
                            matrix[i + 2][j + 1] = WATER
                            matrix[i + 2][j - 1] = WATER
                        if i - 2 >= 0:
                            matrix[i - 2][j + 1] = WATER
                            matrix[i - 2][j - 1] = WATER
                    if np.count_nonzero((matrix[i] == WATER) | (matrix[i] == '.')) == 10 - rows[i]:
                        for k in range(0, 10):
                            if matrix[i][k] == '.':
                                matrix[i][k] = WATER
        
        
        
        return Board(matrix, rows, columns)

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        #TODO add more attributes

    def is_valid_vertical_action(self, board, row, col):
        """Verifica se colocar uma parte de barco na vertical na posição dada é válido"""

        tuple_cells = self.board.adjacent_vertical_values(board, row, col)
        

        if tuple_cells[0] == WATER and tuple_cells[1] == WATER:
            return True
    
        return False

    def is_valid_horizontal_action(self, board, row, col):
        """Verifica se colocar uma parte de barco na horizontal na posição dada é válido"""
        
        tuple_cells = self.board.adjacent_horizontal_values(board, row, col)
        
        
        if tuple_cells[0] == WATER and tuple_cells[1] == WATER:
            return True
        
        return False


    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        board = state.board
        actions = []
        for row in range(len(10)):
            for col in range(len(10)):
                if board.get_value(row, col) == '.':
                    # ver se encaixa na vertical
                    if self.is_valid_vertical_action(board, row, col):
                        actions.append((row, col, VERTICAL))
                    # ver se encaixa na horizontal
                    if self.is_valid_horizontal_action(board, row, col):
                        actions.append((row, col, HORIZONTAL))
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        # inicialmente assumimos que a ação é válida e preenche um espaço vazio
        
        # action = (row, col, value)
        
        if state.board.get_value(action[0], action[1]) != ".":
            return None
        else:
            state.board.matrix[action[0]][action[1]] = action[2]
        return BimaruState(state.board) 

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        for i in range(10):
            for j in range(10):
                
                pass
                    
                

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe
    

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    board = Board.parse_instance()
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    print(str(board))