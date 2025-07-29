import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randrange
import threading
from colorama import Fore
from colorama import init as colorama_init
from time import time

colorama_init(autoreset=True)
rubik_cube = list()
solved_cube = list()


def faces(num_faces: str, face: str, translate: list, rotate: list, color_1="white", color_2="blue", color_3="white",
          color_line="black"):

#     Desenha uma, duas ou três faces conectadas de um cubo 3D com cores e bordas especificadas.
    
#     Parâmetros:
#     - num_faces: "one", "two" ou "three" → quantas arestas desenhar
#     - face: "ONE", "TWO" ou "THREE" → quantas e quais faces preencher com cor
#     - translate: [x, y, z] → posição do objeto
#     - rotate: [ângulo, eixo_x, eixo_y, eixo_z] → rotação do objeto
#     - color_1, color_2, color_3: cores para até 3 faces
#     - color_line: cor das bordas (linhas)
#     """

    # Vértices de um cubo base (usado para montar faces)
    facesbuff = (
        (1, -1, -1),
        (1, 1, -1),
        (1, 1, 1),
        (1, -1, 1),
        (-1, -1, 1),
        (-1, 1, 1),
        (-1, 1, -1)
    )

    # Pares de vértices que formam as linhas/bordas
    facesbordbuff = (
        (0, 1),
        (0, 3),
        (2, 3),
        (2, 1),   # Face 1
        (2, 5),
        (3, 4),
        (5, 4),   # Face 2
        (5, 6),
        (6, 1)    # Face 3
    )

    # Conjunto de 3 faces do cubo, cada uma com 4 vértices
    insidefaces = (
        (0, 3, 2, 1),   # Face 1
        (2, 3, 4, 5),   # Face 2
        (1, 2, 5, 6)    # Face 3
    )

    # Mapas de nome para quantidade de linhas/faces a desenhar
    numface = {"one": 4, "two": 7, "three": 10, "ONE": 0, "TWO": 1, "THREE": 2}

    # Mapeamento de cores para RGB
    pair_colors = {
        "white": (1, 1, 1),
        "blue": (0, 0, 1),
        "red": (1, 0.2, 0.3),
        "orange": (1, 0.5, 0.1),
        "green": (0, 1, 0),
        "yellow": (1, 1, 0),
        "black": (0, 0, 0)
    }

    # Posiciona o objeto na tela
    glTranslated(translate[0], translate[1], translate[2])

    # Rotaciona o objeto no espaço 3D
    glRotated(rotate[0], rotate[1], rotate[2], rotate[3])

    # Inicia o desenho das faces (polígonos de 4 lados)
    glBegin(GL_QUADS)
    
    if face == "ONE":
        # Desenha apenas a primeira face com color_1
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
    
    elif face == "TWO":
        # Desenha a primeira face com color_1
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        # Desenha a segunda face com color_2
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])

    elif face == "THREE":
        # Primeira face
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        # Segunda face
        for vertex in insidefaces[numface.get("TWO")]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])
        # Terceira face
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_3))
            glVertex3fv(facesbuff[vertex])
    
    glEnd()  # Fim do desenho das faces

    # Inicia o desenho das bordas (linhas entre os vértices)
    glBegin(GL_LINES)
    count = 0
    for line in facesbordbuff:
        if count < numface.get(num_faces):  # Desenha só a quantidade de linhas necessárias
            for point in line:
                glColor3fv(pair_colors.get(color_line))
                glVertex3fv(facesbuff[point])
            count += 1
        else:
            break
    glEnd()  # Fim do desenho das bordas

    # Desfaz a rotação para não afetar outros objetos
    glRotated(-rotate[0], rotate[1], rotate[2], rotate[3])
    # Obs: a translação também poderia ser desfeita, mas foi comentada:
    # glTranslated(-translate[0], -translate[1], -translate[2])


def faces_pos(num_faces: str, face: str, translate: list, rotate: list, color_1="white", color_2="blue",
              color_3="white", color_line="black"):
    #Adjust rotation of faces on the screen

    # Aplica a translação e rotação e desenha as faces com as cores definidas
    faces(num_faces, face, translate, rotate, color_1, color_2, color_3, color_line)

    # Desfaz a rotação para que objetos seguintes não sejam afetados
    glTranslated(-translate[0], -translate[1], -translate[2])


