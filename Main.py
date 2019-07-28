from pygame.locals import *
import sys
import time
import numpy as np
import time
from Levels import all_levels
from random import randint
from Default_matrix import *
from Const import *
from Images import *



class Pipe(object):
    def __init__(self, x, y, index, image, type):
        self.x = x
        self.y = y
        self.index = index
        self.image = image
        self.type = type
        self.rotate_state = 0

    def draw(self):
        block_fill_size = CELL_SIZE - BORDER_SIZE
        pygame.draw.rect(screen, BLOCK_TILE_COLOR, (self.x, self.y, block_fill_size, block_fill_size), 0)
        screen.blit(self.image, (self.x, self.y))

    def rotate_self(self):
        if self.type != 1:
            # крестовину не поворачиваем
            if self.type == 5:
                return self.x, self.y
            # поворот картинки для блоков
            orig_rect = self.image.get_rect()
            rot_image = pygame.transform.rotate(self.image, ROTATE_ANGLE)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            self.image = rot_image
            # Поворачиваем и перезаписываем главную матрицу
        else:
            # для узлового блока мы не поворачиваем картинку, а рисуем другую
            self.rotate_state = (self.rotate_state + 1) % 4
            self.image = CORES[self.rotate_state]

        return self.x, self.y



class Level:
    def __init__(self):
        self.num = 2#randint(1, 10)
        self.level_matrix = all_levels[self.num][0]
        self.solve_matrix = all_levels[self.num][1]
        self.level_time = 25 #all_levels[self.num][2]




class Board:
    def __init__(self, level):
        self.pipes = []
        self.mega_matrix = []
        self.level_map = level

    # метод для получения стандартной матрицы по его типу
    def get_mini_matrix(self, type_of_pipe):
        if type_of_pipe == 0:
            return empty
        if type_of_pipe == 1:
            return core_matrix
        if type_of_pipe == 2:
            return line_matrix
        if type_of_pipe == 3:
            return angle_matrix
        if type_of_pipe == 4:
            return triple_matrix
        if type_of_pipe == 5:
            return cross_matrix

    # получаем нужное кол-во поворотов в зависимости от типа матрицы
    def get_max_rotations(self, original_matrix_type):
        if original_matrix_type == 1 or original_matrix_type == 3 or original_matrix_type == 4:
            return 4
        if original_matrix_type == 2:
            return 2
        if original_matrix_type == 5:
            return 1
        return 0


    def rotate_sub_matrix(self, col, row, rotate_num, matrix_type):
        original_matrix_type = matrix_type  # получаем тип матрицы
        max_rotations = self.get_max_rotations(original_matrix_type)  # максимальное кол-во поворотов для этой детали
        original_matrix = self.get_mini_matrix(original_matrix_type)  # копия от оригинальной матрицы
        return_matrix = original_matrix  # первое состояние всегда оригинальное
        default_rotate_count = rotation_state[col][row]  # текущее кол-во поворотов в матрице пововротов
        rotate_count = (default_rotate_count + rotate_num) % (max_rotations + 1)  # добавляем новый (текущий) поворот

        if rotate_count == 0:
            rotate_count = 1

        for i in range(rotate_count - 1):
            return_matrix = np.rot90(return_matrix)  # поворачиваем матрицу rotate_count раз

        rotation_state[col][row] = rotate_count

        return return_matrix





    # создание карты уровня
    def create_mega_matrix(self):
        reset_rotation_matrix()
        print(np.array(rotation_state))
        level_matrix = self.level_map
        horizontal_matrix = []
        col = 0

        while col < MATRIX_SIZE:
            for row in range(len(level_matrix[col])):
                block_index = level_matrix[col][row]
                tmp_matrix = self.get_mini_matrix(block_index)
                if len(horizontal_matrix) == 0:
                    horizontal_matrix = tmp_matrix
                else:
                    horizontal_matrix = np.hstack((horizontal_matrix, tmp_matrix))

            if len(self.mega_matrix) == 0:
                self.mega_matrix = horizontal_matrix
            else:
                self.mega_matrix = np.vstack((self.mega_matrix, horizontal_matrix))

            horizontal_matrix = []
            col += 1




    # перестройка карты урованя с поворотом указанной коорданатами подматрицы
    def rebuild_mega_matrix(self, pos_x_pixels, pos_y_pixels, matrix_type):
        global end_game
        # Переводим пиксельные координаты в индеклы
        pos_x = int(pos_x_pixels / CELL_SIZE)
        pos_y = int(pos_y_pixels / CELL_SIZE) - 1

        # Обнуление карты уровня
        self.mega_matrix = []
        horizontal_matrix = []

        col = 0
        #print(np.array(self.level_map))

        while col < MATRIX_SIZE:
            for row in range(len(self.level_map[col])):
                # Подмена матрицы
                if row == pos_x and col == pos_y:
                    tmp_matrix = self.rotate_sub_matrix(col, row, 1, matrix_type)  # крутим и заменяем необходимую матрицу
                else:
                    tmp_matrix = self.rotate_sub_matrix(col, row, 0, self.level_map[col][row])  # прокручиваем блоки в то положение как они были

                if len(horizontal_matrix) == 0:
                    horizontal_matrix = tmp_matrix
                else:
                    horizontal_matrix = np.hstack((horizontal_matrix, tmp_matrix))


            if len(self.mega_matrix) == 0:
                self.mega_matrix = horizontal_matrix
            else:
                self.mega_matrix = np.vstack((self.mega_matrix, horizontal_matrix))

            horizontal_matrix = []
            col += 1


    def rotate_pipe(self, screen_x, screen_y):
        rotate_pipe: Pipe = self.get_pipe_for_xy(screen_x, screen_y)
        if rotate_pipe != 0:
            x, y = rotate_pipe.rotate_self()
            pipe_type = rotate_pipe.type
            # крестовину не поворачиваем
            if pipe_type != 5:
                self.rebuild_mega_matrix(x, y, rotate_pipe.type)







    def draw_pipes(self):
        level_matrix = self.level_map
        index = 0
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                p_type = level_matrix[j][i]
                if p_type != 0:
                    new_pipe = Pipe(BORDER_SIZE + i * CELL_SIZE, Y_INDENT + BORDER_SIZE + j * CELL_SIZE, index, IMAGE_SWITCHER[p_type], p_type)
                    self.pipes.append(new_pipe)
                    new_pipe.draw()
                    index += 1


    def draw_empty_tiles(self):
        screen.fill(WHITE_COLOR)
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, Y_INDENT, WINDOW_WIDTH, WINDOW_WIDTH), 0)
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                block_fill_size = CELL_SIZE - BORDER_SIZE
                pygame.draw.rect(screen, EMPTY_TILE_COLOR, (BORDER_SIZE + i * CELL_SIZE, Y_INDENT + BORDER_SIZE + j * CELL_SIZE, block_fill_size, block_fill_size), 0)

    def light_on(self):
        for pipe in self.pipes:
            if pipe.type == 1:
                pipe.image = CORES_LIGHT[pipe.rotate_state]




    def get_pipe_for_xy(self, x, y):
        for pipe in self.pipes:
            if pipe.x < x < pipe.x + CELL_SIZE:
                if pipe.y < y < pipe.y + CELL_SIZE:
                    return pipe
        return 0


    def update_frame(self):
        for pipe in self.pipes:
            pipe.draw()

    def check_win_state(self, solve_matrix):
        print(" ")
        print(np.array(solve_matrix))
        print(" ")
        print(self.mega_matrix)
        if np.array_equal(self.mega_matrix, solve_matrix):
            return True
        return False


