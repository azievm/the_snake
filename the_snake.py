from random import choice, randint
import sys

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, body_color=None):
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, который предназначен
        для переопределения в дочерних классах
        """
        pass

    def draw_cell(self, position, color):
        """Отрисовывает ячейки на игровой поверхности"""
        rect = pg.Rect(
            (position),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, color, rect)

        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним
    """

    def __init__(self, snake=None, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(snake)

    def randomize_position(self, snake=None):
        """Устанавливает случайное положение яблока на игровом поле"""
        while snake and self.position in snake.positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.next_direction = None
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка
        positions и удаляя последний элемент,
        если длина змейки не увеличилась
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH)
        new_y = ((head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, (new_x, new_y))

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние
        после столкновения с собой
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])

    def draw(self):
        """Отрисовывает змейку и затирает последний сегмент"""
        self.draw_cell(self.get_head_position(), self.body_color)
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                sys.exit()


def main():
    """Основной игровой цикл, где происходит обновление состояния объектов"""
    pg.init()

    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple(snake)
    apple.draw()

    while True:
        clock.tick(SPEED)

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake)
            apple.draw()

        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.draw()

        snake.draw()

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        pg.display.update()


if __name__ == '__main__':
    main()
