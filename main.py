from ursina.shaders import *
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import board, pieces, ai
from move import Move
from threading import Thread


app = Ursina(fullscreen=True)

sky = Sky(texture='brick')

sun = DirectionalLight( position=(0, 5, 0), color=color.light_gray, shadows = True, shadow_map_resolution = Vec2(5000, 5000)) # добавляем освещение, включаем тени
sun.look_at(Vec3(0,-1,0))

player = FirstPersonController(gravity = 0, y=2, z=-8)

grid = []   # Список для клеток
for row in range(8):       # Над каждой клеткой создаём плоскость, чтобы иметь возможность взаимодействия с каждой клеткой    
    for column in range(8):
        quad = Entity(model='quad', color=color.black10, highlight_color=color.rgba(1,1,1, 1), scale=1, rotation_x = 90, collider = 'box')
        quad.position = (column, 0, row)
        grid.append(quad)

figures = [] # Список для фигур. Все созданные фигуры помещаем в список

def load_models_():
    global pes, tur, kon, ofc, kin, fer
    if not 'models_compressed\ferz.bam':

        pes = Entity(
            model='peshka.obj',
            color=color.clear, 
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        tur = Entity(
            model='tur.obj',  
            color=color.clear, 
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        kon = Entity(
            model='kon.obj',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        ofc = Entity(
            model='oficer.obj',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        kin = Entity(
            model='king.obj',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        fer = Entity(
            model='ferz.obj',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )
    else:
        pes = Entity(
        model='peshka',
        color=color.clear, 
        position=(0, 10, 0),
        shader = lit_with_shadows_shader,
        collider = 'mesh'
        )

        tur = Entity(
            model='tur',  
            color=color.clear, 
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        kon = Entity(
            model='kon',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        ofc = Entity(
            model='oficer',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        kin = Entity(
            model='king',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

        fer = Entity(
            model='ferz',
            color=color.clear,
            scale=(1, 1),
            position=(0, 10, 0),
            shader = lit_with_shadows_shader,
            collider = 'mesh'
        )

Thread(target=load_models_).start()

ground = Entity(
    model='plane',  # Используем плоскость как модель
    texture='doska_shahmat.png',  # Применяем текстуру
    scale=(8, 1, 8),  # Устанавливаем размер
    position=(3.5, -0.01, 3.5),
    rotation_y = 90,
    shader = lit_with_shadows_shader
)

coord = Entity(
    model='plane',  # Используем плоскость как модель
    texture='doska.jpg',  # Применяем текстуру координат доски
    scale=(9.3, 2, 9.3),  # Устанавливаем размер
    position=(3.5, -0.02, 3.5),
    shader = lit_with_shadows_shader
)

cell_pos = 0 # Переменная для хранения позиции выбранной клетки

select_figure = 0 # Переменная для хранения выбраной фигуры

board = board.Board.new()


def figures_rasstanovka():
    global figures
    for y in range(board.HEIGHT):

            for x in range(board.WIDTH):
                piece = board.chesspieces[x][y]
                if (piece != 0):
                    if piece.to_string()[0] == 'W':
                        if piece.to_string()[1] == 'P':
                            figures += [duplicate(pes, color=color.white, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'R':
                            figures += [duplicate(tur, color=color.white, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'N':
                            figures += [duplicate(kon, color=color.white, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'B':
                            figures += [duplicate(ofc, color=color.white, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'Q':
                            figures += [duplicate(fer, color=color.white, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'K':
                            figures += [duplicate(kin, color=color.white, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                    else:
                        if piece.to_string()[1] == 'P':
                            figures += [duplicate(pes, color=color.dark_gray, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'R':
                            figures += [duplicate(tur, color=color.dark_gray, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'N':
                            figures += [duplicate(kon, color=color.dark_gray, position=(x,0,abs(-7+y)),rotation_y=180, shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'B':
                            figures += [duplicate(ofc, color=color.dark_gray, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'Q':
                            figures += [duplicate(fer, color=color.dark_gray, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]
                        elif piece.to_string()[1] == 'K':
                            figures += [duplicate(kin, color=color.dark_gray, position=(x,0,abs(-7+y)), shader=lit_with_shadows_shader, collider='mesh')]

scene.fog_density = .1          # sets exponential density
scene.fog_density = (0, 20)   # sets linear density start and end

print(board.to_string())
Thread(target=figures_rasstanovka).start()
#figures_rasstanovka()

a_w = False
a_b = False

ai_anim = False

def black_hod():
    pass

def update():
    global cell_pos, y, select_figure, board, a_w, a_b

    if a_w:
        if a_w[0].position == a_w[1]:
            for i in figures:
                if i.position == a_w[0].position and a_w[0] != i:
                    figures.remove(i)
                    destroy(i)
                    break
            a_w = False

    if a_b:
        if a_b[0].position == a_b[1]:
            for i in figures:
                if i.position == a_b[0].position and a_b[0] != i:
                    figures.remove(i)
                    destroy(i)
                    break
            a_b = False

    if mouse.right:   # Выбор фигуры правой кнопкой мыши
        #if not select_figure:
        for y in figures:
            if mouse.hovered_entity == y and y.color == color.white:           
                y.animate_position(y.position + (0,1,0), curve=curve.linear, duration=0.5)
                select_figure = y
                

    if mouse.left:   # Выбор клетки левой кнопкой мыши
        for j in range(0, 64):
            print(select_figure)
            if mouse.hovered_entity == grid[j] and (select_figure.position - (0,1,0) == grid[j].position):
                select_figure.animate_position(select_figure.position + (0,-1,0), curve=curve.linear, duration=0.5)
                #select_figure = None
                break

            if mouse.hovered_entity == grid[j]:           
                cell_pos = mouse.hovered_entity.position
                move = get_valid_user_move(board)
                if (move == 0):
                    if (board.is_check(pieces.Piece.WHITE)):
                        print("Checkmate. Black Wins.")
                        break
                    else:
                        print("Stalemate.")
                        break
                if (move == -1):
                    break
                board.perform_move(move)
                
                select_figure.animate_position(cell_pos, curve=curve.linear, duration=0.5)
                a_w = (select_figure, cell_pos)
                print("User move: " + move.to_string())
                print(board.to_string())
                Thread(target=ai_mov).start()
                
    
    if held_keys['e']:      # выход на клавишу 'E'
        application.quit()


def input(key):
    if key == 'scroll up':
        if player.Y < 5:
            player.animate_position(player.position + (0,1,0), curve=curve.linear, duration=0.3)
    if key == 'scroll down':
        if player.Y > 0:
            player.animate_position(player.position + (0,-1,0), curve=curve.linear, duration=0.3)


def ai_mov():
    global a_b
    ai_move = ai.AI.get_ai_move(board, [])
    if (ai_move == 0):
        if (board.is_check(pieces.Piece.BLACK)):
            print("Checkmate. White wins.")
            quit()
        else:
            print("Stalemate.")
            quit

    board.perform_move(ai_move)
    print("AI move: " + ai_move.to_string())
    for i in figures:
        if i.X == ai_move.xfrom and i.Z == abs(-7+ai_move.yfrom):
            i.animate_position((ai_move.xto, 0 , abs(-7+ai_move.yto)), curve=curve.linear, duration=0.5)
            a_b = (i, (ai_move.xto, 0 , abs(-7+ai_move.yto)))
    print(board.to_string())


def get_user_move():
    print("Example Move: A2 A4")
    print(cell_pos)
    move_str = "ABCDEFGH"[select_figure.X]+"12345678"[select_figure.Z]+" "+"ABCDEFGH"[int(cell_pos[0])]+"12345678"[int(cell_pos[2])]
    move_str = move_str.replace(" ", "")

    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2]) # The board is drawn "upside down", so flip the y coordinate.
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4]) # The board is drawn "upside down", so flip the y coordinate.
        return Move(xfrom, yfrom, xto, yto)
    except ValueError:
        print("Invalid format. Example: A2 A4")
        #return get_user_move()

# Returns a valid move based on the users input.
def get_valid_user_move(board):

    move = get_user_move()
    valid = False
    possible_moves = board.get_possible_moves(pieces.Piece.WHITE)
    # No possible moves
    if (not possible_moves):
        return 0

    for possible_move in possible_moves:
        if (move.equals(possible_move)):
            valid = True
            break

    if (valid):
        return move
    else:
        return -1
    

# Converts a letter (A-H) to the x position on the chess board.
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7

    raise ValueError("Invalid letter.")



app.run()
