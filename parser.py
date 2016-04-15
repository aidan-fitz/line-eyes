from display import *
from matrix import *
from matrix import matrix_mult as mmult
from draw import *
from draw3d import *
from math import *

from stack import Stack

def parse_file( fname, screen, pen ):
    # transformation matrix stack
    stack = Stack()
    
    # Iterating over the file so we can keep it open
    # Allows us to use stdin
    with open(fname) as fd:
        itr = iter(fd)
        
        # Do not loop through the list because we need to get multiple elements
        while True:
            args = next(itr, "quit").strip().lower().split()
            cmd = args.pop(0)
            
            # Skip comments and blank lines
            if cmd == '' or cmd[0] == '#':
                continue

            print cmd

            # 2-D drawing routines
            if cmd == "line":
                x0 = float(args[0])
                y0 = float(args[1])
                z0 = float(args[2])
                x1 = float(args[3])
                y1 = float(args[4])
                z1 = float(args[5])

                # Immediately draw line to screen
                edges = []
                add_edge(edges, x0, y0, z0, x1, y1, z1)
                mmult(stack.peek(), edges)
                draw_lines(edges, screen, pen)
                
            elif cmd == "circle" or cmd == "c":
                cx = float(args[0])
                cy = float(args[1])
                cz = 0
                r = float(args[2])
                step = 1/round(4 * sqrt(r))

                # Immediately draw curve to screen
                edges = []
                add_circle(edges, cx, cy, cz, r, step)
                mmult(stack.peek(), edges)
                draw_lines(edges, screen, pen)

            elif cmd == "hermite" or cmd == "h":
                x = [float(s) for s in args[:4]]
                y = [float(s) for s in args[4:]]

                # Immediately draw curve to screen
                edges = []
                add_curve(edges, x[0], x[1], x[2], x[3], y[0], y[1], y[2], y[3], 0.05, HERMITE)
                mmult(stack.peek(), edges)
                draw_lines(edges, screen, pen)

            elif cmd == "bezier" or cmd == "b":
                x = [float(s) for s in args[:4]]
                y = [float(s) for s in args[4:]]

                # Immediately draw curve to screen
                edges = []
                add_curve(edges, x[0], x[1], x[2], x[3], y[0], y[1], y[2], y[3], 0.05, BEZIER)
                mmult(stack.peek(), edges)
                draw_lines(edges, screen, pen)

            # 3-D drawing routines
            elif cmd == "box":
                x = float(args[0])
                y = float(args[1])
                z = float(args[2])
                width = float(args[3])
                height = float(args[4])
                depth = float(args[5])

                polygons = []
                add_box(polygons, x, y, z, width, height, depth)
                mmult(stack.peek(), polygons)
                draw_lines(polygons, screen, pen)

            elif cmd == 'sphere':
                x = float(args[0])
                y = float(args[1])
                z = 0
                r = float(args[2])
                step = int(round(2 * sqrt(r)))

                polygons = []
                add_sphere(polygons, x, y, z, r, step)
                mmult(stack.peek(), polygons)
                draw_lines(polygons, screen, pen)

            elif cmd == 'torus':
                x = float(args[0])
                y = float(args[1])
                z = 0
                r = float(args[2])
                R = float(args[3])
                step = int(round(3 * sqrt(r)))

                polygons = []
                add_torus(polygons, x, y, z, r, R, step)
                mmult(stack.peek(), polygons)
                draw_lines(polygons, screen, pen)

            # matrix control operations
            elif cmd == "translate":
                x = float(args[0])
                y = float(args[1])
                z = float(args[2])
                u = make_translate(x, y, z)
                stack.mult(u)

            elif cmd == "scale":
                x = float(args[0])
                y = float(args[1])
                z = float(args[2])
                u = make_scale(x, y, z)
                stack.mult(u)

            elif cmd == 'rotate':
                if args[0] == 'x':
                    u = make_rotX(radians(float(args[1])))
                    stack.mult(u)
                elif args[0] == 'y':
                    u = make_rotY(radians(float(args[1])))
                    stack.mult(u)
                elif args[0] == 'z':
                    u = make_rotY(radians(float(args[1])))
                    stack.mult(u)
                else:
                    raise ValueError(args[0] + " is not a valid direction")

            elif cmd == "push":
                stack.push()

            elif cmd == "pop":
                stack.pop()

            # engine control operations
            elif cmd == "display":
                display(screen)

            elif cmd == "save":
                fname = args[0]
                if fname is not None:
                    if fname[-4:].lower() == ".ppm":
                        save_ppm(screen, fname)
                    else:
                        save_extension(screen, fname)

            elif cmd == "quit":
                return
            
            # handle invalid commands
            else:
                print 'Invalid command:', cmd
