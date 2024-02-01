from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

class GameObject:
    """
    Базовый класс, от которого наследуются другие игровые объекты

    position — позиция объекта на игровом поле
    body_color — цвет объекта

    __init__ — инициализирует базовые атрибуты объекта
    draw — предназначен для переопределения в дочерних классах
    """

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self, surface):
        pass

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

    def __init__(self, body_color = APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

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

    def __init__(self,
                 length=1,
                 positions=[((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))],
                 direction=RIGHT,
                 next_direction=None,
                 last=None,
                 body_color=SNAKE_COLOR,):

        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.last = last
        super().__init__(body_color)

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):

        head_position = self.get_head_position()

        direction_position = self.direction
        
        new_x = (head_position[0] + direction_position[0]
                 * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_position[1] + direction_position[1]
                 * GRID_SIZE) % SCREEN_HEIGHT

        if (new_x, new_y) == self.positions[1:]:
            self.reset()

        else:
            self.positions.insert(0, (new_x, new_y))

            if self.length < len(self.positions):
                self.last = self.positions.pop()

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        direction_list = [UP, DOWN, LEFT, RIGHT]
        self.direction = choice(direction_list)

    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш, чтобы изменить направление движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основной цикл игры
    """

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        if apple.position == snake.positions[0]:
            snake.length += 1

            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        pygame.display.update()

        screen.fill(BOARD_BACKGROUND_COLOR)

if __name__ == '__main__':
    main()

