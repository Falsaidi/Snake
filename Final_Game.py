# If anyone's reading this, I would just like to say that H.A.N.S. has been one of my absolute favourite projects as of
# yet. I just sat here for like 15 minutes watching him do his thing and I can't help to be proud of what this has
# turned into. While the A.I. is quite simple and could absolutely be improved, the memories I'll have of creating him
# and showing him off to people is going to be something I hold onto for the rest of my life, and I can't say enough
# how happy I am to be in the position that I am. From the demo day with Anmol, Jackson, Nicole, Mia, and Mr. Fershau,
# and selling the raffle tickets at the hockey game with the musical peeps, I can't say enough how great this year has
# turned out to be and I hope it only gets better from here. H.A.N.S. has been such an incredible project for me these
# past couple of months, and while I do hope to always cherish the time I had developing him, this will likely be the
# last time I edit this code. Thanks for everything H.A.N.S.! lol

# Finished January 31, 2020

import pygame
import random
import threading
import sys
from time import sleep

# Initializes the screen and all variables
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Sets the screen to full screen
screen.fill((200, 200, 200))
screen_font = pygame.font.SysFont("arial", 22)
button_font = pygame.font.SysFont("arial", 40)
title_font = pygame.font.SysFont("arial", 60)
subtitle_font = pygame.font.SysFont("arial", 28)
name_font = pygame.font.SysFont("arial", 18)
done = False
directions = ["UP", "DOWN", "LEFT", "RIGHT"]
game_width = 40
game_height = 40
update_time = 0.065
ai_bool = True
iteration = 1
max_length = 0
start_length = 3
block_colours = [(255, 255, 255), (0, 0, 0), (255, 255, 0), (200, 200, 200), (0, 0, 210)]
length = 3
last_right = False
snake_one, snake_two, map_obj = [], [], []
snake_positions = []
against = False
hour = "00"
minute = "00"
second = "00"
time = ""
win_condition = 50


# Displays the number of lives left for the player
def display_lives():
    global snake_one
    screen.fill((200, 200, 200), (screen.get_width() - 60, 0, screen.get_width(), 90))
    lives_text = screen_font.render(" X" * snake_one.lives, True, (255, 0, 0))
    screen.blit(lives_text, (screen.get_width() - 60, 5))


# Displays the current length in the upper right corner
def display_value():
    global snake_one
    global snake_two
    screen.fill((200, 200, 200), (screen.get_width()-250, screen.get_height()-90,
                                  screen.get_width(), screen.get_height()))

    # This try block is in case only one snake exists, as if that's the case, an error will be raised as I try to
    # grab a value from the non-existent second snake
    try:
        iteration_text_one = screen_font.render(f"Your (Black) Length: {snake_one.length}", True, (0, 0, 0))
        iteration_text_two = screen_font.render(f"H.A.N.S. (Blue) Length: {snake_two.length}", True, (0, 0, 0))
        screen.blit(iteration_text_one, (screen.get_width() - 206, screen.get_height()-60))
        screen.blit(iteration_text_two, (screen.get_width() - 230, screen.get_height()-30))
    except AttributeError:
        screen.fill((200, 200, 200), (screen.get_width() - 175, 0, screen.get_width(), 30))
        iteration_text = screen_font.render("Current Length: " + str(snake_one.length), True, (0, 0, 0))
        screen.blit(iteration_text, (screen.get_width() - 175, 0))


# Displays the max score reached in the bottom left corner
def max_score(snek_length):
    global max_length
    if snek_length > max_length:
        max_length = snek_length

    screen.fill((200, 200, 200), (0, screen.get_height()-30, 150, screen.get_height()))
    max_length_text = screen_font.render(f"Max Length: {max_length}", True, (0, 0, 0))
    screen.blit(max_length_text, (0, screen.get_height()-30))


