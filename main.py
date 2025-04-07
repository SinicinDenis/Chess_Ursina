from ursina.shaders import *
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import board, pieces, ai
from move import Move


app = Ursina(fullscreen=True)

sky = Sky(texture='radial_gradient')

sun = DirectionalLight( position=(0, 5, 0), color=color.light_gray, shadows = True) # добавляем освещение, включаем тени
sun.look_at(Vec3(0,-1,0))

player = FirstPersonController(gravity = 0, y=2, z=-8)

grid = []   # Список для клеток
for row in range(8):       # Над каждой клеткой создаём плоскость, чтобы иметь возможность взаимодействия с каждой клеткой    
    for column in range(8):
        quad = Entity(model='quad', color=color.black10, highlight_color=color.rgba(1,1,1, 1), scale=1, rotation_x = 90, collider = 'box')
        quad.position = (column, 0, row)
        grid.append(quad)

figures = [] # Список для фигур. Все созданные фигуры помещаем в список

peshka1w = Entity(
    model='peshka.obj',
    color=color.smoke, 
    position=(0, 0, 1),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(peshka1w)

for i in range(1,8):
    peshw = duplicate(peshka1w,color=color.smoke, position = (i, 0, 1),shader = lit_with_shadows_shader,collider = 'mesh')
    figures.append(peshw)
for i in range(0,8):
    peshb = duplicate(peshka1w,color=color.black, position = (i, 0, 6),shader = lit_with_shadows_shader,collider = 'mesh')
    figures.append(peshb)

turw1 = Entity(
    model='tur.obj',  
    color=color.smoke, 
    scale=(1, 1),
    position=(0, 0, 0),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(turw1)

tur2 = duplicate(turw1, color=color.smoke,position=(7,0,0),shader = lit_with_shadows_shader, collider = 'mesh')#
tur3 = duplicate(turw1, color=color.black,position=(0,0,7),shader = lit_with_shadows_shader, collider = 'mesh')#
tur4 = duplicate(turw1, color=color.black,position=(7,0,7),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(tur2)
figures.append(tur3)
figures.append(tur4)

konw1 = Entity(
    model='kon.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(1, 0, 0),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)

figures.append(konw1)
kon2 = duplicate(konw1, color=color.smoke,position=(6,0,0),shader = lit_with_shadows_shader, collider = 'mesh')#
kon3 = duplicate(konw1, color=color.black,position=(1,0,7),rotation_y=180,shader = lit_with_shadows_shader, collider = 'mesh')#
kon4 = duplicate(konw1, color=color.black,position=(6,0,7),rotation_y=180,shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(kon2)
figures.append(kon3)
figures.append(kon4)

oficerw1 = Entity(
    model='oficer.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(2, 0, 0),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(oficerw1)
oficer2 = duplicate(oficerw1, color=color.smoke,position=(5,0,0),shader = lit_with_shadows_shader, collider = 'mesh')#
oficer3 = duplicate(oficerw1, color=color.black,position=(2,0,7),shader = lit_with_shadows_shader, collider = 'mesh')#
oficer4 = duplicate(oficerw1, color=color.black,position=(5,0,7),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(oficer2)
figures.append(oficer3)
figures.append(oficer4)

kingw = Entity(
    model='king.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(4, 0, 0),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(kingw)
king2 = duplicate(kingw, color=color.black,position=(4,0,7),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(king2)

ferzw = Entity(
    model='ferz.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(3, 0, 0),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(ferzw)
ferz2 = duplicate(ferzw, color=color.black,position=(3,0,7),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(ferz2)


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
print(board.to_string())

def update():
    global cell_pos, y, select_figure, board

    if mouse.right:   # Выбор фигуры правой кнопкой мыши
        #if not select_figure:
        for y in range(0, 32):
            if mouse.hovered_entity == figures[y]:           
                figures[y].animate_position(figures[y].position + (0,1,0), curve=curve.linear, duration=0.5)
                select_figure = figures[y]

    if mouse.left:   # Выбор клетки левой кнопкой мыши
        for j in range(0, 64):
            if mouse.hovered_entity == grid[j]:           
                cell_pos = mouse.hovered_entity.position
                select_figure.animate_position(cell_pos, curve=curve.linear, duration=0.5)
                move = get_valid_user_move(board)
                if (move == 0):
                    if (board.is_check(pieces.Piece.WHITE)):
                        print("Checkmate. Black Wins.")
                        break
                    else:
                        print("Stalemate.")
                        break

                board.perform_move(move)

                print("User move: " + move.to_string())
                print(board.to_string())

                ai_move = ai.AI.get_ai_move(board, [])
                if (ai_move == 0):
                    if (board.is_check(pieces.Piece.BLACK)):
                        print("Checkmate. White wins.")
                        break
                    else:
                        print("Stalemate.")
                        break

                board.perform_move(ai_move)
                print("AI move: " + ai_move.to_string())
                for i in figures:
                    if i.X == ai_move.xfrom and i.Z == abs(-7+ai_move.yfrom):
                        i.animate_position((ai_move.xto, 0 , abs(-7+ai_move.yto)), curve=curve.linear, duration=0.5)
                print(board.to_string())
    
        
    if held_keys['e']:      # выход на клавишу 'E'
        application.quit() 


def get_user_move():
    print("Example Move: A2 A4")
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
        print("Invalid move.")
    

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
