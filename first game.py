import random

# Define the grid size, number of obstacles, and number of health pickups
GRID_SIZE = 10
NUM_OBSTACLES = 5
NUM_HEALTH_PICKUPS = 3
OBSTACLE_MOVEMENT_STEPS = 1  # How many steps an obstacle moves in each turn
INITIAL_HEALTH = 10  # Initial health points for the player
HEALTH_PICKUP_AMOUNT = 5  # Amount of health restored by a pickup

class Player:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
    
    def move(self, direction, obstacles):
        if direction == "w" and self.y > 0:
            new_y = self.y - 1
            if (self.x, new_y) not in obstacles:
                self.y = new_y
        elif direction == "s" and self.y < GRID_SIZE - 1:
            new_y = self.y + 1
            if (self.x, new_y) not in obstacles:
                self.y = new_y
        elif direction == "a" and self.x > 0:
            new_x = self.x - 1
            if (new_x, self.y) not in obstacles:
                self.x = new_x
        elif direction == "d" and self.x < GRID_SIZE - 1:
            new_x = self.x + 1
            if (new_x, self.y) not in obstacles:
                self.x = new_x
        else:
            print("You can't move in that direction!")

    def take_damage(self, amount):
        self.health -= amount
        print(f"Health: {self.health}")

    def gain_health(self):
        self.health += HEALTH_PICKUP_AMOUNT
        print(f"Health increased! Current health: {self.health}")

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MovingObstacle:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
    
    def move(self, grid_size, obstacles):
        # Define possible movement directions
        directions = ["w", "s", "a", "d"]
        direction = random.choice(directions)
        
        # Try to move in the chosen direction
        if direction == "w" and self.y > 0:
            new_y = self.y - 1
        elif direction == "s" and self.y < grid_size - 1:
            new_y = self.y + 1
        else:
            new_y = self.y

        if direction == "a" and self.x > 0:
            new_x = self.x - 1
        elif direction == "d" and self.x < grid_size - 1:
            new_x = self.x + 1
        else:
            new_x = self.x
        
        # Update position only if new position is not occupied
        if (new_x, new_y) not in obstacles:
            self.x = new_x
            self.y = new_y

class Game:
    def __init__(self):
        self.player = Player(0, 0, INITIAL_HEALTH)  # Player starts with initial health
        self.target = Target(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        while (self.target.x == self.player.x and self.target.y == self.player.y):
            # Ensure the target is not placed on the same spot as the player
            self.target = Target(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        
        self.obstacles = set()
        self.moving_obstacles = []
        self.health_pickups = set()

        # Generate static obstacles
        while len(self.obstacles) < NUM_OBSTACLES:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) != (self.player.x, self.player.y) and (x, y) != (self.target.x, self.target.y):
                self.obstacles.add((x, y))
        
        # Generate moving obstacles
        for _ in range(NUM_OBSTACLES):
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) != (self.player.x, self.player.y) and (x, y) != (self.target.x, self.target.y):
                damage = random.randint(1, 3)  # Random damage amount for obstacles
                self.moving_obstacles.append(MovingObstacle(x, y, damage))
        
        # Generate health pickups
        while len(self.health_pickups) < NUM_HEALTH_PICKUPS:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) != (self.player.x, self.player.y) and (x, y) != (self.target.x, self.target.y) and (x, y) not in self.obstacles and (x, y) not in [(o.x, o.y) for o in self.moving_obstacles]:
                self.health_pickups.add((x, y))

    def display_grid(self):
        grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        grid[self.player.y][self.player.x] = '@'
        grid[self.target.y][self.target.x] = '$'
        for obs in self.obstacles:
            grid[obs[1]][obs[0]] = '#'
        for obs in self.moving_obstacles:
            grid[obs.y][obs.x] = '#'
        for hp in self.health_pickups:
            grid[hp[1]][hp[0]] = 'H'
        
        for row in grid:
            print(" ".join(row))
    
    def update_obstacles(self):
        for obs in self.moving_obstacles:
            for _ in range(OBSTACLE_MOVEMENT_STEPS):
                obs.move(GRID_SIZE, self.obstacles.union((o.x, o.y) for o in self.moving_obstacles))
    
    def check_collision(self):
        if (self.player.x, self.player.y) in [(o.x, o.y) for o in self.moving_obstacles]:
            for obs in self.moving_obstacles:
                if (self.player.x, self.player.y) == (obs.x, obs.y):
                    self.player.take_damage(obs.damage)
                    # Check if the player has lost all health
                    if self.player.health <= 0:
                        print("Game over! You've been defeated by the obstacles.")
                        return False
        return True

    def check_health_pickup(self):
        if (self.player.x, self.player.y) in self.health_pickups:
            self.player.gain_health()
            self.health_pickups.remove((self.player.x, self.player.y))

    def play(self):
        print("Welcome to the Grid Navigator with Health Pickups and Larger Playing Area!")
        print("Move the '@' character to reach the '$'. Avoid the obstacles '#' that harm you and collect 'H' to regain health.")
        print("Controls: w = up, a = left, s = down, d = right\n")
        while True:
            self.display_grid()
            if self.player.x == self.target.x and self.player.y == self.target.y:
                print("Congratulations! You've reached the target!")
                break
            if not self.check_collision():
                break
            move = input("Move (w, a, s, d): ").lower()
            if move in ["w", "s", "a", "d"]:
                self.player.move(move, self.obstacles.union((o.x, o.y) for o in self.moving_obstacles))
                self.check_health_pickup()
            else:
                print("Invalid move. Please enter 'w', 'a', 's', or 'd'.")
                continue
            self.update_obstacles()
            print()

if __name__ == "__main__":
    game = Game()
    game.play()>