# Returns a random position within the map that isn't already occupied by the snake
def rand_pos(first=False):
    global snake_one
    global snake_two
    position = [random.randint(5, 35), random.randint(5, 35)]
    if not first:
        if snake_two:
            while position in snake_one.positions or position in snake_two.positions:
                position = [random.randint(5, 35), random.randint(5, 35)]
        else:
            while position in snake_one.positions:
                position = [random.randint(5, 35), random.randint(5, 35)]
    return position


# Holding the spot as one of the worst functions I've ever created, this function returns a specific direction for the
# snake to follow to allow to it to follow a specific path I've created to win
def return_direction(snek_pos):
    x = snek_pos[0][0]
    y = snek_pos[0][1]
    if 1 < x < game_width-2:
        if y == game_height-3 or y == 2:
            if y == game_height-3:
                return "RIGHT" if x % 2 == 1 else "UP"
            else:
                return "RIGHT" if x % 2 == 0 else "DOWN"
        elif y == 1:
            return "LEFT"
        else:
            return "UP" if x % 2 == 0 else "DOWN"
    elif x == game_width - 2:
        return "UP" if y != 1 else "LEFT"
    elif x == 1:
        return "DOWN" if y != game_height-3 else "RIGHT"


# Evaluates whether or not the path to the goal is safe for the snake to take
def check_path(snek_pos, goal_pos):
    increment_x = 1 if goal_pos[0] < snek_pos[0][0] else -1
    increment_y = 1 if goal_pos[1] < snek_pos[0][1] else -1
    global map_obj
    for i in range(goal_pos[0], snek_pos[0][0], increment_x):
        if map_obj.map_obj[i][snek_pos[0][1]] in (1, 3, 4):
            return False
    for i in range(goal_pos[1], snek_pos[0][1], increment_y):
        if map_obj.map_obj[goal_pos[0]][i] in (1, 3, 4):
            return False
    return True


# Checks the direction given to see if a hazardous block exists, returning True if not and False otherwise
def check_direction(snek_pos, direction):
    global map_obj
    x = snek_pos[0][0]
    y = snek_pos[0][1]
    if direction == "LEFT":
        if map_obj.map_obj[x-1][y] in (1, 3, 4):
            return False
    elif direction == "RIGHT":
        if map_obj.map_obj[x+1][y] in (1, 3, 4):
            return False
    elif direction == "UP":
        if map_obj.map_obj[x][y-1] in (1, 3, 4):
            return False
    elif direction == "DOWN":
        if map_obj.map_obj[x][y+1] in (1, 3, 4):
            return False
    return True


# This is just the screen that pops up when the player dies in the "vs" mode
def dead():
    global map_obj
    global screen
    global title_font
    global button_font

    while True:

        pygame.event.get()

        # Checks to see if the game should be closed (or if it should restart)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window()
                return 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                close_window()
                return 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                screen.fill((200, 200, 200), (0, 0, screen.get_width(), screen.get_height()))
                main_one()

        # If the player clicks on one of the buttons, it sends them to the corresponding screen
        if pygame.mouse.get_pressed()[0]:
            if screen.get_width() / 2 + 50 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 + 360 and \
                    screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
                start()
                return 0
            elif screen.get_width() / 2 - 300 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 - 80 and \
                    screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
                screen.fill((200, 200, 200), (0, 0, screen.get_width(), screen.get_height()))
                main_one()
                return 0

        # Renders the buttons and text, as well as setting up the hover animations and such
        title = title_font.render("Oh No You Died ;(", True, (255, 0, 0))
        screen.blit(title, (screen.get_width() / 2 - 250, screen.get_height() / 2 - 150))

        if screen.get_width() / 2 - 255 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 - 110 and \
                screen.get_height() / 2 + 10 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 50:
            again = button_font.render("Try Again", True, (100, 100, 100))
            home = button_font.render("Home", True, (0, 0, 0))
        elif screen.get_width() / 2 + 50 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 + 150 and \
                screen.get_height() / 2 + 10 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 50:
            again = button_font.render("Try Again", True, (0, 0, 0))
            home = button_font.render("Home", True, (100, 100, 100))
        else:
            again = button_font.render("Try Again", True, (0, 0, 0))
            home = button_font.render("Home", True, (0, 0, 0))

        screen.fill((255, 255, 255), (screen.get_width() / 2 - 270, screen.get_height() / 2, 175, 70))
        screen.fill((255, 255, 255), (screen.get_width() / 2 + 30, screen.get_height() / 2, 125, 70))
        screen.blit(again, (screen.get_width() / 2 - 250, screen.get_height() / 2 + 10))
        screen.blit(home, (screen.get_width() / 2 + 50, screen.get_height() / 2 + 10))

        pygame.display.flip()


