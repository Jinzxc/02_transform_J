from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
               takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
         ident: set the transform matrix to the identity matrix -
         scale: create a scale matrix,
                then multiply the transform matrix by the scale matrix -
                takes 3 arguments (sx, sy, sz)
         translate: create a translation matrix,
                    then multiply the transform matrix by the translation matrix -
                    takes 3 arguments (tx, ty, tz)
         rotate: create a rotation matrix,
                 then multiply the transform matrix by the rotation matrix -
                 takes 2 arguments (axis, theta) axis should be x y or z
         apply: apply the current transformation matrix to the edge matrix
         display: clear the screen, then
                  draw the lines of the edge matrix to the screen
                  display the screen
         save: clear the screen, then
               draw the lines of the edge matrix to the screen
               save the screen to a file -
               takes 1 argument (file name)
         quit: end parsing

See the file script for an example of the file format
"""
def parse_file( fname, points, transform, screen, color ):
      func_arg_dict = {
            'line'     : lambda arg: add_edge(points, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5]),
            'scale'    : lambda arg: matrix_mult(make_scale(arg[0], arg[1], arg[2]), transform),
            'move'     : lambda arg: matrix_mult(make_translate(arg[0], arg[1], arg[2]), transform),
            'rotate'   : lambda arg: rotate_dict.get('rotate' + arg[0])(arg[1]),
            'save'     : lambda arg: [func_not_arg_dict.get('display')(), save_extension(screen, arg[0])]
      }

      func_not_arg_dict = {
            'ident'    : lambda : ident(transform),
            'apply'    : lambda : matrix_mult(transform, points),
            'display'  : lambda : [clear_screen(screen), draw_lines(points, screen, color), display(screen)]
      }

      rotate_dict = {
            'rotatex'   : lambda theta: matrix_mult(make_rotX(theta), transform),
            'rotatey'   : lambda theta: matrix_mult(make_rotY(theta), transform),
            'rotatez'   : lambda theta: matrix_mult(make_rotZ(theta), transform)
      }

      f = open(fname, "r")
      lines = []

      for line in f:
            lines.append(line.rstrip())

      i = 0
      while i < len(lines):
            if lines[i] == 'quit':
                  print('exiting')
                  break
            
            if lines[i] in func_arg_dict:
                  args = [x for x in lines[i + 1].split(" ")]

                  if lines[i] != 'save' and lines[i] != 'rotate':
                        args = [int(x) for x in args]

                  if lines[i] == 'rotate':
                        args[1] = float(args[1])

                  func_arg_dict.get(lines[i])(args)
                  i = i + 1
            elif lines[i] in func_not_arg_dict:
                  func_not_arg_dict.get(lines[i], None)()
                  if lines[i] == 'apply':
                        points = [[int(y) for y in x] for x in points]
            i += 1