def f_layer(layer: list):
    """Cria a primeira camada (superior) do cubo mágico com 9 blocos (cubies)."""

    # 1º cubie (canto frontal esquerdo) - desenha 3 faces: topo (white), frente (blue), esquerda (white)
    faces_pos("three", "THREE", [0, 3, 0], [90, 0, -1, 0], layer[0][0], layer[0][1], layer[0][2])

    # 2º cubie (borda frontal) - desenha 2 faces: topo (white), frente (blue)
    faces_pos("two", "TWO", [2, 3, 0], [90, 0, 0, 1], layer[1][0], layer[1][1])

    # 3º cubie (canto frontal direito) - desenha 3 faces: topo, frente, direita
    faces_pos("three", "THREE", [4, 3, 0], [0, 0, 0, 0], layer[2][0], layer[2][1], layer[2][2])

    # 4º cubie (borda direita) - desenha 2 faces: topo, direita
    faces_pos("two", "TWO", [4, 3, -2], [90, -1, 0, 0], layer[3][0], layer[3][1])

    # 5º cubie (canto traseiro direito) - desenha 3 faces: topo, direita, trás
    faces_pos("three", "THREE", [4, 3, -4], [90, -1, 0, 0], layer[4][0], layer[4][1], layer[4][2])

    # 6º cubie (borda traseira) - desenha 2 faces: topo, trás
    faces_pos("two", "TWO", [2, 3, -4], [180, 1, 1, 0], layer[5][0], layer[5][1])

    # 7º cubie (canto traseiro esquerdo) - desenha 3 faces: topo, trás, esquerda
    faces_pos("three", "THREE", [0, 3, -4], [180, 0, -1, 0], layer[6][0], layer[6][1], layer[6][2])

    # 8º cubie (borda esquerda) - desenha 2 faces: topo, esquerda
    faces_pos("two", "TWO", [0, 3, -2], [180, 0, 1, 1], layer[7][0], layer[7][1])

    # 9º cubie (meio da camada) - desenha apenas a face de cima
    faces_pos("one", "ONE", [2, 3, -2], [180, 1, 1, 0], layer[8][0])

def s_layer(layer: list):
    """Cria a segunda camada (camada do meio) do cubo mágico com 8 blocos (cubies)."""

     # 1º cubie (frente-esquerda, sem a face de cima) - desenha 2 faces: frente e esquerda
    faces_pos("two", "TWO", [0, 1, 0], [90, 0, -1, 0], layer[0][0], layer[0][1])

    # 2º cubie (frente-centro) - desenha apenas a face frontal
    faces_pos("one", "ONE", [2, 1, 2], [90, 0, 1, 0], layer[1][0])

     # 3º cubie (frente-direita) - desenha 2 faces: frente e direita
    faces_pos("two", "TWO", [4, 1, 0], [180, 1, 0, 1], layer[2][0], layer[2][1])

    # 4º cubie (direita-centro) - desenha apenas a face direita
    faces_pos("one", "ONE", [4, 1, -2], [0, 0, 0, 0], layer[3][0])

    # 5º cubie (traseira-direita) - desenha 2 faces: trás e direita
    faces_pos("two", "TWO", [4, 1, -4], [90, 0, 1, 0], layer[4][0], layer[4][1])

    # 6º cubie (trás-centro) - desenha apenas a face de trás
    faces_pos("one", "ONE", [2, 1, -4], [90, 0, 1, 0], layer[5][0])

    # 7º cubie (trás-esquerda) - desenha 2 faces: trás e esquerda
    faces_pos("two", "TWO", [0, 1, -4], [180, 1, 0, -1], layer[6][0], layer[6][1])

    # 8º cubie (esquerda-centro) - desenha apenas a face esquerda
    faces_pos("one", "ONE", [-2, 1, -2], [0, 0, 0, 0], layer[7][0])

def t_layer(layer: list):
    """Cria a terceira camada (inferior) do cubo mágico com 9 blocos (cubies)."""

    # 1º cubie (canto frontal esquerdo) - desenha 3 faces: baixo, frente, esquerda
    faces_pos("three", "THREE", [0, -1, 0], [180, 0, 0, 1], layer[0][0], layer[0][1], layer[0][2])

    # 2º cubie (borda frontal) - desenha 2 faces: baixo e frente
    faces_pos("two", "TWO", [2, -1, 0], [90, 0, 0, -1], layer[1][0], layer[1][1])

    # 3º cubie (canto frontal direito) - desenha 3 faces: baixo, frente, direita
    faces_pos("three", "THREE", [4, -1, 0], [90, 0, 0, -1], layer[2][0], layer[2][1], layer[2][2])

    # 4º cubie (borda direita) - desenha 2 faces: baixo e direita
    faces_pos("two", "TWO", [4, -1, -2], [90, 1, 0, 0], layer[3][0], layer[3][1])

    # 5º cubie (canto traseiro direito) - desenha 3 faces: baixo, direita, trás
    faces_pos("three", "THREE", [4, -1, -4], [180, -100, -1, 0], layer[4][0], layer[4][1], layer[4][2])

    # 6º cubie (borda traseira) - desenha 2 faces: baixo e trás
    faces_pos("two", "TWO", [2, -1, -4], [180, -100, 100, -1], layer[5][0], layer[5][1])

    # 7º cubie (canto traseiro esquerdo) - desenha 3 faces: baixo, trás, esquerda
    faces_pos("three", "THREE", [0, -1, -4], [180, -1, 1, 0], layer[6][0], layer[6][1], layer[6][2])

    # 8º cubie (borda esquerda) - desenha 2 faces: baixo e esquerda
    faces_pos("two", "TWO", [0, -1, -2], [180, 0, -100, 100], layer[7][0], layer[7][1])

    # 9º cubie (meio da camada inferior) - desenha apenas a face inferior
    faces_pos("one", "ONE", [2, -3, -2], [90, 0, -1, 100], layer[8][0])