# This is the screen that pops up when the player wins
def win():
    global map_obj
    global screen
    global title_font
    global button_font

    while True:

        pygame.event.get()

        # Checks to see if the window should be closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window()
                return 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                close_window()
                return 0

        # If the player presses on a button, it sends them to the corresponding screen
        if pygame.mouse.get_pressed()[0]:
            if screen.get_width() / 2 + 50 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 + 360 and \
                    screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
                start()
                return 0
            elif screen.get_width() / 2 - 300 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 - 80 and \
                    screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
                screen.fill((200, 200, 200), (0, 0, screen.get_width(), screen.get_height()))
                main_one()
                return 0

        # Renders the buttons and text, as well as handling the hover animations and such
        title = title_font.render("Oh Hey You Won :D", True, (0, 255, 0))
        screen.blit(title, (screen.get_width() / 2 - 250, screen.get_height() / 2 - 150))

        if screen.get_width() / 2 - 255 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 - 110 and \
                screen.get_height() / 2 + 10 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 50:
            again = button_font.render("Play Again", True, (100, 100, 100))
            home = button_font.render("Home", True, (0, 0, 0))
        elif screen.get_width() / 2 + 50 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 + 150 and \
                screen.get_height() / 2 + 10 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 50:
            again = button_font.render("Play Again", True, (0, 0, 0))
            home = button_font.render("Home", True, (100, 100, 100))
        else:
            again = button_font.render("Play Again", True, (0, 0, 0))
            home = button_font.render("Home", True, (0, 0, 0))

        screen.fill((255, 255, 255), (screen.get_width() / 2 - 270, screen.get_height() / 2, 175, 70))
        screen.fill((255, 255, 255), (screen.get_width() / 2 + 30, screen.get_height() / 2, 125, 70))
        screen.blit(again, (screen.get_width() / 2 - 260, screen.get_height() / 2 + 10))
        screen.blit(home, (screen.get_width() / 2 + 50, screen.get_height() / 2 + 10))

        pygame.display.flip()


