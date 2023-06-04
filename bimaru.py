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
import copy
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
        self.check_up()
            
        self.complete_boats()

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.matrix[row][col] == EMPTY_SPACE:
            return None
        return self.matrix[row][col]
            
    def adjacent_vertical_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row - 1 < 0:
            cell1 = WATER
        elif self.matrix[row-1][col] == EMPTY_SPACE:
            cell1 = None
        else:
            cell1 = self.matrix[row-1][col]
        if row + 1 > 9:
            cell2 = WATER
        elif self.matrix[row+1][col] == EMPTY_SPACE:
            cell2 = None
        else:
            cell2 = self.matrix[row+1][col]
        return cell1, cell2

    def adjacent_horizontal_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col - 1 < 0:
            cell1 = WATER
        elif self.matrix[row][col-1] == EMPTY_SPACE:
            cell1 = None
        else:
            cell1 = self.matrix[row][col-1]
        if col + 1 > 9:
            cell2 = WATER
        elif self.matrix[row][col+1] == EMPTY_SPACE:
            cell2 = None
        else:
            cell2 = self.matrix[row][col+1]
        return cell1, cell2

    def adjacent_diagonal1_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""

        cell1 = None
        cell2 = None
        if row - 1 >= 0 and col - 1 >= 0 :
            cell1 = self.matrix[row-1][col-1]
        if row + 1 <= 9 and col + 1 <= 9 :
            cell2 = self.matrix[row+1][col+1]
        return cell1, cell2

    def adjacent_diagonal2_values(self, row: int, col: int) -> tuple:
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        
        cell1 = None
        cell2 = None
        if  row - 1 >= 0 and col + 1 <= 9 :
            cell1 = self.matrix[row-1][col+1]
        if row + 1 <= 9 and col - 1 >=0 :
            cell2 = self.matrix[row+1][col-1]
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
                str_ += col + ""
            str_ += "\n"
            i+=1
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
                
                # remove from pieces
                
                self.pieces[0] -= 1
                
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
                    self.columns[col - 1] -= 1
            
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
                    self.columns[col + 1] -= 1  
            
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
                    
                    
    def check_up(self):
        """Preenche os valores adjacentes às peças com água."""
        # preenchimento de agua apos a colocacao de barcos e de mais barcos
          
        stop = False
        
        while not stop:
            
            copy = np.copy(self.matrix)
            
            for i in range(10):
                column = self.matrix[:,i]
                non_zeros = np.nonzero((column == TOP) | (column == BOTTOM) | (column == MIDDLE) | (column == CIRCLE) | (column == UNDONE_BOAT) | (column == LEFT) | (column == RIGHT))
                if non_zeros[0].size == self.unaltered_columns[i]:
                    for j in range(0, 10):
                        if self.matrix[j][i] == EMPTY_SPACE:
                            self.matrix[j][i] = WATER
                row = self.matrix[i]
                non_zeros = np.nonzero((row == LEFT) | (row == RIGHT) | (row == MIDDLE) | (row == CIRCLE) | (row == UNDONE_BOAT) | (row == TOP) | (row == BOTTOM))
                if non_zeros[0].size == self.unaltered_rows[i]:
                    for j in range(0, 10):
                        if self.matrix[i][j] == EMPTY_SPACE:
                            self.matrix[i][j] = WATER
            
            for i in range(10):

                # verificar se se pode preencher os espaços vazios com agua
                
                # verificar linhas
                non_zeros = np.nonzero((self.matrix[i] == EMPTY_SPACE))
                size = non_zeros[0].size
                if size == self.rows[i]:
                    for k in range(10):
                                    
                        if self.matrix[i][k] == EMPTY_SPACE:
                            self.matrix[i][k] = UNDONE_BOAT

                            if k - 1 >= 0 and i - 1 >= 0: 
                                self.matrix[i-1][k-1] = WATER
                            if k + 1 <= 9 and i - 1 >= 0:
                                self.matrix[i-1][k+1] = WATER
                            if k - 1 >= 0 and i + 1 <= 9:
                                self.matrix[i+1][k-1] = WATER
                            if k + 1 <= 9 and i + 1 <= 9:
                                self.matrix[i+1][k+1] = WATER
                            
                            # retirar 1 ao valor da linha e da coluna
                            
                            self.rows[i] -= 1
                            self.columns[k] -= 1
                
                # verificar colunas         
                non_zeros = np.nonzero((self.matrix[:,i] == EMPTY_SPACE))
                size = non_zeros[0].size
                if size == self.columns[i]:
                    for k in range(10):
                        
                        if self.matrix[k][i] == EMPTY_SPACE:
                            self.matrix[k][i] = UNDONE_BOAT

                            if k - 1 >= 0 and i - 1 >= 0: 
                                self.matrix[k-1][i-1] = WATER
                            if k - 1 >= 0 and i + 1 <= 9:
                                self.matrix[k-1][i+1] = WATER
                            if k + 1 <= 9 and i - 1 >= 0:
                                self.matrix[k+1][i-1] = WATER
                            if k + 1 <= 9 and i + 1 <= 9:
                                self.matrix[k+1][i+1] = WATER
                            
                            # # meter água à volta do barco
                            
                            # if any(value in (TOP, BOTTOM, UNDONE_BOAT) for value in self.adjacent_vertical_values(k, i))\
                            #     and any(value == WATER for value in self.adjacent_horizontal_values(k, i)):
                            
                            #     if i - 1 >= 0:
                            #         self.matrix[k][i - 1] = WATER
                            #     if i + 1 <= 9:
                            #         self.matrix[k][i + 1] = WATER
                            
                            # retirar 1 ao valor da linha e da coluna
                            
                            self.rows[k] -= 1
                            self.columns[i] -= 1
                
                
                # verificar se há MIDDLE
                
                middle_index = np.nonzero((self.matrix[i] == MIDDLE))
                
                if middle_index[0].size > 0:
                    middle_index = middle_index[0][0]
                    
                    # verificar horizontalmente
                    
                    adjacent_values_vertical    = self.adjacent_vertical_values(i, middle_index)
                    adjacent_values_horizontal  = self.adjacent_horizontal_values(i, middle_index)
                    if all(value == WATER for value in adjacent_values_vertical)\
                        and all(value not in (UNDONE_BOAT, LEFT, RIGHT, MIDDLE) for value in adjacent_values_horizontal):
                        # preencher em cada lado com uma peça de um barco
                        self.matrix[i][middle_index - 1] = UNDONE_BOAT
                        self.matrix[i][middle_index + 1] = UNDONE_BOAT
                        
                        # retirar 1 ao valor da linha e da coluna
                        
                        self.rows[i] -= 2
                        self.columns[middle_index - 1] -= 1
                        self.columns[middle_index + 1] -= 1
                        
                        # preencher espaço à volta com água
                        if i - 1 >= 0:
                            self.matrix[i - 1][middle_index - 1] = WATER
                            self.matrix[i - 1][middle_index + 1] = WATER
                            self.matrix[i - 1][middle_index] = WATER
                        if i + 1 <= 9:
                            self.matrix[i + 1][middle_index] = WATER
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
                            
                    if all(value == WATER for value in adjacent_values_horizontal)\
                        and all(value not in (UNDONE_BOAT, TOP, BOTTOM, MIDDLE) for value in adjacent_values_vertical):
                        # preencher em cima e em baixo com a peça de um barco
                        
                        self.matrix[i - 1][middle_index] = UNDONE_BOAT
                        self.matrix[i + 1][middle_index] = UNDONE_BOAT
                        
                        # retirar 1 ao valor da linha e da coluna
                        
                        self.rows[i - 1] -= 1
                        self.rows[i + 1] -= 1
                        self.columns[middle_index] -= 2
                        
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
                            
                                        
            stop = np.array_equal(copy, self.matrix)
        
    
                    
    def remove_done_boat(self, size_of_boat):
        self.pieces[size_of_boat - 1] -= 1
    
    def treat_left(self, row, col):
        """
        Handles the case where a boat LEFT is found
        """
        
        add_col = col + 1
        found_pieces = False
        
        while self.matrix[row][add_col] not in (WATER, EMPTY_SPACE):
            if self.matrix[row][add_col] in (UNDONE_BOAT, MIDDLE):
                found_pieces = True
                
            elif self.matrix[row][add_col] == RIGHT:
                # barco acabou
                
                found_pieces = True
                
                add_col += 1
                
                break
            
            if add_col == 9:
                # chegamos ao final da linha, o barco acabou
                
                add_col += 1
                
                break
            
            add_col += 1

        if found_pieces:
            add_col -= 1
            self.matrix[row][add_col] = RIGHT
            # remover barco preenchido
            size_of_boat = add_col - col + 1
            self.remove_done_boat(size_of_boat)
            
            add_col -= 1
            while add_col > col:
                self.matrix[row][add_col] = MIDDLE
                add_col -= 1
        
    
    def treat_top(self, row, col):
        """
        Handles the case where a boat TOP is found
        """
        
        add_row = row + 1
        found_pieces = False
        
        while self.matrix[add_row][col] not in (WATER, EMPTY_SPACE):
            if self.matrix[add_row][col] in (UNDONE_BOAT, MIDDLE):
                found_pieces = True
                
            elif self.matrix[add_row][col] == BOTTOM:
                # barco acabou
                
                found_pieces = True
                
                add_row += 1
                
                break
            
            if add_row == 9:
                # chegamos ao final da linha, o barco acabou
                
                add_row += 1
                
                break
            
            add_row += 1

        if found_pieces:
            add_row -= 1
            self.matrix[add_row][col] = BOTTOM
            # remover barco preenchido
            size_of_boat = add_row - row + 1
            self.remove_done_boat(size_of_boat)
            
            add_row -= 1
            while add_row > row:
                self.matrix[add_row][col] = MIDDLE
                add_row -= 1
                
        
    def treat_undone_boat(self, row, col):
        """
        Handles the case where a boat is found but it's not complete
        """
        
        # check adjacent positions for other pieces of the boat
        
        horizontal_adjacent = self.adjacent_horizontal_values(row, col)
        vertical_adjacent = self.adjacent_vertical_values(row, col)
                
        if all(value == WATER for value in horizontal_adjacent):
            # possibility of a vertical boat
            if all(value == WATER for value in vertical_adjacent):
                
                # it's a circle
                
                self.matrix[row][col] = CIRCLE
                
                # IMPORTANT: verificar se é preciso preencher o barco a volta com agua
                
                # remover barco preenchido
                self.remove_done_boat(1)
            else:
                # vertical boat
                
                # pela definição do loop, o resto do barco tem de estar abaixo

                # ver se o barco esta delimitado por água

                add_row = row + 1
                found_pieces = False
                
                if any(value == None for value in vertical_adjacent):
                    return
                
                while self.matrix[add_row][col] != WATER:
                    if self.matrix[add_row][col] in (UNDONE_BOAT, MIDDLE):
                        found_pieces = True
                        
                    elif self.matrix[add_row][col] == BOTTOM:
                        # barco acabou
                        
                        found_pieces = True
                        
                        add_row += 1
                        
                        break
                    
                    if add_row == 9:
                        # chegamos ao final da linha, o barco acabou
                        
                        add_row += 1
                        
                        break
                    
                    add_row += 1

                if found_pieces:
                    add_row -= 1
                    self.matrix[add_row][col] = BOTTOM
                    # remover barco preenchido
                    size_of_boat = add_row - row + 1
                    self.remove_done_boat(size_of_boat)
                    
                    add_row -= 1
                    while add_row > row:
                        self.matrix[add_row][col] = MIDDLE
                        add_row -= 1
            
                self.matrix[row][col] = TOP
            
            
        else:
            # horizontal boat
            
            # pela definição do loop, o resto do barco tem de estar à direita
            
            # verificar se o barco esta delimitado por água
            
            add_col = col + 1
            found_pieces = False
            
            while self.matrix[row][add_col] != WATER:
                if self.matrix[row][add_col] in (UNDONE_BOAT, MIDDLE):
                    found_pieces = True
                    
                elif self.matrix[row][add_col] == RIGHT:
                    # barco acabou
                    
                    found_pieces = True
                    
                    # por conformidade ao loop mais abaixo, adicionamos +1 ao add_col na mesma
                    add_col += 1
                    
                    break
                
                if add_col == 9:
                    # chegamos ao final da linha, o barco acabou
                    
                    # por conformidade ao loop mais abaixo, adicionamos +1 ao add_col na mesma
                    add_col += 1
                    
                    break
                
                add_col += 1

            if found_pieces:
                add_col -= 1
                self.matrix[row][add_col] = RIGHT
                # remover barco preenchido
                size_of_boat = add_col - col + 1
                self.remove_done_boat(size_of_boat)
                
                add_col -= 1
                while add_col > col:
                    self.matrix[row][add_col] = MIDDLE
                    add_col -= 1
        
            self.matrix[row][col] = LEFT
            
            if row - 1 >= 0:
                self.matrix[row - 1][col] = WATER
            if row + 1 <= 9:
                self.matrix[row + 1][col] = WATER
            
    
    def complete_boats(self):
        """
        Completa os barcos feitos de momento com a denominação correta.
        """
        
        for row in range(10):
            for col in range(10):
                if self.matrix[row][col] not in (WATER, EMPTY_SPACE):
                    position = self.matrix[row][col]
                    if position == LEFT:
                        self.treat_left(row, col)
                        
                    elif position == TOP:
                        self.treat_top(row, col)
                        
                    elif position == UNDONE_BOAT:
                        self.treat_undone_boat(row, col)

    
    # def count_boats(self):
    #     """Retorna o maior barco que ainda não foi colocado"""
    #     boats={1:4, 2:3, 3:2, 4:1}
    #     for row in range(10):
    #         for col in range(10):
    #             count = 1
    #             if self.matrix[row][col] == TOP:
    #                 for i in range(10):
    #                     if row + i <= 9 and self.matrix[row + i][col] != WATER :
    #                         count += 1
    #                     if row + i <= 9 and self.matrix[row + i][col] == BOTTOM:
    #                         boats[count] -= 1
    #                         break
    #             elif self.matrix[row][col] == LEFT:
    #                 for i in range(10):
    #                     if col + i <= 9 and self.matrix[row][col + i] != WATER:
    #                         count += 1
    #                     if col + i <= 9 and self.matrix[row][col + i] == RIGHT:
    #                         boats[count] -= 1
    #                         break
    #     for i in range(4,0,-1):
    #         if boats[i] != 0:
    #             return i
    #     return 0

    def is_valid_position(self, row, col, boat_size, orientation):
        """Verifica se a posição é válida para colocar um barco de tamanho boat_size com uma dada orientação"""
        count = 0
        boat = []
         
        # pôr barco na horizontal

        if orientation == HORIZONTAL:
            if col + boat_size - 1 > 9:
                return False
            if self.matrix[row][col] in (LEFT, UNDONE_BOAT):
                tuple_adjacent_b = self.adjacent_values(row, col)
                for i in range(8):
                    if i != 3 and i != 5 and i != 6:
                        if tuple_adjacent_b[i] not in (WATER, EMPTY_SPACE, None):
                            return False
                count += 1

            elif self.matrix[row][col] == EMPTY_SPACE:
                if self.columns[col] < 1:
                    return False
            
            else:
                return False
                
            for i in range(col + 1, col + boat_size - 1):
                if self.matrix[row][i] == EMPTY_SPACE:
                    if self.columns[i] < 1:
                        return False
                elif self.matrix[row][i] in (MIDDLE, UNDONE_BOAT):
                    count += 1
                else:
                    return False
                if self.adjacent_vertical_values(row, i)[0]  not in (WATER, EMPTY_SPACE, None):
                    return False
                if self.adjacent_vertical_values(row, i)[1]  not in (WATER, EMPTY_SPACE, None):
                    return False
                
            if self.matrix[row][col + boat_size - 1] in (RIGHT, UNDONE_BOAT):
                tuple_adjacent_e = self.adjacent_values(row, col + boat_size - 1)
                for i in range(8):
                    if i != 2 and i != 4 and i != 7:
                        if tuple_adjacent_e[i] not in (WATER, EMPTY_SPACE, None):
                            return False
                count += 1
            elif self.matrix[row][col + boat_size - 1] == EMPTY_SPACE:
                if self.columns[col + boat_size - 1] < 1:
                    return False  
            else:
                return False

            if self.rows[row] < boat_size - count:
                return False
            for co in range(col, col + boat_size):
                boat.append(self.matrix[row][co])
            if (boat_size == 2 and boat == [LEFT, RIGHT]) or (boat_size == 3 and boat == [LEFT, MIDDLE, RIGHT]) or \
                  (boat_size == 4 and boat == [LEFT, MIDDLE, MIDDLE, RIGHT]):
                return False
                
            
    # (cima, baixo, esquerda, direita, esquedra_cima, direita_baixo, direita_cima, esquerda_baixo)
    
        # pôr barco na vertical
    
        elif orientation == VERTICAL:
            if row + boat_size - 1 > 9:
                return False
            if self.matrix[row][col] in (TOP, UNDONE_BOAT):
                tuple_adjacent_b = self.adjacent_values(row, col)
                for i in range(8):
                    if i != 1 and i != 5 and i != 7:
                        if tuple_adjacent_b[i] not in (WATER, EMPTY_SPACE, None):
                            return False
                count += 1
            elif self.matrix[row][col] == EMPTY_SPACE:
                if self.rows[row] < 1:
                    return False
                       
            else:
                return False    
            for i in range(row + 1, row + boat_size - 1):
                if self.matrix[i][col] == EMPTY_SPACE:
                    if self.rows[i] < 1:
                        return False
                    
                elif self.matrix[i][col] in (MIDDLE, UNDONE_BOAT):
                    count += 1
                else:
                    return False
                if self.adjacent_horizontal_values(i, col)[0]  not in (WATER, EMPTY_SPACE, None):
                    return False
                if self.adjacent_horizontal_values(i, col)[1]  not in (WATER, EMPTY_SPACE, None):
                    return False
                
            if self.matrix[row + boat_size - 1][col] in (BOTTOM, UNDONE_BOAT):
                tuple_adjacent_e = self.adjacent_values(row + boat_size - 1, col)
                for i in range(8):
                    if i != 0 and i != 4 and i != 6:
                        if tuple_adjacent_e[i] not in (WATER, EMPTY_SPACE, None):
                            return False
                count += 1
            elif self.matrix[row + boat_size - 1][col] == EMPTY_SPACE:
                if self.rows[row + boat_size - 1] < 1:
                    return False
            else:
                return False
            if self.columns[col] < boat_size - count:
                return False
            
            for ro in range(row, row + boat_size):
                boat.append(self.matrix[ro][col])

            if (boat_size == 2 and boat == [TOP, BOTTOM]) or \
                (boat_size == 3 and boat == [TOP, MIDDLE, BOTTOM]) or \
                    (boat_size == 4 and boat == [TOP, MIDDLE, MIDDLE, BOTTOM]):
                return False

 
    # (cima, baixo, esquerda, direita, esquedra_cima, direita_baixo, direita_cima, esquerda_baixo)

        return True
    

    def is_valid_submarine_position(self, row, col):
        """Verifica se colocar um submarino na posição dada é válido"""

        if self.matrix[row][col] not in (EMPTY_SPACE, UNDONE_BOAT):
            return False
        
        if self.matrix[row][col] == EMPTY_SPACE:
            if self.rows[row] < 1 or self.columns[col] < 1:
                return False
        tuple_adjacent = self.adjacent_values(row, col)    
        for value in tuple_adjacent:
            if value not in (WATER, EMPTY_SPACE, None):
                return False
        return True

    def reverse_clean_board(self):
        """Limpa o tabuleiro de forma a que fique vazio"""
        for row in range(10):
            for col in range(10):
                if self.columns[col] == 0 and self.rows[row] == 0 \
                      and self.matrix[row][col] == UNDONE_BOAT:
                    self.matrix[row][col] = WATER




