# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 103808 João Miguel Nogueira
# 103465 João Rocha

EMPTY_SPACE = "!"
UNDONE_BOAT = "O"

HINT_WATER  = "W"
HINT_CIRCLE = "C"
HINT_TOP    = "T"
HINT_MIDDLE = "M"
HINT_BOTTOM = "B"
HINT_LEFT   = "L"
HINT_RIGHT  = "R"

WATER       = "."
CIRCLE      = "c"
TOP         = "t"
MIDDLE      = "m"
BOTTOM      = "b"
LEFT        = "l"
RIGHT       = "r"


HORIZONTAL  = 0
VERTICAL    = 1

#               1x1  2x1  3x1  4x1
PIECES      = [  4 ,  3 ,  2 ,  1  ]

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


class Board:
    
    """Representação interna de um tabuleiro de Bimaru.""" 
    
    def __init__(self, matrix, rows, columns, unaltered_rows, unaltered_columns, hints):
        """Construtor da classe. Recebe como argumentos uma matriz que representa
        o tabuleiro, uma lista com os espaços preenchidos nas linhas, uma lista
        com os espaços preenchidos nas colunas e uma lista com o número de peças"""
        self.matrix = matrix
        self.rows = rows
        self.columns = columns
        self.unaltered_rows = unaltered_rows
        self.unaltered_columns = unaltered_columns
        self.hints = hints
        self.pieces = PIECES
        self.post_parse()

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.matrix[row][col] == EMPTY_SPACE:
            return None
        return self.matrix[row][col]
            
    def adjacent_vertical_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row - 1 < 0:
            cell1 = None
        elif self.matrix[row-1][col] == EMPTY_SPACE:
            cell1 = None
        else:
            cell1 = self.matrix[row-1][col]
        if row + 1 > 9:
            cell2 = None
        elif self.matrix[row+1][col] == EMPTY_SPACE:
            cell2 = None
        else:
            cell2 = self.matrix[row+1][col]
        return cell1, cell2

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col - 1 < 0:
            cell1 = None
        elif self.matrix[row][col-1] == EMPTY_SPACE:
            cell1 = None
        else:
            cell1 = self.matrix[row][col-1]
        if col + 1 > 9:
            cell2 = None
        elif self.matrix[row][col+1] == EMPTY_SPACE:
            cell2 = None
        else:
            cell2 = self.matrix[row][col+1]
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
        
        unaltered_rows = rows[:]
        
        columns = stdin.readline()
        columns = columns.rstrip().split("\t")
        columns.pop(0)
        columns = [int(i) for i in columns]
        
        unaltered_columns = columns[:]
        
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
            hint[2] = hint[2].lower()
            
            # retirar 1 ao valor da linha e da coluna
            
            if hint[2] != "w":
                matrix[row][col] = hint[2]
                rows[row] -= 1
                columns[col] -= 1
            else:
                matrix[row][col] = WATER
        
        return Board(matrix, rows, columns, unaltered_rows, unaltered_columns, hints)
    
    def post_parse(self):
        """
        Colocar águas e barcos em volta dos hints caso seja possivel.
        """
        
        for hint in self.hints:
            
            row = hint[0]
            col = hint[1]
        
            if hint[2] == TOP:
                
                if self.matrix[row + 1][col] == EMPTY_SPACE:
                    self.matrix[row + 1][col] = UNDONE_BOAT
                
                    # retirar 1 ao valor da linha e da coluna
                    
                    self.rows[row + 1] -= 1
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
                
                if self.matrix[row - 1][col] == EMPTY_SPACE:
                    self.matrix[row - 1][col] = UNDONE_BOAT
                
                    # retirar 1 ao valor da linha e da coluna
                    
                    self.rows[row - 1] -= 1
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
                
                if self.matrix[row][col - 1] == EMPTY_SPACE:
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
                
                if self.matrix[row][col + 1] == EMPTY_SPACE:
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

    
    def count_boats(self):
        """Retorna o maior barco que ainda não foi colocado"""
        boats={1:4, 2:3, 3:2, 4:1}
        for row in range(0, 10):
            for col in range(0, 10):
                count = 1
                if self.matrix[row][col] == TOP:
                    for i in range(0, 10):
                        if self.matrix[row + i][col] != WATER:
                            count += 1
                        if self.matrix[row + i][col] == BOTTOM:
                            boats[count] -= 1
                            break
                elif self.matrix[row][col] == LEFT:
                    for i in range(0, 10):
                        if self.matrix[row][col + i] != WATER:
                            count += 1
                        if self.matrix[row][col + i] == RIGHT:
                            boats[count] -= 1
                            break
        for i in range(4,0,-1):
            if boats[i] != 0:
                return i
        return 0