# It's the map it's the map it's the map it's the map it's the maaaaaaap
class Map:
    def __init__(self, snek, goal):
        self.map_obj = []
        self.reset()
        self.snek = snek
        self.goal = goal
        self.second = "00"
        self.minute = "00"
        self.hour = "00"
        self.display_time()
        self.time = ""

    # Displays the time in the upper left corner
    def display_time(self):
        self.time = threading.Timer(1, self.display_time)
        self.time.start()
        screen.fill((200, 200, 200), (0, 0, 100, 30))
        if int(self.second) < 59:
            self.second = str(int(self.second) + 1)
            if len(self.second) == 1:
                self.second = "0" + self.second
        else:
            if int(self.minute) < 59:
                self.minute = str(int(self.minute) + 1)
                if len(self.minute) == 1:
                    self.minute = "0" + self.minute
            else:
                if int(self.hour) < 59:
                    self.hour = str(int(self.hour) + 1)
                    if len(self.hour) == 1:
                        self.hour = "0" + self.hour
                    self.minute = "00"
            self.second = "00"
        time_text = screen_font.render(f"{self.hour}:{self.minute}:{self.second}", True, (0, 0, 0))
        screen.blit(time_text, (0, 0))

    # Resets the map_obj to its initial state
    def reset(self):
        self.map_obj = []
        temp = []
        for i in range(game_height):
            for j in range(game_width):
                if i == 0 or i == game_width-1 or j == 0 or j == game_height-1:
                    temp.append(3)
                else:
                    temp.append(0)
            self.map_obj.append(temp)
            temp = []

    # Updates the map_obj to contain both the snake and the goal
    def update(self):
        display_value()
        global snake_positions
        global snake_one
        global snake_two
        map_obj.snek = snake_positions

        # If the snake has reached a goal then run the function again to ensure that it doesn't look janky
        if snake_one.positions[0] == map_obj.goal:
            snake_one.length += 2
            map_obj.goal = rand_pos()
            return 1
        if snake_two:
            if snake_two.positions[0] == map_obj.goal:
                snake_two.length += 2
                map_obj.goal = rand_pos()
                return 1

        # Places the snake and goal within the map_obj
        for i in snake_one.positions:
            exec(f"self.map_obj[{i[0]}][{i[1]}] = 1")
        if snake_two:
            for i in snake_two.positions:
                exec(f"self.map_obj[{i[0]}][{i[1]}] = 4")
        exec(f"self.map_obj[{self.goal[0]}][{self.goal[1]}] = 2")

        # Determines the screen size and how large the individual blocks need to be
        surface = pygame.display.get_surface()
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        block_x = 0
        block_y = 0
        if surface_height < surface_width:
            block_width = (surface_width * 0.55) / 40
            block_height = block_width
        else:
            block_height = (surface_height * 0.55) / 40
            block_width = block_height

        # Draws the map onto the screen
        global block_colours
        for i in range(0, game_width):
            for j in range(0, game_height):
                pygame.draw.rect(screen, block_colours[map_obj.map_obj[i][j]], (
                    surface_width * 0.2 + (block_width * i), surface_height * 0.01 + (block_height * j), block_width,
                    block_height), 0)

                block_x += 1
                block_y += 1


# Snek will eat
class Snek:
    def __init__(self, start_pos, direction, ai=False):
        self.start, self.positions = start_pos, start_pos
        self.direction = direction
        global start_length
        self.length = start_length
        self.ai = ai
        self.lives = 3
        self.t = ""

    # Updates the position of the snake
    def update(self):
        global map_obj
        self.t = threading.Timer(update_time, self.update)
        self.t.start()

        if not self.ai:
            display_lives()

        # Extends the snake if needed
        if len(self.positions) < self.length:
            self.positions.append([])

        # Moves the snake forward
        i = len(self.positions)-1
        while i >= 1:
            self.positions[i] = list(self.positions[i-1])
            i -= 1

        global last_right

        # Makes the decision for H.A.N.S. to see where he should go next
        if self.ai:
            if not check_path(self.positions, map_obj.goal):
                new_direction = return_direction(self.positions)
                if check_direction(self.positions, new_direction):
                    self.direction = new_direction
                else:
                    x = self.positions[0][0]
                    y = self.positions[0][1]
                    if not last_right:
                        if map_obj.map_obj[x-1][y] in (0, 2):
                            self.direction = "LEFT"
                        elif map_obj.map_obj[x+1][y] in (0, 2):
                            self.direction = "RIGHT"
                        elif map_obj.map_obj[x][y-1] in (0, 2):
                            self.direction = "UP"
                        elif map_obj.map_obj[x][y+1] in (0, 2):
                            self.direction = "DOWN"
                    else:
                        if map_obj.map_obj[x+1][y] in (0, 2):
                            self.direction = "RIGHT"
                        elif map_obj.map_obj[x-1][y] in (0, 2):
                            self.direction = "LEFT"
                        elif map_obj.map_obj[x][y-1] in (0, 2):
                            self.direction = "UP"
                        elif map_obj.map_obj[x][y+1] in (0, 2):
                            self.direction = "DOWN"
            else:
                if self.positions[0][0] != map_obj.goal[0]:
                    self.direction = "RIGHT" if self.positions[0][0] < map_obj.goal[0] else "LEFT"
                elif self.positions[0][1] != map_obj.goal[1]:
                    self.direction = "DOWN" if self.positions[0][1] < map_obj.goal[1] else "UP"

        # Moves the head of the snake based on the direction entered by the user
        if self.direction == "LEFT":
            self.positions[0][0] -= 1
            last_right = False
        elif self.direction == "RIGHT":
            self.positions[0][0] += 1
            last_right = True
        elif self.direction == "UP":
            self.positions[0][1] -= 1
        elif self.direction == "DOWN":
            self.positions[0][1] += 1

        # Checks whether the snake has died or not
        if self.positions[0][0] in (0, 39) or (
                self.positions[0][1] in (0, 39) or
                map_obj.map_obj[self.positions[0][0]][self.positions[0][1]] in (1, 4)):
            global start_length
            if against and not self.ai:
                self.lives -= 1
            self.length = start_length
            self.positions = [rand_pos()]
            self.direction = rand_element(directions)

        # Resets and updates the map to account for the new snake position
        map_obj.reset()
        m = map_obj.update()
        if m:
            map_obj.update()