class BimaruState:
    
    state_id = 0

    def __init__(self, board: Board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    
    def __lt__(self, other):
        return self.id < other.id


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(initial = BimaruState(board), goal=None)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        # IMPORTANT:
        
        # ver linhas e colunas com baixo numero
        
        # ou 
        
        # ver como meter maior barco possivel
        
        # formato da ação: (cell_1, cell_2, boat_size, orientação)
        
        for i in range(3,-1,-1):
            if state.board.pieces[i] != 0:
                boat_size = i + 1
                break
        
        if any(row < 0 for row in state.board.rows) or any(col < 0 for col in state.board.columns):
            return []

        board = state.board
        actions = []
        # count_empty_spaces_row = [0]*10
        # count_empty_spaces_col = [0]*10
        # for row in range(10):
        #     for col in range(10):
        #         if board[row][col] == EMPTY_SPACE:
        #             count_empty_spaces_row[row] += 1
        #             count_empty_spaces_col[col] += 1
        if boat_size > 1:
            for row in range(10):
                # if board.rows[row] <= count_empty_spaces_col[row]:
                for col in range(10):
                    # if board.columns[col] <= count_empty_spaces_row[col]:
                    if  board.is_valid_position( row, col, boat_size, HORIZONTAL):
                        actions.append((row, col, boat_size, HORIZONTAL))
                    if board.is_valid_position( row, col, boat_size, VERTICAL):
                        actions.append((row, col, boat_size, VERTICAL))
                
        elif boat_size == 1:
            for row in range(10):
                # if board.rows[row] <= count_empty_spaces_row[row]:  
                for col in range(10):
                    # if board.columns[col] <= count_empty_spaces_col[col]:
                    if board.is_valid_submarine_position(row, col):
                        actions.append((row, col, 1))
                        
        
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        board = copy.deepcopy(state.board)

        # action = (row, col, boat_size, orientation)
        
        if action[2] == 1:
            if board.matrix[action[0]][action[1]] == EMPTY_SPACE:
                board.rows[action[0]] -= 1
                board.columns[action[1]] -= 1
                
            board.matrix[action[0]][action[1]] = CIRCLE
            
            for row in range(action[0] - 1, action[0] + 2):
                for col in range(action[1] - 1, action[1] + 2):
                    if row >= 0 and row < 10 and col >= 0 and col < 10 and row != action[0] and col != action[1]:
                        if board.matrix[row][col] == EMPTY_SPACE:
                            board.matrix[row][col] = WATER
            board.pieces[action[2] - 1] -= 1

        elif action[3] == HORIZONTAL:
            if board.matrix[action[0]][action[1]] == EMPTY_SPACE:
                board.rows[action[0]] -= 1
                board.columns[action[1]] -= 1
                
            board.matrix[action[0]][action[1]] = LEFT
            for col in range(action[1]+1, action[1] + action[2] - 1):
                if board.matrix[action[0]][col] == EMPTY_SPACE:
                    board.columns[col] -= 1
                    board.rows[action[0]] -= 1
                board.matrix[action[0]][col] = MIDDLE
            if board.matrix[action[0]][action[1] + action[2] - 1] == EMPTY_SPACE:
                board.columns[action[1] + action[2] - 1] -= 1
                board.rows[action[0]] -= 1
            board.matrix[action[0]][action[1] + action[2] - 1] = RIGHT
            for row in range(action[0] - 1, action[0] + 2):
                for col in range(action[1] - 1, action[1] + action[2] + 1):
                    if row >= 0 and row < 10 and col >= 0 and col < 10 and not ( row == action[0] and action[1] <= col <= action[1] + action[2] - 1):
                        if board.matrix[row][col] == EMPTY_SPACE:
                            board.matrix[row][col] = WATER
            board.pieces[action[2] - 1] -= 1
        
        elif action[3] == VERTICAL:
            if board.matrix[action[0]][action[1]] == EMPTY_SPACE:
                board.columns[action[1]] -= 1
                board.rows[action[0]] -= 1
            board.matrix[action[0]][action[1]] = TOP
            for row in range(action[0]+1, action[0] + action[2] - 1):
                if board.matrix[row][action[1]] == EMPTY_SPACE:
                    board.columns[action[1]] -= 1
                    board.rows[row] -= 1
                board.matrix[row][action[1]] = MIDDLE
            if board.matrix[action[0] + action[2] - 1][action[1]] == EMPTY_SPACE:
                board.columns[action[1]] -= 1
                board.rows[action[0] + action[2] - 1] -= 1
            board.matrix[action[0] + action[2] - 1][action[1]] = BOTTOM
            for row in range(action[0] - 1, action[0] + action[2] + 1):
                for col in range(action[1] - 1, action[1] + 2):
                    if row >= 0 and row < 10 and col >= 0 and col < 10 and not ( action[0] <= row <= action[0] + action[2] - 1 and col == action[1]):
                        if board.matrix[row][col] == EMPTY_SPACE:
                            board.matrix[row][col] = WATER
            board.pieces[action[2] - 1] -= 1
            
        board.check_up()
                         
        return BimaruState(board) 

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        if not np.any(state.board.rows) or not np.any(state.board.columns):
            if np.any(state.board.pieces):
                return False
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
    
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    
    goal_node = depth_first_tree_search(problem)
    
    if goal_node is not None:
        print("Is goal? ", problem.goal_test(goal_node.state))
        print("Solution:")
        print(goal_node.state.board.print())
    