def u_first_move(cube: list):
    """Executa um movimento na camada superior (U - Up), atualiza a posição das peças e retorna o novo estado do cubo"""

    temp_cube = list()  # Lista temporária para armazenar o novo estado dos cubies após a rotação
    count = 0           # Contador para rastrear a posição atual no loop

    # Etapa 1: Reorganizar individualmente os elementos dos cubies, dependendo da sua posição
    for face in cube:
        # Se o cubie tem duas cores e está entre os primeiros 9 (ou seja, na camada superior)
        if len(face) == 2 and 0 <= count < 9:
            # Inverte a ordem das cores (por exemplo: [azul, branco] vira [branco, azul])
            temp_cube.append([face[1], face[0]])

        # Se estiver na posição 2 e o cubie tiver 3 cores (canto)
        elif count == 2:
            # Reordena as cores em novo padrão (por exemplo: [a, b, c] → [b, c, a])
            temp_cube.append([face[1], face[2], face[0]])

        # Se estiver na posição 4 (outro canto)
        elif count == 4:
            # Reorganiza também, mas com ordem diferente (por exemplo: [a, b, c] → [c, a, b])
            temp_cube.append([face[2], face[0], face[1]])

        else:
            # Para os demais cubies, mantém a ordem original
            temp_cube.append(face)

        count += 1  # Atualiza a posição

    # Etapa 2: Troca de posições dos cubies da camada superior (simula rotação da face de cima)

    # Troca em cruz: 0 → 2 → 4 → 6 → 0
    temp_0 = temp_cube[0]
    temp_cube[0] = temp_cube[6]
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_0
    temp_4 = temp_cube[4]
    temp_cube[4] = temp_2
    temp_cube[6] = temp_4

    # Troca em cruz dos cubies entre os cantos: 1 → 3 → 5 → 7 → 1
    temp_1 = temp_cube[1]
    temp_cube[1] = temp_cube[7]
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_1
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_3
    temp_cube[7] = temp_5

    # Retorna o novo estado da camada superior com as cores e posições atualizadas
    return temp_cube


def u_move(cube: list):
    """Executa o movimento U (Up) no cubo — gira a camada superior no sentido horário 
    e retorna o cubo com a nova posição das peças"""

    temp_cube = list()  # Lista para armazenar temporariamente os cubies modificados
    count = 0           # Contador para saber em que posição do cubo estamos

    # Etapa 1: Reorganizar individualmente as cores dos cubies da camada superior
    for face in cube:
        # Se for um cubie com 2 cores e estiver entre os 9 primeiros (camada superior)
        if len(face) == 2 and 0 <= count < 9:
            # Inverte a ordem das cores (por exemplo: [azul, branco] → [branco, azul])
            temp_cube.append([face[1], face[0]])

        # Cubie de 3 cores na posição 2 (um dos cantos da camada superior)
        elif count == 2:
            # Mantém a mesma ordem das cores (possivelmente já na ordem desejada)
            temp_cube.append([face[0], face[1], face[2]])

        # Cubie de 3 cores na posição 4 (outro canto)
        elif count == 4:
            # Reorganiza as cores (exemplo: [a, b, c] → [c, a, b])
            temp_cube.append([face[2], face[0], face[1]])

        # Cubie de 3 cores na posição 6 (outro canto)
        elif count == 6:
            # Reorganiza as cores (exemplo: [a, b, c] → [b, c, a])
            temp_cube.append([face[1], face[2], face[0]])

        else:
            # Para os demais cubies, mantém a ordem original
            temp_cube.append(face)

        count += 1  # Avança para a próxima posição

    # Etapa 2: Trocar a posição dos cubies da camada superior para simular a rotação da face de cima

    # Movimento dos cantos (em sentido horário):
    # Posição 6 → 4 → 2 → 0 → 6
    temp_6 = temp_cube[6]
    temp_cube[6] = temp_cube[0]
    temp_4 = temp_cube[4]
    temp_cube[4] = temp_6
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_4
    temp_cube[0] = temp_2

    # Movimento das arestas (entre os cantos), também em sentido horário:
    # Posição 7 → 5 → 3 → 1 → 7
    temp_7 = temp_cube[7]
    temp_cube[7] = temp_cube[1]
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_7
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_5
    temp_cube[1] = temp_3

    # Retorna o cubo com a nova configuração da camada superior
    return temp_cube