# Returns a random element within an array (I'm going to be honest I have no idea why the fuck I needed this)
def rand_element(arr):
    return arr[random.randint(0, len(arr)-1)]


# Closes the window and exits the game once the program ends
def close_window():
    global snake_one
    global snake_two
    if snake_one:
        snake_one.t.cancel()
    if snake_two:
        snake_two.t.cancel()
    if map_obj.time:
        map_obj.time.cancel()
    pygame.quit()
    sys.exit()


# This just returns one of two directions at random (good for starting the player off in a fair position and direction)
def rand_direction_lim():
    if random.randint(0, 2) == 0:
        return "RIGHT"
    else:
        return "DOWN"


# Runs the "vs" mode of the game where you go against H.A.N.S.
def main_one():
    global against
    global time
    global snake_one
    global snake_two
    global map_obj
    global snake_positions
    global directions
    global win_condition

    snake_one = ''
    snake_two = ''
    map_obj = ''
    against = True
    start_func = False
    # Runs the main portion of the code
    while True:

        # Initializes the snake and map_obj
        if not start_func:
            snake_one = Snek([[10, 10]], rand_direction_lim(), ai=False)
            snake_two = Snek([[30, 30]], rand_element(directions), ai=True)
            snake_positions = [snake_one.positions, snake_two.positions]
            map_obj = Map(snake_positions, rand_pos(True))
            snake_one.update()
            snake_two.update()
            display_value()
            start_func = True

        if snake_one.lives == 0:
            snake_one.t.cancel()
            snake_two.t.cancel()
            map_obj.time.cancel()
            display_lives()
            dead()
            break

        elif snake_one.length > win_condition:
            snake_one.t.cancel()
            snake_two.t.cancel()
            map_obj.time.cancel()
            win()
            break

        # Determines whether the user has entered a key that corresponds to a direction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                close_window()

            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and snake_one.direction != "DOWN":
                    snake_one.direction = "UP"
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and snake_one.direction != "UP":
                    snake_one.direction = "DOWN"
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and snake_one.direction != "RIGHT":
                    snake_one.direction = "LEFT"
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and snake_one.direction != "LEFT":
                    snake_one.direction = "RIGHT"

        # Updates the screen
        pygame.display.flip()


