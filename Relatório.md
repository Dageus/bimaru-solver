# Relatório

## Introdução

O projeto em desenvolvimento consiste em usar um algoritmo que utiliza uma árvore de decisões para chegar à solução de um problema denominado Bimaru.

O Bimaru é um jogo de lógica que consiste em preencher uma matriz de dimensões N x N com barcos de tamanhos variados, de forma que cada barco ocupe um número de células igual ao seu tamanho e que não existam barcos adjacentes, nem mesmo na diagonal. Além disso, cada linha e cada coluna da matriz deve conter um número de barcos igual ao indicado na sua margem. Existe um número limitado de barcos de cada tamanho. O objetivo do jogo é preencher a matriz de forma a satisfazer todas as restrições, não deixando nenhuma linha nem coluna por preencher.

## Desenvolvimento

Após uma leitura do enunciado e olhar para o os exemplos dados e o código fonte fornecido, pensamos que o enunciado nos estava a levar a uma forma específica para resolver o problema,
por exemplo:

1. nos exemplos dados, era usada a função ```get_value(row, col)``` para se obter que valor estava numa certa célula; mas reparamos logo uma abstração a esse nível não era necessária, pois o tabuleiro era uma matriz de inteiros, logo bastava usar ```matrix[row][col]```;

1. adicionalmente, a função ```actions()``` devolvia uma lista de tuplos, em que cada tuplo representava a ação de preencher uma célula; mas após falar com colegas e falar com o professor das práticas chegamos à conclusão que este tipo de abordagem ao preenchimento de barcos não tornaria o processo muito mais complicado, mas também mais ineficiente; então assumimos que a função ```actions()``` devia devolver uma lista de listas, em que cada lista representava uma ação de preencher um barco, quebrando assim ramos na futura árvore de decisões que levariam a possibilidades erradas;

1. por último, após ver nos exemplos dados que não era utilizada lógica para preencher o tabuleiro, iniciamos o projeto puramente com uma abordagem de força bruta, em que se testava todas as possibilidades de preenchimento do tabuleiro, e se não fosse possível preencher o tabuleiro com as restrições dadas, então o programa devolvia ```None```;
Verificá-mos depois que esta noção estava errada, e que o ato de preencher o tabuleiro com lógica tornava o processo muito mais eficiente, ao ponto de tabuleiros mais simples nem necessitarem da árvore para serem resolvidos, e que a árvore de decisões era apenas necessária para tabuleiros mais complexos;

## Estrutura das classes

No nosso projeto, temos 3 classes principais:

1. ```BimaruState```: esta classe representa o estado do tabuleiro num certo momento, e contém as funções dadas no enunciado, tal como umas funções adicionadas pelo nosso grupo, para facilirar o preenchiment

## Explicação do código

### Preenchimento inicial do tabuleiro

O preenchimento inicial do tabuleiro é feito pela função ```post_parse()``` e pela função ```check_up()```;

A função ```post_parse()``` é responsável por, após a leitura do ficheiro de input, preencher todas as hints dadas com um contorno de água onde é necessário, e caso seja uma hint que implique a existência de mais peças ao seu lado, como L, R, T, B, são colocadas peças de barco auxiliares nas posições corretas de forma a facilitar o preenchimento do tabuleiro;

A função ```check_up()``` é responsável por analisar as linhas e colunas e verificar se há barcos que possam ser completos com a informação dada no input, quer seja completando uma linha ou coluna inteira com águas porque o seu valor é 0, ou completando um barco que já esteja acabado graças à informação dada na linha e coluna (ex.: um barco ser de tamanho 3 porque só há 3 espaços possiveis nessa linha, pois o resto são águas, e porque o valor da linha é 3);
Esta função também implica o preenchimento de água após a conclusão de um barco, pois se um barco está completo, todas as diagonais de cada peça do barco são águas;

### Preenchimento do tabuleiro com peças corretas

Apesar das funções ```post_parse()``` e ```check_up()``` preencherem o tabuleiro com peças corretas, o seu valor é desconhecido, pois são preenchidas com o valor 'O', que representa uma peça de barco auxiliar, e não uma peça de barco normal;

Logo, para se preencher os barcos corretamente e retirar-se a uma lista previamente feita com o número de peças de cada barco que ainda faltam preencher, é necessário usar a função ```complete_boats()``` que pertence à classe ```BimaruState```;