def r_move(cube: list):
    """Pega o cubo, faz um movimento e devolve-o com a posição atualizada.

Esta função executa um movimento em "R" (face direita no sentido horário) no cubo.
Ela rotaciona tanto as posições externas (troca de cubos) quanto as orientações internas (reorganização de cores) das faces afetadas.
    """

    temp_cube = list()  # Lista temporária para armazenar as faces modificadas
    temp_pos = list()  
    count = 0           # Contador para saber em qual face estamos no loop

    for face in cube:
        # Ajusta a ordem das cores em algumas faces para simular a rotação dos cubos
        if count in (11, 20, 13, 3):  # Faces que precisam de inversão de ordem de 2 elementos
            temp_cube.append([face[1], face[0]])

        elif count == 19:  # Reorganiza uma face de 3 cores para simular rotação do cubo em R
            temp_cube.append([face[2], face[0], face[1]])

        elif count == 4:  # Mantém a mesma ordem das 3 cores
            temp_cube.append([face[0], face[1], face[2]])

        elif count == 21:  # Rotaciona as cores para simular o cubo virando
            temp_cube.append([face[1], face[2], face[0]])

        else:  # As demais faces permanecem inalteradas
            temp_cube.append(face)

        count += 1

    # Troca entre 4 faces: 2 → 19 → 21 → 4 → 2
    # Essas são faces maiores (3 cores), e representam provavelmente os blocos centrais da face R
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_cube[19]
    temp_cube[19] = temp_cube[21]
    temp_cube[21] = temp_cube[4]
    temp_cube[4] = temp_2

    # Troca entre 4 faces de 2 cores: 3 → 11 → 20 → 13 → 3
    # Representam arestas e cantos da face R
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_cube[11]
    temp_cube[11] = temp_cube[20]
    temp_cube[20] = temp_cube[13]
    temp_cube[13] = temp_3

    return temp_cube  # Retorna o novo estado do cubo após o movimento R


    """
    Executa o movimento L (Left) — gira a face da esquerda no sentido horário.
    """

    temp_cube = []
    count = 0

    # Primeiro, copia todas as faces para evitar índice fora de alcance
    for face in cube:
        temp_cube.append(face[:])  # Cópia da face (evita referência direta)
        count += 1

    # Agora, reorganiza as orientações das peças
    if len(temp_cube[1]) == 2:
        temp_cube[1] = [temp_cube[1][1], temp_cube[1][0]]
    if len(temp_cube[9]) == 2:
        temp_cube[9] = [temp_cube[9][1], temp_cube[9][0]]
    if len(temp_cube[27]) == 2:
        temp_cube[27] = [temp_cube[27][1], temp_cube[27][0]]
    if len(temp_cube[38]) == 2:
        temp_cube[38] = [temp_cube[38][1], temp_cube[38][0]]

    if len(temp_cube[0]) == 3:
        temp_cube[0] = [temp_cube[0][2], temp_cube[0][0], temp_cube[0][1]]
    if len(temp_cube[6]) == 3:
        temp_cube[6] = [temp_cube[6][1], temp_cube[6][2], temp_cube[6][0]]
    if len(temp_cube[18]) == 3:
        temp_cube[18] = [temp_cube[18][0], temp_cube[18][1], temp_cube[18][2]]
    if len(temp_cube[36]) == 3:
        temp_cube[36] = [temp_cube[36][1], temp_cube[36][2], temp_cube[36][0]]

    # Agora faz as trocas de posições
    temp_0 = temp_cube[0]
    temp_18 = temp_cube[18]
    temp_6 = temp_cube[6]
    temp_36 = temp_cube[36]

    temp_cube[0] = temp_18
    temp_cube[18] = temp_6
    temp_cube[6] = temp_36
    temp_cube[36] = temp_0

    temp_1 = temp_cube[1]
    temp_9 = temp_cube[9]
    temp_27 = temp_cube[27]
    temp_38 = temp_cube[38]

    temp_cube[1] = temp_9
    temp_cube[9] = temp_27
    temp_cube[27] = temp_38
    temp_cube[38] = temp_1

    return temp_cube

