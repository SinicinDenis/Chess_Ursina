from ursina.shaders import *
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(fullscreen=True)

sky = Sky(texture='radial_gradient')

sun = DirectionalLight( position=(0, 5, 0), color=color.light_gray, shadows = True) # добавляем освещение, включаем тени
sun.look_at(Vec3(0,-1,0))

player = FirstPersonController(gravity = 0, y=2, z=-8)

grid = []   # Список для клеток
for row in range(8):       # Над каждой клеткой создаём плоскость, чтобы иметь возможность взаимодействия с каждой клеткой    
    for column in range(8):
        quad = Entity(model='quad', color=color.black10, scale=1, rotation_x = 90, collider = 'box')
        quad.position = (column-3, 0, row-3)
        grid.append(quad)

figures = [] # Список для фигур. Все созданные фигуры помещаем в список

peshka1w = Entity(
    model='peshka.obj',
    color=color.smoke, 
    position=(-3, 0, -2),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(peshka1w)

for i in range(-2,5):
    peshw = duplicate(peshka1w,color=color.smoke, position = (i, 0, -2),shader = lit_with_shadows_shader,collider = 'mesh')
    figures.append(peshw)
for i in range(-3,5):
    peshb = duplicate(peshka1w,color=color.black, position = (i, 0, 3),shader = lit_with_shadows_shader,collider = 'mesh')
    figures.append(peshb)

turw1 = Entity(
    model='tur.obj',  
    color=color.smoke, 
    scale=(1, 1),
    position=(-3, 0, -3),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(turw1)

tur2 = duplicate(turw1, color=color.smoke,position=(4,0,-3),shader = lit_with_shadows_shader, collider = 'mesh')#
tur3 = duplicate(turw1, color=color.black,position=(-3,0,4),shader = lit_with_shadows_shader, collider = 'mesh')#
tur4 = duplicate(turw1, color=color.black,position=(4,0,4),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(tur2)
figures.append(tur3)
figures.append(tur4)

konw1 = Entity(
    model='kon.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(-2, 0, -3),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)

figures.append(konw1)
kon2 = duplicate(konw1, color=color.smoke,position=(3,0,-3),shader = lit_with_shadows_shader, collider = 'mesh')#
kon3 = duplicate(konw1, color=color.black,position=(-2,0,4),rotation_y=180,shader = lit_with_shadows_shader, collider = 'mesh')#
kon4 = duplicate(konw1, color=color.black,position=(3,0,4),rotation_y=180,shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(kon2)
figures.append(kon3)
figures.append(kon4)

oficerw1 = Entity(
    model='oficer.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(-1, 0, -3),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(oficerw1)
oficer2 = duplicate(oficerw1, color=color.smoke,position=(2,0,-3),shader = lit_with_shadows_shader, collider = 'mesh')#
oficer3 = duplicate(oficerw1, color=color.black,position=(-1,0,4),shader = lit_with_shadows_shader, collider = 'mesh')#
oficer4 = duplicate(oficerw1, color=color.black,position=(2,0,4),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(oficer2)
figures.append(oficer3)
figures.append(oficer4)

kingw = Entity(
    model='king.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(0, 0, -3),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(kingw)
king2 = duplicate(kingw, color=color.black,position=(0,0,4),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(king2)

ferzw = Entity(
    model='ferz.obj',
    color=color.smoke,
    scale=(1, 1),
    position=(1, 0, -3),
    shader = lit_with_shadows_shader,
    collider = 'mesh'
)
figures.append(ferzw)
ferz2 = duplicate(ferzw, color=color.black,position=(1,0,4),shader = lit_with_shadows_shader, collider = 'mesh')#
figures.append(ferz2)


ground = Entity(
    model='plane',  # Используем плоскость как модель
    texture='doska_shahmat.png',  # Применяем текстуру
    scale=(8, 1, 8),  # Устанавливаем размер
    position=(0.5, -0.01, 0.5),
    rotation_y = 90,
    shader = lit_with_shadows_shader
)

coord = Entity(
    model='plane',  # Используем плоскость как модель
    texture='doska.jpg',  # Применяем текстуру координат доски
    scale=(9.3, 2, 9.3),  # Устанавливаем размер
    position=(0.5, -0.03, 0.5),
    shader = lit_with_shadows_shader
)

cell_pos = 0 # Переменная для хранения позиции выбранной клетки

select_figure = 0 # Переменная для хранения выбраной фигуры
         
def update():
    global cell_pos, y, select_figure

    if mouse.right:   # Выбор фигуры правой кнопкой мыши
        for y in range(0, 32):
            if mouse.hovered_entity == figures[y]:           
                figures[y].animate_position(figures[y].position + (0,1,0), curve=curve.linear, duration=0.5)
                select_figure = figures[y]

    if mouse.left:   # Выбор клетки левой кнопкой мыши
        for j in range(0, 64):
            if mouse.hovered_entity == grid[j]:           
                cell_pos = mouse.hovered_entity.position
                select_figure.animate_position(cell_pos, curve=curve.linear, duration=0.5)
        
    if held_keys['e']:      # выход на клавишу 'E'
        application.quit() 

app.run()
