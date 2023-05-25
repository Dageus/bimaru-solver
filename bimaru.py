# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 103808 João Miguel Nogueira
# 10____ João Rocha

WATER   = "W"
CIRCLE  = "C"
TOP     = "T"
MIDDLE  = "M"
BOTTOM  = "B"
LEFT    = "L"
RIGHT   = "R"

#          1x1  2x1  3x1  4x1
PIECES = [  4 ,  3 ,  2 ,  1  ]


"""
Sets:

Note the following data:
• Gridsl consists of the grids in which one ship of
length l is located and is a subset of the overall set
gridsall.
• Gridsall consists of all grids in which one ship is
located where each grid is numbered.
It is the union of the grids in gridsl (i.e., U(l) grids(l)). 
A particular grid is denoted by g, 
where g ∈ {1,...,N}; N denotes the last grid.
"""

"""

Basear projeto no ship based model, aka reformular isto tudo

"""

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

    def adjacent_vertical_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        cell1 = self.matrix[row-1][col]
        cell2 = self.matrix[row+1][col]
        if self.matrix[row-1][col] == "." or self.matrix[row-1][col] == "W" or row - 1 < 0:
            cell1 = None
        if self.matrix[row+1][col] == "." or self.matrix[row+1][col] == "W" or row + 1 > 9:
            cell2 = None
        return cell1, cell2
    
    def fill_ship_adjacent_values(self, row: int, col: int):
        """Preenche os valores adjacentes à peça com água."""
        #TODO
    
    #TODO adjacent values parra ate 4 para verificar se 2 hints formam o mm barco

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        cell1 = self.matrix[row][col-1]
        cell2 = self.matrix[row][col+1]
        if self.matrix[row][col-1] == "." or self.matrix[row][col-1] == "W" or col - 1 < 0:
            cell1 = None
        if self.matrix[row][col+1] == "." or self.matrix[row][col+1] == "W" or col + 1 > 9:
            cell2 = None
        return cell1, cell2
    
    def __str__(self):
        """Devolve uma string que representa o tabuleiro."""
        str = ""
        
        for rows in self.matrix:
            for col in rows:
                str += col
            str += "\n"
        return str
    
    def print(self):
        """Imprime o tabuleiro."""
        return self.__str__()

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        
        matrix = np.full((10, 10), 100)
        
        rows = stdin.readline()
        rows = rows.rstrip().split(" ")
        rows.pop(0)
        rows = [int(i) for i in rows]
        
        columns = stdin.readline()
        columns = columns.rstrip().split(" ")
        columns.pop(0)
        columns = [int(i) for i in columns]
        
        num_hints = int(stdin.readline())
        
        for i in range(num_hints):
            hint = stdin.readline()
            hint = hint.rstrip().split(" ")
            hint.pop(0)
            hint = [int(hint[0]), int(hint[1]), hint[2]]
            matrix[hint[0]][hint[1]] = hint[2]
            
            # preenchimento de água à volta da peça e possivel preenchimento de peça caso seja possível
            
            if hint[2] == TOP:
                if hint[0] - 1 >= 0:
                    matrix[hint[0]-1][hint[1]] = WATER
            
        for i in columns:
            if columns[i] == 0:
                matrix[i] = 0
            if np.count_nonzero(matrix[i]) == columns[i]:
                columns[i] = 0
                matrix[i] = 0
                
        for i in rows:
            if rows[i] == 0:
                matrix[:,i] = 0
            if np.count_nonzero(matrix[:,i]) == rows[i]:
                rows[i] = 0
                matrix[:,i] = 0
        
        return Board(matrix, rows, columns)

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        #TODO add more attributes

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        board = state.board
        actions = []
        while True:
            #TODO
            break

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
        #TODO
                    
                

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
    
    ok big discovery, meter todos os barcos que matematicamente consigo calcular,
    e so depois é que vou começar a ir buscar uma posição random e a partir dai 
    fazer procuras com base numa heuristica