def m_move(cube: list):
    """Pega o cubo, faz um movimento e devolve-o com a posição atualizada.

Esta função executa um movimento em "M" (camada do meio, corte vertical entre E e D, girando como a face E no sentido horário).
Ela atualiza as posições e orientações do cubo e, em seguida, aplica uma rotação em Z para alinhamento visual."""

    temp_cube = list()  # Lista temporária para armazenar as novas faces do cubo
    temp_pos = list()   
    count = 0           # Contador de índice da face atual

    # Primeiro, ajustamos a orientação (ordem) das cores de algumas peças específicas
    for face in cube:
        if count in (1, 5, 18, 22):  # Essas peças precisam ter suas cores invertidas
            temp_cube.append([face[1], face[0]])  # Inversão de dois elementos
        else:
            temp_cube.append(face)  # Mantém a face inalterada
        count += 1

    # Agora, trocamos as posições dos cubos da camada do meio (M layer)

    # Etapa 1: salvar temporariamente valores que serão sobrescritos
    temp_1 = temp_cube[1]
    temp_8 = temp_cube[8]

    # Etapa 2: executar a rotação dos cubinhos da camada M no sentido do L (horário olhando de trás para frente)
    temp_cube[1]  = temp_cube[5]
    temp_cube[8]  = temp_cube[14]
    temp_cube[5]  = temp_cube[22]
    temp_cube[14] = temp_cube[25]
    temp_cube[22] = temp_cube[18]
    temp_cube[25] = temp_cube[10]
    temp_cube[18] = temp_1
    temp_cube[10] = temp_8

    # Etapa 3: aplicar uma rotação visual Z (giro do cubo inteiro no eixo Z)
    temp_cube = z_move(temp_cube)

    return temp_cube  # Retorna o novo estado do cubo após o movimento M


def m_first_move(cube: list):
    """
    Executa o primeiro movimento da camada do meio (M layer) e retorna o cubo com as posições atualizadas.

    Esta função simula uma rotação da camada do meio (central vertical), semelhante ao movimento da face L no sentido horário.
    Também aplica uma rotação no eixo Z ao final para alinhar visualmente o cubo.
    """

    temp_cube = list()  # Lista temporária para armazenar as faces modificadas
    temp_pos = list()   # (não utilizada, provavelmente deixada por hábito ou para uso futuro)
    count = 0           # Contador para rastrear o índice da face no loop

    # Etapa 1: inverter a orientação de algumas peças específicas
    for face in cube:
        if count in (1, 5, 18, 22):  # Peças da camada do meio que precisam de inversão de cores
            temp_cube.append([face[1], face[0]])  # Inversão da ordem das duas cores
        else:
            temp_cube.append(face)  # Peças que permanecem com as cores originais
        count += 1

    # Etapa 2: troca de posição dos cubies centrais da camada do meio

    # Salva valores temporariamente antes da troca em cascata
    temp_5 = temp_cube[5]
    temp_14 = temp_cube[14]
    temp_22 = temp_cube[22]
    temp_25 = temp_cube[25]
    temp_18 = temp_cube[18]
    temp_10 = temp_cube[10]

    # Executa a rotação dos cubies da camada do meio (em sentido horário olhando da frente)
    temp_cube[5]  = temp_cube[1]   # 1 → 5
    temp_cube[14] = temp_cube[8]   # 8 → 14
    temp_cube[22] = temp_5         # 5 → 22
    temp_cube[25] = temp_14        # 14 → 25
    temp_cube[18] = temp_22        # 22 → 18
    temp_cube[10] = temp_25        # 25 → 10
    temp_cube[1]  = temp_18        # 18 → 1
    temp_cube[8]  = temp_10        # 10 → 8

    # Etapa 3: aplica uma rotação no eixo Z (gira o cubo inteiro para manter a orientação visual coerente)
    temp_cube = z_move(temp_cube)

    return temp_cube  # Retorna o cubo com a nova configuração da camada M