class BimaruState:
    
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1
        self.check_up()
        
    def check_up(self):
        """Preenche os valores adjacentes às peças com água."""
        # preenchimento de agua apos a colocacao de barcos e de mais barcos
          
        stop = False
        
        while not stop:
            
            print(self.board.print())
            
            copy = np.copy(self.board.matrix)
            
            for i in range(10):
                column = self.board.matrix[:,i]
                non_zeros = np.nonzero((column == TOP) | (column == BOTTOM) | (column == MIDDLE) | (column == CIRCLE) | (column == UNDONE_BOAT) | (column == LEFT) | (column == RIGHT))
                print("column {} non zeros len: ".format(i) + str(non_zeros[0].size), "vs. ", self.board.unaltered_columns[i])
                if non_zeros[0].size == self.board.unaltered_columns[i]:
                    for j in range(0, 10):
                        if self.board.matrix[j][i] == EMPTY_SPACE:
                            self.board.matrix[j][i] = WATER
                row = self.board.matrix[i]
                non_zeros = np.nonzero((row == LEFT) | (row == RIGHT) | (row == MIDDLE) | (row == CIRCLE) | (row == UNDONE_BOAT) | (row == TOP) | (row == BOTTOM))
                print("row {} non zeros len: ".format(i) + str(non_zeros[0].size), "vs. ", self.board.unaltered_rows[i])
                if non_zeros[0].size == self.board.unaltered_rows[i]:
                    for j in range(0, 10):
                        if self.board.matrix[i][j] == EMPTY_SPACE:
                            self.board.matrix[i][j] = WATER
            
            
            for i in range(10):

                # verificar se se pode preencher os espaços vazios com agua
                
                # verificar linhas
                non_zeros = np.nonzero((self.board.matrix[i] == WATER))
                size = non_zeros[0].size
                print("linha {} non zeros len: ".format(i) + str(size), "vs. ", self.board.rows[i])
                if size == 10 - self.board.unaltered_rows[i]:
                    print("linha {}".format(i))
                    for k in range(10):
                        if self.board.matrix[i][k] == EMPTY_SPACE:
                            self.board.matrix[i][k] = UNDONE_BOAT
                            
                            # retirar 1 ao valor da linha e da coluna
                            
                            self.board.rows[i] -= 1
                            self.board.columns[k] -= 1
                
                # verificar colunas         
                non_zeros = np.nonzero((self.board.matrix[:,i] == WATER))
                size = non_zeros[0].size
                print("coluna {} non zeros len: ".format(i) + str(size), "vs. ", self.board.columns[i])
                if size == 10 - self.board.unaltered_columns[i]:
                    print("coluna {}".format(i))
                    for k in range(10):
                        if self.board.matrix[k][i] == EMPTY_SPACE:
                            self.board.matrix[k][i] = UNDONE_BOAT
                            
                            # retirar 1 ao valor da linha e da coluna
                            
                            self.board.rows[k] -= 1
                            self.board.columns[i] -= 1
                
                
                # verificar se se 
                
                
                middle_index = np.nonzero((self.board.matrix[i] == MIDDLE))
                
                if middle_index[0].size > 0:
                    middle_index = middle_index[0][0]
                    
                    # verificar horizontalmente
                    
                    adjacent_values_vertical    = self.board.adjacent_vertical_values(i, middle_index)
                    adjacent_values_horizontal  = self.board.adjacent_horizontal_values(i, middle_index)
                    if (adjacent_values_vertical[0] == WATER or adjacent_values_vertical[1] == WATER)\
                        and (adjacent_values_horizontal[0] != UNDONE_BOAT and adjacent_values_horizontal[1] != UNDONE_BOAT):
                        print("horizontal")
                        # preencher em cada lado com uma peça de um barco
                        self.board.matrix[i][middle_index - 1] = UNDONE_BOAT
                        self.board.matrix[i][middle_index + 1] = UNDONE_BOAT
                        
                        # retirar 1 ao valor da linha e da coluna
                        
                        self.board.rows[i] -= 2
                        self.board.columns[middle_index - 1] -= 1
                        self.board.columns[middle_index + 1] -= 1
                        
                        # preencher espaço à volta com água
                        self.board.matrix[i - 1][middle_index - 1] = WATER
                        self.board.matrix[i - 1][middle_index + 1] = WATER
                        self.board.matrix[i + 1][middle_index] = WATER
                        self.board.matrix[i - 1][middle_index] = WATER
                        self.board.matrix[i + 1][middle_index + 1] = WATER
                        self.board.matrix[i + 1][middle_index - 1] = WATER
                        # verificar se há espaço extra para as bordas do barco
                        if i + 2 <= 9:
                            self.board.matrix[i + 2][middle_index + 1] = WATER
                            self.board.matrix[i + 2][middle_index - 1] = WATER
                        if i - 2 >= 0:
                            self.board.matrix[i - 2][middle_index + 1] = WATER
                            self.board.matrix[i - 2][middle_index - 1] = WATER
                    
                    # verificar verticalmente
                            
                    if (adjacent_values_horizontal[0] == WATER or adjacent_values_horizontal[1] == WATER)\
                        and (adjacent_values_vertical[0] != UNDONE_BOAT or adjacent_values_vertical[1] != UNDONE_BOAT):
                        print("vertical")
                        # preencher em cima e em baixo com a peça de um barco
                        self.board.matrix[i - 1][middle_index] = UNDONE_BOAT
                        self.board.matrix[i + 1][middle_index] = UNDONE_BOAT
                        
                        # retirar 1 ao valor da linha e da coluna
                        
                        self.board.rows[i - 1] -= 1
                        self.board.rows[i + 1] -= 1
                        self.board.columns[middle_index] -= 2
                        
                        # preencher espaço à volta com água
                        self.board.matrix[i - 1][middle_index - 1] = WATER
                        self.board.matrix[i - 1][middle_index + 1] = WATER
                        self.board.matrix[i][middle_index + 1] = WATER
                        self.board.matrix[i][middle_index - 1] = WATER
                        self.board.matrix[i + 1][middle_index - 1] = WATER
                        self.board.matrix[i + 1][middle_index + 1] = WATER
                        # verificar se há espaço extra para as bordas do barco
                        if i + 2 <= 9:
                            self.board.matrix[i + 2][middle_index + 1] = WATER
                            self.board.matrix[i + 2][middle_index - 1] = WATER
                        if i - 2 >= 0:
                            self.board.matrix[i - 2][middle_index + 1] = WATER
                            self.board.matrix[i - 2][middle_index - 1] = WATER
                            
                                        
            stop = np.array_equal(copy, self.board.matrix)
            
            print("--------------------")
            
            print(self.board.print())
        
        return self
    
    def remove_done_boat(self, size_of_boat):
        self.board.pieces[size_of_boat - 1] -= 1
    
    def treat_left(self, row, col):
        """
        Handles the case where a boat LEFT is found
        """
        if col + 4 <= 9:
            index = col + 4
        else:
            index = 9
        add_col = col + 1
        found_pieces = False
        while add_col <= index:
            if self.board.matrix[row][add_col] == UNDONE_BOAT or self.board.matrix[row][add_col] == MIDDLE:
                found_pieces = True
            elif self.board.matrix[row][add_col] == RIGHT or index == 9:
                # meter isto legivel
                if add_col == index:
                    # quer dizer que sao 2 barcos, preencher so um deles e
                    # deixar o algoritmo fazer o resto
                    self.board.matrix[row][col + 1] = RIGHT
                    self.board.matrix[row][col + 2] = WATER
                    # remover barco preenchido
                    self.remove_done_boat(2)
                    break
                # remover barco preenchido
                size_of_boat = index - add_col
                self.remove_done_boat(size_of_boat)

                if index == 9:
                    self.board.matrix[row][index] = RIGHT
                
                add_col -= 1
                while add_col > col:
                    self.board.matrix[row][add_col] = MIDDLE
                    add_col -= 1
                break
            elif self.board.matrix[row][add_col] == WATER:
                if found_pieces and add_col < index:
                    add_col -= 1
                    self.board.matrix[row][add_col] = RIGHT
                    # remover barco preenchido
                    size_of_boat = index - add_col
                    self.remove_done_boat(size_of_boat)
                    
                    add_col -= 1
                    while add_col > col:
                        self.board.matrix[row][add_col] = MIDDLE
                        add_col -= 1
                break
            
            add_col += 1

    def treat_right(self, row, col):
        """
        Handles the case where a boat RIGHT is found
        """
        
        if col - 4 >= 0:
            index = col - 4
        else:
            index = 0
        add_col = col - 1
        found_pieces = False
        while add_col >= index:
            if self.board.matrix[row][add_col] == UNDONE_BOAT or self.board.matrix[row][add_col] == MIDDLE:
                found_pieces = True
            elif self.board.matrix[row][add_col] == LEFT or index == 0:
                
                if add_col == index:
                    # quer dizer que sao 2 barcos, preencher so um deles e
                    # deixar o algoritmo fazer o resto
                    self.board.matrix[row][col - 1] = LEFT
                    self.board.matrix[row][col - 2] = WATER
                    # remover barco preenchido
                    self.remove_done_boat(2)
                    break
                # remover barco preenchido
                size_of_boat = col - add_col
                self.remove_done_boat(size_of_boat)
                
                if index == 0:
                    self.board.matrix[row][index] = LEFT

                add_col += 1
                while add_col < col:
                    self.board.matrix[row][add_col] = MIDDLE
                    add_col += 1
                break
            elif self.board.matrix[row][add_col] == WATER:
                if found_pieces and add_col > index:
                    # remover barco preenchido
                    size_of_boat = col - add_col
                    self.remove_done_boat(size_of_boat)
                    
                    add_col += 1
                    self.board.matrix[row][add_col] = LEFT
                    # meter isto legivel
                    add_col += 1
                    while add_col < col:
                        self.board.matrix[row][add_col] = MIDDLE
                        add_col += 1
                break
            
            add_col -= 1
            
    
    def treat_top(self, row, col):
        """
        Handles the case where a boat TOP is found
        """
        
        if row + 4 <= 9:
            index = row + 4
        else:
            index = 9
        add_row = row + 1
        found_pieces = False
        while add_row <= index:
            if self.board.matrix[add_row][col] == UNDONE_BOAT:
                found_pieces = True
            elif self.board.matrix[add_row][col] == BOTTOM or index == 9:
                if add_row == index:
                    # quer dizer que sao 2 barcos, preencher so um deles e
                    # deixar o algoritmo fazer o resto
                    self.board.matrix[row + 1][col] = BOTTOM
                    self.board.matrix[row + 2][col] = WATER
                    
                    # remover barco preenchido
                    self.remove_done_boat(2)    
                    break

                if index == 9:
                    self.board.matrix[index][col] = TOP
                
                # remover barco preenchido
                size_of_boat = add_row - row
                self.remove_done_boat(size_of_boat)
                
                add_row -= 1
                while add_row > row:
                    self.board.matrix[add_row][col] = MIDDLE
                    add_row -= 1
                break
            elif self.board.matrix[add_row][col] == WATER:
                if found_pieces and add_row < index:
                    add_row -= 1
                    # remover barco preenchido
                    size_of_boat = add_row - row
                    self.remove_done_boat(size_of_boat)
                    
                    self.board.matrix[add_row][col] = BOTTOM
                    add_row -= 1
                    while add_row > row:
                        self.board.matrix[add_row][col] = MIDDLE
                        add_row -= 1
                break
                
            add_row += 1
        
    def treat_bottom(self, row, col):
        """
        Handles the case where a boat BOTTOM is found
        """
        
        if row - 4 >= 0:
            index = row - 4
        else:
            index = 0
        # should be seperate function
        add_row = row - 1
        found_pieces = False
        while add_row >= index:
            if self.board.matrix[add_row][col] == UNDONE_BOAT:
                found_pieces = True
                
            elif self.board.matrix[add_row][col] == TOP or index == 0:
                if add_row == index:
                    # quer dizer que sao 2 barcos, preencher so um deles e
                    # deixar o algoritmo fazer o resto
                    self.board.matrix[row - 1][col] = TOP
                    self.board.matrix[row - 2][col] = WATER
                    
                    # remover barco preenchido
                    self.remove_done_boat(2)
                    break

                if index == 0:
                    self.board.matrix[index][col] = TOP
                
                # remover barco preenchido
                size_of_boat = row - add_row
                self.remove_done_boat(size_of_boat)
                
                add_row += 1
                
                while add_row < row:
                    self.board.matrix[add_row][col] = MIDDLE
                    add_row += 1
                break
            
            elif self.board.matrix[add_row][col] == WATER:
                if found_pieces and add_row > index:
                    add_row += 1
                    self.board.matrix[add_row][col] = TOP
                    add_row += 1
                    while add_row < row:
                        self.board.matrix[add_row][col] = MIDDLE
                        add_row += 1
                break
                
            add_row -= 1

    
    def treat_undone_boat(self, row, col):
        """
        Handles the case where a boat is found but it's not complete
        """
        
        # check adjacent positions for other pieces of the boat
        
        horizontal_adjacent = self.board.adjacent_horizontal_values(row, col)
        vertical_adjacent = self.board.adjacent_vertical_values(row, col)
                
        if all(value in (WATER, None) for value in horizontal_adjacent):
            # possibility of a vertical boat
            if all(value in (WATER, None) for value in vertical_adjacent):
                # it's a circle
                self.board.matrix[row][col] = CIRCLE
                
                # remover barco preenchido
                self.remove_done_boat(1)
            else:
                # vertical boat
                
                # pela definição do loop, o resto do barco tem de estar abaixo
                
                # check if the boat is complete
                
                if vertical_adjacent[0] == TOP:
                    # then this must be a middle piece
                    self.board.matrix[row][col] = MIDDLE

                
                # ver como completar o resto do barco
                    
                else:

                    # ver se o barco esta delimitado por água

                    add_col = col + 1
                    found_pieces = False
                    while self.board.matrix[row][add_col] not in (WATER, EMPTY_SPACE):
                        if self.board.matrix[row][add_col] == UNDONE_BOAT or self.board.matrix[row][add_col] == MIDDLE:
                            found_pieces = True
                        elif self.board.matrix[row][add_col] == RIGHT:
                            # meter isto legivel
                            
                            # remover barco preenchido
                            size_of_boat = add_col - col + 1
                            self.remove_done_boat(size_of_boat)

                            if index == 9:
                                self.board.matrix[row][index] = RIGHT
                            
                            add_col -= 1
                            while add_col > col:
                                self.board.matrix[row][add_col] = MIDDLE
                                add_col -= 1
                            break
                        
                        add_col += 1

                        if found_pieces and add_col < index:
                            add_col -= 1
                            self.board.matrix[row][add_col] = RIGHT
                            # remover barco preenchido
                            size_of_boat = index - add_col
                            self.remove_done_boat(size_of_boat)
                            
                            add_col -= 1
                            while add_col > col:
                                self.board.matrix[row][add_col] = MIDDLE
                                add_col -= 1
                        break
                    self.board.matrix[row][col] = TOP
                    
                    self.treat_top(row, col)
                
            
        else:
            # horizontal boat
            
            # pela definição do loop, o resto do barco tem de estar à direita
            
            # check if the boat is complete
            
            if horizontal_adjacent[0] == LEFT:
                # then this must be a middle piece
                self.board.matrix[row][col] = MIDDLE

                # ISTO TA MAL, VERIFICAR QUE O BARCO ESTA DELIMITADO POR AGUASN AT LEAST
            
            # ver como completar o resto do barco
            
            else:    
                self.board.matrix[row][col] = LEFT
            
    
    def complete_boats(self):
        """
        Completa os barcos feitos de momento com a denominação correta.
        """
        
        for row in range(10):
            for col in range(10):
                if self.board.matrix[row][col] != WATER and self.board.matrix[row][col] != EMPTY_SPACE:
                    position = self.board.matrix[row][col]
                    if position == LEFT:
                        self.treat_left(row, col)
                            
                    elif position == RIGHT:
                        self.treat_right(row, col)
                        
                    elif position == TOP:
                        self.treat_top(row, col)
                        
                    elif position == BOTTOM:
                        self.treat_bottom(row, col)
                        
                    elif position == UNDONE_BOAT:
                        self.treat_undone_boat(row, col)
    
    
    def __lt__(self, other):
        return self.id < other.id


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board

    def is_valid_position(self, row, col, boat_size, orientation):
        """Verifica se colocar uma parte de barco na horizontal na posição dada é válido"""
        count = 0
         
        if orientation == HORIZONTAL:
            if self.board[row][col] == LEFT:
                tuple_adjacent_b = self.board.adjacent_vertical_values(row, col)
                for i in range(8):
                    if i != 3 and i != 5 and i != 6:
                        if tuple_adjacent_b[i] not in (WATER, EMPTY_SPACE):
                            return False
                count += 1
            elif self.board[row][col] == EMPTY_SPACE:
                if self.board.columns[col] < 1:
                    return False
            else:
                return False
                
            for i in range(col + 1, col + boat_size - 1):
                if self.board[row][i] == EMPTY_SPACE:
                    if self.board.columns[i] < 1:
                        return False
                elif self.board[row][i] == MIDDLE:
                    count += 1
                else:
                    return False
                if self.board.adjacent_vertical_values(row, i)[0]  not in (WATER, EMPTY_SPACE):
                    return False
                if self.board.adjacent_vertical_values(row, i)[1]  not in (WATER, EMPTY_SPACE):
                    return False
                
            if self.board[row][col + boat_size - 1] == RIGHT:
                tuple_adjacent_e = self.board.adjacent_vertical_values(row, col + boat_size - 1)
                for i in range(8):
                    if i != 2 and i != 4 and i != 7:
                        if tuple_adjacent_e[i] not in (WATER, EMPTY_SPACE):
                            return False
                count += 1
            elif self.board[row][col + boat_size - 1] == EMPTY_SPACE:
                if self.board.columns[col + boat_size - 1] < 1:
                    return False
                
            if self.board.rows[row] < boat_size - count:
                return False
            
    # # (cima, baixo, esquerda, direita, esquedra_cima, direita_baixo, direita_cima, esquerda_baixo)
    
        elif orientation == VERTICAL:
            if self.board[row][col] == TOP:
                tuple_adjacent_b = self.board.adjacent_vertical_values(row, col)
                for i in range(8):
                    if i != 1 and i != 5 and i != 7:
                        if tuple_adjacent_b[i] not in (WATER, EMPTY_SPACE):
                            return False
                count += 1
            elif self.board[row][col] == EMPTY_SPACE:
                if self.board.rows[row] < 1:
                    return False
            else:
                return False
                
            for i in range(row + 1, row + boat_size - 1):
                if self.board[i][col] == EMPTY_SPACE:
                    if self.board.rows[i] < 1:
                        return False
                elif self.board[i][col] == MIDDLE:
                    count += 1
                else:
                    return False
                if self.board.adjacent_horizontal_values(i, col)[0]  not in (WATER, EMPTY_SPACE):
                    return False
                if self.board.adjacent_horizontal_values(i, col)[1]  not in (WATER, EMPTY_SPACE):
                    return False
                
            if self.board[row + boat_size - 1][col] == BOTTOM:
                tuple_adjacent_e = self.board.adjacent_vertical_values(row + boat_size - 1, col)
                for i in range(8):
                    if i != 0 and i != 4 and i != 6:
                        if tuple_adjacent_e[i] not in (WATER, EMPTY_SPACE):
                            return False
                count += 1
            elif self.board[row + boat_size - 1][col] == EMPTY_SPACE:
                if self.board.rows[row + boat_size - 1] < 1:
                    return False
                
            if self.board.columns[col] < boat_size - count:
                return False
 

        return False

    def is_valid_submarine_position(self, row, col):
        """Verifica se colocar um submarino na posição dada é válido"""

        if board[row][col] != EMPTY_SPACE:
            return False
        
        if board[row][col] == EMPTY_SPACE:
            if self.board.rows[row] < 1 or self.board.columns[col] < 1:
                return False
        tuple_adjacent = self.board.adjacent_values(row, col)    
        for value in tuple_adjacent:
            if value not in (WATER, EMPTY_SPACE):
                return False
        return True



    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        # formato da ação: (cell_1, cell_2, boat_size, orientação)
        
        state.board.complete_boats()
        
        board = state.board
        actions = []
        boat_size = board.count_boats()
        if boat_size > 1:
            for row in range(10):
                for col in range(10):
                    if  self.is_valid_position(board, row, col, boat_size, HORIZONTAL):
                        actions.append((row, col, boat_size, HORIZONTAL))
                    elif self.is_valid_position(board, row, col, boat_size, VERTICAL):
                        actions.append((row, col, boat_size, VERTICAL))
        elif boat_size == 1:
            for row in range(10):
                for col in range(10):
                    if self.is_valid_submarine_position(board, row, col):
                        actions.append((row, col, 1))

    
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        # action = (row, col, boat_size, orientation)
        
        if action[2] == 1:
            self.board.matrix[action[0]][action[1]] = CIRCLE
        elif action[3] == HORIZONTAL:
            self.board.matrix[action[0]][action[1]] = LEFT
            for col in range(action[1], action[1] + action[2] - 1):
                self.board.matrix[action[0]][col] = MIDDLE
            self.board.matrix[action[0]][action[1] + action[2] - 1] = RIGHT
        
        elif action[3] == VERTICAL:
            self.board.matrix[action[0]][action[1]] = TOP
            for row in range(action[0], action[0] + action[2] - 1):
                self.board.matrix[row][action[1]] = MIDDLE
            self.board.matrix[action[0] + action[2] - 1][action[1]] = BOTTOM
        
        
        return BimaruState(state.board) 

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        
        """not np.any(state.board.pieces) or """
        
        if not np.any(state.board.rows) or not np.any(state.board.columns):
            state.complete_boats()
            for hint in state.board.hints:
                state.board.matrix[hint[0]][hint[1]] = hint[2].upper()
            return True

        return False
                

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        
        # usar heuristica consistente
        
        return -node.depth*2
    

if __name__ == "__main__":
    
    board = Board.parse_instance()
    
    print(board.print())
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    initial_state = BimaruState(board)
    
    #goal_node = depth_first_tree_search(problem)
    
    print("Is goal? ", problem.goal_test(initial_state))
    print("Solution:")
    print(initial_state.board.print())
    