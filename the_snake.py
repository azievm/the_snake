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
pg.display.set_caption('Змейка | Выход: ESC')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """
    Базовый класс, от которого наследуются другие игровые объекты

    position — позиция объекта на игровом поле
    body_color — цвет объекта

    __init__ — инициализирует базовые атрибуты объекта
    draw — предназначен для переопределения в дочерних классах
    """

    def __init__(self, body_color=None):
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self, surface, position, body_color, line_thickness=0):
        """Отрисовывает объекты на игровой поверхности."""
        rect = pg.Rect(
            (position[0], position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, body_color, rect, line_thickness)


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject
    Описывающий яблоко и действия с ним

    __init__ — задаёт цвет яблока и вызывает метод randomize_position
    randomize_position — устанавливает случайное положение на игровом поле
    draw — отрисовывает яблоко на игровой поверхности

    body_color — цвет яблока
    position — позиция яблока на игровом поле
    """

    def __init__(self, positions=(0, 0), body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Устанавливает случайное положение яблока на игровом поле"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

        if self.position in positions:
            self.randomize_position(positions)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности"""
        super().draw(surface, self.position, self.body_color)
        super().draw(surface, self.position, BORDER_COLOR, 1)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject
    Описывающий яблоко и действия с ним

    __init__ — инициализирует начальное состояние змейки
    update_direction — обновляет направление движения змейки
    move — обновляет позицию змейки
    draw — отрисовывает змейку на экране
    get_head_position — возвращает позицию головы змейки
    reset — сбрасывает змейку в начальное состояние после столкновения с собой

    """

    def __init__(self, body_color=SNAKE_COLOR):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        super().__init__(body_color)

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        Добавляя новую голову в начало списка positions
        И удаляя последний элемент, если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

        self.position = (new_x, new_y)
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )

            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
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


def main():
    """Основной цикл игры"""
    # Инициализация PyGame:
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.draw(screen)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            apple.draw(screen)

        snake.draw(screen)
        apple.draw(screen)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        pg.display.update()

        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