def e_move(cube: list):
    """Executa o movimento 'E' (Edge Middle Layer Clockwise).
    Move as peças da camada do meio horizontal no sentido horário, quando vista de cima."""

    temp_cube = list()
    count = 0

    # Clona o cubo e inverte a ordem das cores em algumas peças da camada do meio (índices 9, 11, 13, 15)
    for face in cube:
        if count in (9, 11, 13, 15):
            # Inverte as duas cores (normalmente laterais) — útil para manter orientação
            temp_cube.append([face[1], face[0]])
        else:
            # Copia as outras peças como estão
            temp_cube.append(face)
        count += 1

    # Rotaciona as peças da camada do meio (índices 9 a 16) como se fosse um giro entre 4 faces
    temp_9 = temp_cube[9]
    temp_10 = temp_cube[10]
    temp_11 = temp_cube[11]

    # Atribui nova posição girando os valores
    temp_cube[9] = temp_cube[11]
    temp_cube[10] = temp_cube[12]
    temp_cube[11] = temp_cube[13]
    temp_cube[12] = temp_cube[14]
    temp_cube[13] = temp_cube[15]
    temp_cube[14] = temp_cube[16]
    temp_cube[15] = temp_9
    temp_cube[16] = temp_10

    return temp_cube


def d_move(cube: list):
    """
    Executa o movimento da face D (Down/baixo) do cubo.
    Retorna o cubo atualizado com a rotação da camada inferior.
    """

    temp_cube = list()  # Lista para armazenar o novo estado do cubo após as alterações
    temp_pos = list()   
    count = 0           # Contador de índice da face atual no cubo

    # Etapa 1: processar as faces uma por uma, girando/invertendo algumas peças específicas
    for face in cube:
        if count in (18, 20, 22, 24):
            # Inverte a ordem dos dois elementos (como uma peça de canto ou aresta)
            temp_cube.append([face[1], face[0]])
        elif count == 19:
            # Rotaciona 3 elementos da peça (posição 19): 1º → 2º, 2º → 3º, 3º → 1º
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 21:
            # Rotação para a direita: 1º → 2º, 2º → 3º, 3º → 1º
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 23:
            # Mesma rotação do caso de cima
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 17:
            # Rotação para a esquerda (3 elementos)
            temp_cube.append([face[2], face[0], face[1]])
        else:
            # Para outras posições, mantém a face como está
            temp_cube.append(face)
        count += 1

    # Etapa 2: rotacionar as peças centrais da face D

    # Primeiro grupo de peças da face inferior (cantos/arestas internos)
    temp_17 = temp_cube[17]
    temp_cube[17] = temp_cube[19]
    temp_cube[19] = temp_cube[21]
    temp_cube[21] = temp_cube[23]
    temp_cube[23] = temp_17

    # Segundo grupo de peças da borda inferior
    temp_18 = temp_cube[18]
    temp_cube[18] = temp_cube[20]
    temp_cube[20] = temp_cube[22]
    temp_cube[22] = temp_cube[24]
    temp_cube[24] = temp_18

    return temp_cube  # Retorna o cubo atualizado após o movimento D


def x_first_move(cube: list):#replicar para os demais movimentos de rotação do cubo
    """
    Rotaciona o cubo no eixo X (como se girasse para colocar a face lateral na parte superior),
    reorganizando posições e orientações das peças para simular esse giro.
    """

    temp_cube = list()  # Novo estado do cubo após a rotação
    temp_pos = list()   
    count = 0           # Índice para rastrear a posição atual

    # Etapa 1: ajustar orientação das peças afetadas pela rotação
    for face in cube:
        if len(face) == 2:
            # Se for uma aresta com 2 cores, inverter ordem
            temp_cube.append([face[1], face[0]])
        elif count in (0, 17, 2):
            # Rotação para direita (peças de canto)
            temp_cube.append([face[1], face[2], face[0]])
        elif count in (6, 23, 19):
            # Rotação para esquerda (peças de canto)
            temp_cube.append([face[2], face[0], face[1]])
        else:
            # Sem rotação para as demais peças
            temp_cube.append(face)
        count += 1

    # Etapa 2: trocas de posição simulando a rotação no eixo X

    # Camada central (peças centrais girando)
    temp_10 = temp_cube[10]
    temp_cube[10] = temp_cube[8]
    temp_cube[8] = temp_cube[14]
    temp_cube[14] = temp_cube[25]
    temp_cube[25] = temp_10

    temp_18 = temp_cube[18]
    temp_cube[18] = temp_cube[1]
    temp_cube[1] = temp_cube[5]
    temp_cube[5] = temp_cube[22]
    temp_cube[22] = temp_18

    # Troca das peças das bordas do cubo (arestas e cantos)

    temp_19 = temp_cube[19]
    temp_cube[19] = temp_cube[2]
    temp_cube[2] = temp_cube[4]
    temp_cube[4] = temp_cube[21]
    temp_cube[21] = temp_19

    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[3]
    temp_cube[3] = temp_cube[13]
    temp_cube[13] = temp_cube[20]
    temp_cube[20] = temp_11

    temp_17 = temp_cube[17]
    temp_cube[17] = temp_cube[0]
    temp_cube[0] = temp_cube[6]
    temp_cube[6] = temp_cube[23]
    temp_cube[23] = temp_17

    temp_9 = temp_cube[9]
    temp_cube[9] = temp_cube[7]
    temp_cube[7] = temp_cube[15]
    temp_cube[15] = temp_cube[24]
    temp_cube[24] = temp_9

    return temp_cube  # Retorna o cubo rotacionado no eixo X