def draw_timer(time):
    if time >= 0:
        len_time = len(str(abs(time)))
        if len_time == 2:
            time_str = "00:" + str(time)
        else:
            time_str = "00:0" + str(time)
    else:
        time_str = "00:00"

    my_font = pygame.font.Font(FONT_PATH, TEXT_FONT_SIZE)
    text_surface = my_font.render(time_str, True, (0, 0, 0))
    screen.blit(text_surface, (WINDOW_WIDTH / 2 - TEXT_START_INDENT, CELL_SIZE / 2 - 15))

def draw_restart_btn():
    restart_btn = Images.mini_btn_restart.value
    screen.blit(restart_btn, (WINDOW_WIDTH - BORDER_SIZE - TEXT_START_INDENT, BORDER_SIZE))
    return restart_btn

def reset_rotation_matrix():
    for i in range(len(rotation_state)):
        for j in range(len(rotation_state[i])):
            rotation_state[i][j] = 1




def finish():
    font = pygame.font.Font(FONT_BOLD_PATH, RESULT_SIZE)
    text = font.render("GAME OVER", 1, DARK_TEXT_COLOR)
    textPos = (165, 320)
    btnPos = (130, 370)
    screen.blit(text, textPos)

    restart_btn = pygame.image.load('res/restart_press.png').convert()
    screen.blit(restart_btn, btnPos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        pygame.display.update()


def main():
    # init
    global screen
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(CAPTION)

    # main params
    running = True
    end_game = False
    light_on = False

    level_solve_matrix, level_time, main_board = Init()

    # MAINLOOP
    while running:
        main_board.draw_empty_tiles()
        current_time = int(time.clock())

        #DRAW  UI AND BOARDS
        if level_time - current_time >= 0:
            main_board.update_frame()  # отрисовка элементов
        else:
            # Полупрозрачная заливка фона
            screen.blit(Images.alpha_fill.value, (0, Y_INDENT, WINDOW_WIDTH, WINDOW_WIDTH))
            finish()
            # Рестарт
            level_solve_matrix, level_time, main_board = Init()
            level_time = level_time + current_time
            end_game = False
            light_on = False

        draw_timer(level_time - current_time)  # отрисовка таймера


        # EVENTS
        for event in pygame.event.get():
            # выход из игры
            if event.type == pygame.QUIT or  (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                 running = False

            # поворот трубы
            if event.type == pygame.MOUSEBUTTONDOWN and not end_game:
                x, y = event.pos
                main_board.rotate_pipe(x, y)
                win_state = main_board.check_win_state(level_solve_matrix)
                print(win_state)
                # проверка выигрыша
                if win_state:
                    end_game = True
                    continue

            # клик для вызова финиша (работает тогда когда все уже включено)
            if event.type == pygame.MOUSEBUTTONDOWN and end_game and light_on:
                screen.blit(Images.alpha_fill.value, (0, Y_INDENT, WINDOW_WIDTH, WINDOW_WIDTH))
                finish()
                # Рестарт
                level_solve_matrix, level_time, main_board = Init()
                level_time = level_time + current_time
                end_game = False
                light_on = False

            # клик для вызова подсветки
            if event.type == pygame.MOUSEBUTTONDOWN and end_game:
                main_board.light_on() # подсветить все компьютеры
                light_on = True
                continue



        pygame.display.update()



def Init():
    # create level data
    level_data: Level = Level()
    level_time = level_data.level_time
    level_matrix = level_data.level_matrix
    level_solve_matrix = level_data.solve_matrix
    # create board

    main_board: Board = Board(level_matrix)
    main_board.create_mega_matrix()
    main_board.draw_empty_tiles()  # отрисовка пустых клеток
    main_board.draw_pipes()  # отрисовка труб
    return level_solve_matrix, level_time, main_board


if __name__ == '__main__':
    main()

