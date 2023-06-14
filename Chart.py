import time

from Draw import *
from utilites import *
from Count_equation import *


class Chart:
    def __init__(self, formula, scale, width, height, top_border=100):
        self.formula, self.scale, self.size, self.width, self.height, self.top_border = \
            formula, scale, (width, height), width, height, top_border

    def draw_base(self, screen):
        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, (self.width // self.scale // 2 * self.scale,
                                         self.height // self.scale // 2 * self.scale + self.top_border), 10)

        for i in range(self.top_border, self.height + self.top_border, self.scale):
            if i == self.height // self.scale // 2 * self.scale + self.top_border:
                pygame.draw.line(screen, RED, (0, i), (self.width, i), 5)
            else:
                pygame.draw.line(screen, LIGHT_GRAY, (0, i), (self.width, i))
        for j in range(0, self.width, self.scale):
            if j == self.width // self.scale // 2 * self.scale:
                pygame.draw.line(screen, RED, (j, self.top_border), (j, self.height + self.top_border), 5)
            else:
                pygame.draw.line(screen, LIGHT_GRAY, (j, self.top_border), (j, self.height + self.top_border))

    def draw_formula(self, screen):
        equation_x = self.formula.split('=')[1] if 'y' in self.formula.split("=")[0] else self.formula.split("=")[0]
        time_01 = time.time()
        x = -(self.width // self.scale // 2 + 1)
        while x <= self.width // self.scale // 2 + 1:
            equation_copy = list(equation_x)
            j = 0
            while j < len(equation_copy):
                if equation_copy[j] == 'x':
                    equation_copy[j] = f'{x}'
                j += 1
            y = count_equation(equation_copy)
            equation_y = self.formula.split('=')[0] if 'y' in self.formula.split("=")[0] else self.formula.split("=")[1]
            monomials = get_monomials(equation_y)
            equation_right = '{:.20f}'.format(y)
            monomial_with_y = []
            for monomial in monomials:
                if 'y' not in monomial[0]:
                    equation_right += monomial[1] + monomial[0]
                else:
                    monomial_with_y.append(monomial)
            for monomial in monomial_with_y:
                now = ''
                last_operation = False
                for i in monomial[0]:
                    if i != 'y':
                        if i.isdigit() or i == '.':
                            now += i
                        else:
                            if last_operation:
                                equation_right = '(' + equation_right + ')' + ('*' if last_operation == '/' else '/') + now
                                now = ''
                            last_operation = i
                if now != '':
                    equation_right = '(' + equation_right + ')' + ('*' if last_operation == '/' else '/') + now
            y = count_equation(list(equation_right))
            pygame.draw.circle(screen, BLACK, (self.width // self.scale // 2 * self.scale + x * self.scale,
                                               self.height // self.scale // 2 * self.scale + self.top_border -
                                               y * self.scale), 2)
            x += 0.005
        time_02 = time.time()

    def get_pos(self, x, y, whole=True):
        if whole:
            return round((x - self.width // self.scale // 2 * self.scale) / self.scale), \
                -round((y - self.height // self.scale // 2 * self.scale - self.top_border) / self.scale)
        else:
            return ((x - self.width // self.scale // 2 * self.scale) / self.scale), \
                -((y - self.height // self.scale // 2 * self.scale - self.top_border) / self.scale)