# Runs the "watch" version of the game where you simply just watch H.A.N.S. do his thing
def main_two():
    start_func = False
    global done
    global snake_one
    global snake_two
    global map_obj

    button_font2 = pygame.font.SysFont("arial", 30)

    snake_one = ''
    snake_two = ''
    map_obj = ''

    # Runs the main portion of the code
    while not done:

        # Initializes the snake and map_obj
        if not start_func:
            global directions
            snake_one = Snek([[20, 20]], rand_element(directions), ai=ai_bool)
            map_obj = Map(snake_one.positions, rand_pos(snake_one.positions))
            snake_one.update()
            display_value()
            start_func = True

        # Determines whether the user has entered a key that corresponds to a direction or wants to close the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                close_window()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
                close_window()

        screen.fill((200, 200, 200), (0, screen.get_height() - 60, 75, 60))

        # Checks to see if the player pressed the back button, sending them back to the home screen if they did
        if 0 <= pygame.mouse.get_pos()[0] <= 60 and \
                screen.get_height() - 30 <= pygame.mouse.get_pos()[1] <= screen.get_height():
            if pygame.mouse.get_pressed()[0]:
                snake_one.t.cancel()
                map_obj.time.cancel()
                start()
            back = button_font2.render("Back", True, (100, 100, 100))
        else:
            back = button_font2.render("Back", True, (0, 0, 0))
        screen.blit(back, (0, screen.get_height() - 40))

        # Updates the screen
        pygame.display.flip()


# This is the home screen of the game, and is the first thing that pops up when it is opened
def start():
    sleep(0.5)
    global screen
    global done
    global against
    global title_font
    global subtitle_font
    global button_font
    global name_font
    done = True
    while True:

        screen.fill((200, 200, 200))

        pygame.event.get()

        # Checks to see if the window should close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_window()
                return 0

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                close_window()
                return 0

        # Checks to see if the user pressed on one of the buttons, sending them to the corresponding mode if so
        if pygame.mouse.get_pressed()[0]:
            if screen.get_width() / 2 + 50 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 + 360 and \
                    screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
                screen.fill((200, 200, 200), (0, 0, screen.get_width(), screen.get_height()))
                done = False
                against = True
                main_one()
                return 0
            elif screen.get_width() / 2 - 300 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 - 80 and \
                    screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
                screen.fill((200, 200, 200), (0, 0, screen.get_width(), screen.get_height()))
                done = False
                against = False
                main_two()
                return 0

        # Renders all the buttons and text, as well as the hover animations and such
        name = name_font.render("Faisal Alsaidi 2020 CS20S", True, (0, 0, 0))
        title = title_font.render(f"H.A.N.S.", True, (0, 0, 0))
        subtitle = subtitle_font.render(f"A snake algorithm lol", True, (0, 0, 0))

        if screen.get_width() / 2 - 300 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 - 80 and \
                screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
            watch = button_font.render("Watch H.A.N.S.", True, (100, 100, 100))
            against = button_font.render("Play Against H.A.N.S.", True, (0, 0, 0))
        elif screen.get_width() / 2 + 50 <= pygame.mouse.get_pos()[0] <= screen.get_width() / 2 + 360 and \
                screen.get_height() / 2 + 25 <= pygame.mouse.get_pos()[1] <= screen.get_height() / 2 + 65:
            watch = button_font.render("Watch H.A.N.S.", True, (0, 0, 0))
            against = button_font.render("Play Against H.A.N.S.", True, (100, 100, 100))
        else:
            watch = button_font.render("Watch H.A.N.S.", True, (0, 0, 0))
            against = button_font.render("Play Against H.A.N.S.", True, (0, 0, 0))

        screen.blit(name, (0, screen.get_height() - 20))
        screen.blit(title, (screen.get_width() / 2 - 90, screen.get_height() / 2 - 150))
        screen.blit(subtitle, (screen.get_width() / 2 - 100, screen.get_height() / 2 - 75))
        screen.blit(watch, (screen.get_width() / 2 - 300, screen.get_height() / 2 + 25))
        screen.blit(against, (screen.get_width() / 2 + 50, screen.get_height() / 2 + 25))
        pygame.display.flip()


# Starts the game
start()