def z_move(cube: list):
    """
    Rotaciona o cubo no eixo Z (como se girasse o cubo olhando de cima para baixo),
    colocando uma das faces laterais no topo. Isso altera as posições e orientações
    das peças do cubo para simular esse movimento.
    """

    temp_cube = list()  # Novo estado do cubo após a rotação
    temp_pos = list()   
    count = 0

    # Etapa 1: ajustar orientação das peças rotacionadas
    for face in cube:
        if len(face) == 2:
            # Arestas com duas cores: inverte a ordem
            temp_cube.append([face[1], face[0]])
        elif count == 17:
            # Peça de canto girada sentido horário
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 0:
            # Peça de canto girada sentido anti-horário
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 4:
            # Outra peça de canto (horário)
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 6:
            # Outra peça de canto (anti-horário)
            temp_cube.append([face[2], face[0], face[1]])
        else:
            # Peças não afetadas
            temp_cube.append(face)
        count += 1

    # Etapa 2: trocar as posições das peças simulando rotação no eixo Z

    # Centro superior
    temp_12 = temp_cube[12]
    temp_cube[12] = temp_cube[8]
    temp_cube[8] = temp_cube[16]
    temp_cube[16] = temp_cube[25]
    temp_cube[25] = temp_12

    # Arestas centrais superiores
    temp_20 = temp_cube[20]
    temp_cube[20] = temp_cube[3]
    temp_cube[3] = temp_cube[7]
    temp_cube[7] = temp_cube[24]
    temp_cube[24] = temp_20

    # Arestas da direita
    temp_21 = temp_cube[21]
    temp_cube[21] = temp_cube[4]
    temp_cube[4] = temp_cube[6]
    temp_cube[6] = temp_cube[23]
    temp_cube[23] = temp_21

    # Centro da direita
    temp_13 = temp_cube[13]
    temp_cube[13] = temp_cube[5]
    temp_cube[5] = temp_cube[15]
    temp_cube[15] = temp_cube[22]
    temp_cube[22] = temp_13

    # Arestas da esquerda
    temp_19 = temp_cube[19]
    temp_cube[19] = temp_cube[2]
    temp_cube[2] = temp_cube[0]
    temp_cube[0] = temp_cube[17]
    temp_cube[17] = temp_19

    # Centro da esquerda
    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[1]
    temp_cube[1] = temp_cube[9]
    temp_cube[9] = temp_cube[18]
    temp_cube[18] = temp_11

    return temp_cube  # Retorna o cubo com a rotação aplicada no eixo Z


    """Print on the screen how many times is shuffling the cube"""

    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def shuffle(cycle, cube: list):
    """Embaralha o cubo com movimentos aleatórios"""
    moves = [u_move, u_first_move, z_move, x_first_move, e_move]  # adicione mais se quiser
    for _ in range(cycle):
        move = random.choice(moves)
        cube = move(cube)
    return cube


