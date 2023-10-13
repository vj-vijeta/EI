class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def is_valid_move(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

class Obstacle:
    def __init__(self, x, y):
        self.position = Position(x, y)

class MarsRover:
    def __init__(self, x, y, direction, grid, obstacles):
        self.position = Position(x, y)
        self.direction = direction
        self.grid = grid
        self.obstacles = obstacles
        self.command_history = []

    def move(self):
        new_x, new_y = self.position.x, self.position.y

        if self.direction == 'N':
            new_y += 1
        elif self.direction == 'S':
            new_y -= 1
        elif self.direction == 'E':
            new_x += 1
        elif self.direction == 'W':
            new_x -= 1

        new_position = Position(new_x, new_y)

        if self.grid.is_valid_move(new_x, new_y) and not self.has_obstacle(new_position):
            self.position = new_position
            self.command_history.append("M")

    def turn_left(self):
        if self.direction == 'N':
            self.direction = 'W'
        elif self.direction == 'S':
            self.direction = 'E'
        elif self.direction == 'E':
            self.direction = 'N'
        elif self.direction == 'W':
            self.direction = 'S'
        self.command_history.append("L")

    def turn_right(self):
        if self.direction == 'N':
            self.direction = 'E'
        elif self.direction == 'S':
            self.direction = 'W'
        elif self.direction == 'E':
            self.direction = 'S'
        elif self.direction == 'W':
            self.direction = 'N'
        self.command_history.append("R")

    def execute_commands(self, commands):
        for command in commands:
            command.execute(self)

    def has_obstacle(self, position):
        return any(obstacle.position.x == position.x and obstacle.position.y == position.y for obstacle in self.obstacles)

class Command:
    def execute(self, rover):
        pass

class MoveCommand(Command):
    def execute(self, rover):
        rover.move()

class TurnLeftCommand(Command):
    def execute(self, rover):
        rover.turn_left()

class TurnRightCommand(Command):
    def execute(self, rover):
        rover.turn_right()

# Inputs
grid = Grid(10, 10)
obstacles = [Obstacle(2, 2), Obstacle(3, 5)]

# Initialize the rover
rover = MarsRover(0, 0, 'N', grid, obstacles)

# Execute commands
commands = [MoveCommand(), MoveCommand(), TurnRightCommand(), MoveCommand(), TurnLeftCommand(), MoveCommand()]
for command in commands:
    rover.execute_commands([command])

# Print the final position and command history
print(f"Final Position: ({rover.position.x}, {rover.position.y}), Direction: {rover.direction}, Command History: {rover.command_history}")
