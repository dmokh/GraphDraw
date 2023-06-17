import pygame
pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (217, 202, 202)
RED = (255, 0, 0)
op = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'u-': 2, 'cos': 2, 'sin': 2, 'tan': 2, 'ctg': 2, 'log2': 2, 'log': 2,
      'abs': 2, '(': 4, ')': 4, '|': 4}
unary_op = ['u-', 'sin', 'cos', 'tan', 'ctg', 'log2', 'log', 'abs']
binary_op = ['+', '-', '*', '/', '^']
Arial_font = pygame.font.SysFont('arial', 20)
Arial_font_Big = pygame.font.SysFont('arial', 45)
scales = [5, 10, 20, 25, 50, 100]


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