def main():
    """Função principal que inicializa o cubo mágico, interface gráfica e eventos de interação."""

    # Definição manual das três camadas do cubo
    # Cada elemento representa uma face (adesivo) do cubo
    first_layer = [["orange", "blue", "white"], ["white", "orange"], ["green", "orange", "white"],
                   ["green", "white"], ["green", "white", "red"], ["white", "red"], ["blue", "red", "white"],
                   ["blue", "white"], ["white"]]

    second_layer = [["orange", "blue"], ["orange"], ["orange", "green"], ["green"], ["red", "green"],
                    ["red"], ["red", "blue"], ["blue"]]

    third_layer = [["blue", "orange", "yellow"], ["yellow", "orange"], ["yellow", "orange", "green"],
                   ["green", "yellow"], ["green", "red", "yellow"], ["yellow", "red"], ["yellow", "red", "blue"],
                   ["blue", "yellow"], ["yellow"]]

    # Constrói o cubo unindo todas as camadas na lista `rubik_cube`
    global rubik_cube
    global solved_cube
    for layer in (first_layer, second_layer, third_layer):
        for face in layer:
            rubik_cube.append(face)
    
    # Salva o estado resolvido como referência
    solved_cube = rubik_cube

    # Inicialização do Pygame
    pygame.init()
    pygame.font.init()
    display = (800, 600)  # Tamanho da janela

    # Criação da janela com suporte a OpenGL
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    # Ícone da janela
    icon = pygame.image.load('rubik.png')
    pygame.display.set_icon(icon)

    # Fonte usada para textos
    font = pygame.font.SysFont('lucinda console', 64)

    # Título da janela
    pygame.display.set_caption("Rubik Cube")

    # Configuração da câmera 3D com perspectiva
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Translação para afastar a câmera e posicioná-la
    glTranslatef(6.0, -1.0, -20)

    # Rotação inicial da visão para ver o cubo em perspectiva
    glRotatef(45, 1, 1, 1)

    # Ativa o teste de profundidade (z-buffer) para renderização correta
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Variáveis de controle para detectar teclas pressionadas
    u_first_key = False
    u_key = False
    r_key = False
    m_key = False
    m_first_key = False
    z_key = False
    x_first_key = False
    shuffle_key = False
    sexy_key = False
    first_white_key = False

    cycle = 0  # Ciclos de embaralhamento
    m = 1  # Variável auxiliar
    prev_pos_x = 0  # Posição anterior do mouse
    prev_pos_y = 0

    # Loop principal do programa
    while True:
        # Captura eventos do teclado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Rotaciona a câmera para esquerda
                if event.key == pygame.K_g:
                    glRotatef(20, 0, -1, 0)
                # Rotaciona a câmera para direita
                if event.key == pygame.K_f:
                    glRotatef(20, 0, 1, 0)
                # Rotaciona a câmera para cima
                if event.key == pygame.K_d:
                    glRotatef(90, 1, 0, 0)
                # Sai do programa
                if event.key == pygame.K_ESCAPE:
                    exit()

                # Movimentos do cubo
                if event.key == pygame.K_g:
                    u_first_key = True
                if event.key == pygame.K_h:
                    u_key = True
                if event.key == pygame.K_r:
                    r_key = True
                # L move (camada esquerda)
                if event.key == pygame.K_l:
                    rubik_cube = l_move(rubik_cube)
                    l_key = True


                # M move (camada do meio)
                if event.key == pygame.K_6:
                    rubik_cube = m_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_key = True

                # M' move (camada do meio invertida)
                if event.key == pygame.K_x:
                    rubik_cube = m_first_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_first_key = True

                # Z move (gira todo o cubo no eixo Z)
                if event.key == pygame.K_a:
                    z_key = True
                    # Também inicia embaralhamento nesse caso
                    cycle = randrange(5, 100)
                    shuffle_key = True

                # X' move (giro no eixo X)
                if event.key == pygame.K_b:
                    x_first_key = True

                # Sexy move
                if event.key == pygame.K_s:
                    sexy_key = True

                # Resolver a cruz branca
                if event.key == pygame.K_q:
                    first_white_key = True

        # Rotação da câmera via mouse
        for event in pygame.mouse.get_pressed(3):
            if event:
                if abs(prev_pos_x - pygame.mouse.get_pos()[0]) == 0:
                    glRotatef(20, 1, 0, 0)
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) == 0:
                    glRotatef(20, 0, 1, 0)
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) > 1 and abs(
                        prev_pos_x - pygame.mouse.get_pos()[0]) > 1:
                    glRotatef(20, 1, 1, 0)
            prev_pos_x = pygame.mouse.get_pos()[0]
            prev_pos_y = pygame.mouse.get_pos()[1]

        # Limpa a tela antes de desenhar novo frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Executa o movimento selecionado (um por vez)
        if u_first_key:
            rubik_cube = u_first_move(rubik_cube)
            u_first_key = False
        elif u_key:
            rubik_cube = u_move(rubik_cube)
            u_key = False
        elif r_key:
            rubik_cube = d_move(rubik_cube)
            r_key = False
        elif m_key:
            m_key = False
        elif m_first_key:
            m_first_key = False
        elif x_first_key:
            rubik_cube = x_first_move(rubik_cube)
            x_first_key = False
        elif z_key:
            rubik_cube = z_move(rubik_cube)
            z_key = False
        elif shuffle_key:
            rubik_cube = shuffle(cycle, rubik_cube)
            shuffle_key = False
        elif sexy_key:
            rubik_cube = sexy_move(rubik_cube)
            sexy_key = False
        elif first_white_key:
            # Executa o algoritmo de resolução da cruz branca em thread separada
            threading.Thread(target=solving()).start()
            first_white_key = False

        # Desenha as três camadas do cubo
        f_layer(rubik_cube[:9])
        s_layer(rubik_cube[9:17])
        t_layer(rubik_cube[17:])

        # Atualiza a janela
        pygame.display.flip()
        pygame.time.wait(20)


if __name__ == '__main__':
    main()