import time

from utilites import *
from Count_equation import count_equation, get_monomials


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
        equation_y = self.formula.split('=')[0] if 'y' in self.formula.split("=")[0] else self.formula.split("=")[1]
        time_01 = time.time()
        x = -(self.width // self.scale // 2 + 1)
        while x <= self.width // self.scale // 2 + 1:
            equation_copy = list(equation_x)
            equation_y_copy = list(equation_y)
            j = 0
            while j < len(equation_copy):
                if equation_copy[j] == 'x':
                    equation_copy[j] = f'{x}'
                j += 1
            j = 0
            while j < len(equation_y_copy):
                if equation_y_copy[j] == 'x':
                    equation_y_copy[j] = f'{x}'
                j += 1
            y = count_equation(equation_copy)
            monomials = get_monomials(equation_y_copy)
            equation_right = '{:.20f}'.format(y)
            monomial_with_y = []
            for monomial in monomials:
                if 'y' not in monomial[0]:
                    equation_right += ('+' if monomial[1] == '-' else '-') + monomial[0]
                else:
                    monomial_with_y.append(monomial)
            j = 0
            while any(list(map(lambda av: '/' in av[0], monomial_with_y))):
                monomial = monomial_with_y[j]
                now = ''
                last_operation = False
                last_operation_index = 0
                h = 0
                for i in monomial[0]:
                    if i != 'y':
                        if i.isdigit() or i == '.':
                            now += i
                        elif i == '/':
                            if last_operation:
                                k = 0
                                for mon in monomial_with_y:
                                    if k != j:
                                        mon[0] += '*' + now
                                    k += 1
                                monomial[0] = monomial[0][:last_operation_index] + monomial[0][h+1:]
                                equation_right = '(' + equation_right + ')' + '*' \
                                                 + now
                                now = ''
                            last_operation = i
                            last_operation_index = h
                    h += 1
                if now != '':
                    k = 0
                    for mon in monomial_with_y:
                        if k != j:
                            mon[0] += '*' + now
                        k += 1
                    monomial[0] = monomial[0][:last_operation_index] + monomial[0][h + 1:]
                    equation_right = '(' + equation_right + ')' + '*' + now
                j += 1
                if j >= len(monomial_with_y):
                    j = 0
            c_y = 0
            for mon in monomial_with_y:
                now = ''
                b = 1
                last_op = ''
                for i in mon[0]:
                    if i == '*':
                        if last_op != '':
                            now = count_equation(now)
                            b *= float(now)
                            now = ''
                        last_op = i
                    elif i != 'y':
                        now += i
                if now != '':
                    now = count_equation(now)
                    b *= float(now)
                    now = ''
                c_y = c_y + (float(b) if mon[1] == '+' else -float(b))
            equation_right = '(' + equation_right + ')' + '/' + str(c_y)
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
