import time
import pygame
import Chart
from Count_equation import *
from utilites import *
pygame.init()
pygame.font.init()

size = (1000, 750)
top_border = 50
screen = pygame.display.set_mode(size)
if __name__ == "__main__":
    graph_one = Chart.Chart("x=y", scales[5], size[0], size[1]-top_border, top_border)
    position = False
    integer = False
    formula = "x=y"
    now_pos_of_text = 3
    while True:
        graph_one.draw_base(screen)
        graph_one.draw_formula(screen)
        pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, size[0], top_border))
        screen.blit(Arial_font_Big.render(formula[0:now_pos_of_text] + '|' + formula[now_pos_of_text:], False, BLACK),
                    (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        if integer:
            graph_pos = graph_one.get_pos(mouse_pos[0], mouse_pos[1], True)
        else:
            graph_pos = graph_one.get_pos(mouse_pos[0], mouse_pos[1], False)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(1)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    integer = not integer
                if e.button == 3:
                    position = not position
                if e.button == 4:
                    if scales.index(graph_one.scale) + 1 < len(scales):
                        graph_one.scale = scales[scales.index(graph_one.scale) + 1]
                if e.button == 5:
                    if scales.index(graph_one.scale) - 1 > 0:
                        graph_one.scale = scales[scales.index(graph_one.scale) - 1]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    graph_one.formula = formula
                elif e.key == pygame.K_BACKSPACE:
                    if len(formula) > 0:
                        formula = formula[:now_pos_of_text-1] + formula[now_pos_of_text:]
                        now_pos_of_text -= 1
                elif e.key == pygame.K_LEFT:
                    now_pos_of_text = max(0, now_pos_of_text - 1)
                elif e.key == pygame.K_RIGHT:
                    now_pos_of_text = min(now_pos_of_text + 1, len(formula))
                elif e.mod and pygame.KMOD_SHIFT:
                    if e.unicode != '':
                        formula = formula[0:now_pos_of_text-1] + e.unicode + formula[now_pos_of_text-1:]
                    now_pos_of_text += 1
                else:
                    formula = formula[0:now_pos_of_text] + e.unicode + formula[now_pos_of_text:]
                    now_pos_of_text += 1
        if position:
            if integer:
                pygame.draw.rect(screen, LIGHT_GRAY, mouse_pos + (55, 20))
            else:
                pygame.draw.rect(screen, LIGHT_GRAY, mouse_pos + (80, 20))
            screen.blit(Arial_font.render(f'{graph_pos[0]}, {graph_pos[1]}', False, BLACK), mouse_pos)
        pygame.display.flip()
