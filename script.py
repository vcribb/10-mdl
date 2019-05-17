import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print ("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    polygons = []
    edges = []
    obj = command['op']
    args = command['args']

    for command in commands:
        print (command)

        if obj == 'push':
            stack.append([item[:] for item in stack[-1]])
            
        elif obj == 'pop':
            stack.pop()
            
        elif obj == 'move':
            temp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], temp)
            stack[-1] = [item[:] for item in temp]
            
        elif obj == 'scale':
            temp = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], temp)
            stack[-1] = [item[:] for item in temp]
            
        elif obj == 'rotate':
            temp = new_matrix()
            if args[0] == 'x':
                temp = make_rotX(args[1] * (math.pi/180))
            elif args[0] == 'y':
                temp = make_rotY(args[1] * (math.pi/180))
            else:
                temp = make_rotZ(args[1] * (math.pi/180))
            matrix_mult(stack[-1], temp)
            stack[-1] = [item[:] for item in temp]

        elif obj == 'line':
            add_edge(edges, float(args[0]), float(args[1]), float(args[2]),
                     float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif obj == 'box':
            add_box(polygons, float(args[0]), float(args[1]), float(args[2]),
                     float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], polygons)
            if command['constants']:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif obj == 'sphere':
            add_sphere(polygons, float(args[0]), float(args[1]), float(args[2]),
                     float(args[3]), step_3d)
            matrix_mult(stack[-1], polygons)
            if command['constants']:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif obj == 'torus':
            add_torus(polygons, float(args[0]), float(args[1]), float(args[2]),
                     float(args[3]), float(args[4]), step_3d)
            matrix_mult(stack[-1], polygons)
            if command['constants']:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif obj == 'constants':
            pass

        elif obj == 'save':
            save_extension(screen, args[0] + '.png')

        elif obj == 'display':
            display(screen)

        else:
            pass
