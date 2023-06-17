import socket
import sys
import pygame
import random
import time
import threading


enemy_car_x_positions = [35, 180, 325, 470]
enemy_data = []
my_name = ""
chat_data = []
players_data = []
players = []
player1_data = []
# player2_data = []
player1_game_over = False


def receive_data():
    global player1_game_over
    while True:
        # Receive player data of other clients from the server
        received_data = client_socket.recv(2048)

        if received_data:
            # Split received data into a list of strings
            data_list = received_data.decode().split(",")

            for data in data_list:
                if data == "end":
                    player.game_over = True
                elif data.startswith('m'):
                    chat_data.append(data[1:])
                elif data[:-1].isdigit():
                    if data.endswith("e"):
                        enemy_data.append(data[:-1])

                # Check if the received data starts with the player names
                elif data.startswith(str(players[1])):
                    # Remove ':p' from the data
                    data = data.replace(':p', '')

                    # Extract player data after the first colon
                    player_data = data.split(':')[1]
                    player1_data.append(player_data)

                    # Extract boolean value after the second colon and store it in player1_game_over
                    game_over_text = data.split(':')[2]
                    boolean_value = (game_over_text == "True")
                    player1_game_over = bool(boolean_value)
                    print(boolean_value)

            print(player1_data)


class Player:
    def __init__(self, x, y, width, height, speed, y_speed, score, game_over, car_rect):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.y_speed = y_speed
        self.score = score
        self.game_over = game_over
        self.car_rect = car_rect

    def move(self, direction):
        if direction == 'left':
            self.speed = -5
        elif direction == 'right':
            self.speed = 5
        elif direction == 'up':
            self.y_speed = -5
            self.score += 50
        elif direction == 'down':
            self.y_speed = 5
        elif direction == 'slow':
            self.y_speed = 3
        elif direction == 'none':
            self.speed = 0
            # self.y_speed = 0

    def check_limits(self):
        # Limit the car's movement to within 600 pixels from the left edge of the screen.
        if self.x < 10:
            self.x = 10
        if self.x > 560 - self.width:
            self.x = 560 - self.width
        if self.y < 20:
            self.y = 20
        if self.y < 300:  # Limit car to the top half of the screen
            self.y = 300
        if self.y > 550:
            self.y = 550

    def update(self):
        self.x += self.speed
        self.y += self.y_speed

    def draw(self, name):
        screen.blit(car_image, (self.x, self.y))
        my_text = pygame.font.Font(None, 24)
        my_text_surface = my_text.render(f'{name}', True, (255, 255, 255))
        screen.blit(my_text_surface, (self.x + 90, self.y + 0))


class EnemyCar:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def update(self):
        self.y += self.speed

    def define_car(self):
        self.car_rect = pygame.Rect(player.x, player.y, player.width, player.height)


class Track:
    def __init__(self, y, speed, y_speed):
        self.y = y
        self.speed = speed
        self.y_speed = y_speed

    def update(self):
        self.y += self.speed
        self.y_speed = player.y_speed  # Update track's vertical speed based on the player's y_speed

    def draw(self):
        screen.blit(track_image, (0, self.y))
        screen.blit(track_image, (0, self.y + 800))

    def reset(self):
        if self.y > 0:
            self.y = -800


class ChatBox:
    def __init__(self, x, y, w, h, font, max_lines):
        self.rect = pygame.Rect(x, y, w, h)
        self.input_box = pygame.Rect(x + 10, y + h - 60, w - 20, 50)  # Adjusting input box size and position
        self.font = font
        self.text_color = (255, 255, 255)
        self.lines = []
        self.max_lines = max_lines
        self.text = ""
        self.cursor_visible = True  # For the cursor visibility toggle

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.input_box, 2)
        self._draw_text(surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.lines.append(f"{my_name}: {self.text}")  # Appending the new message at the bottom of the list
                client_socket.sendall(f"m{my_name}: {str(self.text)}".encode())
                self.text = ""
                while len(self.lines) > self.max_lines:
                    self.lines.pop(0)  # Removing the first message if there are too many
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.text = self.text[:self.input_box.w // self.font.size(' ')[0]]  # Prevent text overflow

    def _draw_text(self, surface):
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        y = self.rect.y + 3  # Start at the top of the chatbox
        for line in self.lines:  # Iterate from the start of the list
            line_surface = self.font.render(line, True, self.text_color)
            surface.blit(line_surface, (self.rect.x + 5, y))
            y += self.font.get_linesize()  # Move down for the next line

    def update(self, dt):
        # Cursor blinking logic
        if pygame.time.get_ticks() % 1000 // 500 == 0:
            if self.cursor_visible:
                self.text += "|"
            else:
                if self.text.endswith("|"):
                    self.text = self.text[:-1]
            self.cursor_visible = not self.cursor_visible


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color((137, 137, 137))
        self.color_active = pygame.Color('white')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global my_name

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    client_socket.sendall(self.text.encode())
                    my_name = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Render the new text but don't add it yet
                    new_text = self.text + event.unicode
                    new_txt_surface = self.font.render(new_text, True, self.color)

                    # Only add the new text if it fits within the input box
                    if new_txt_surface.get_width() <= self.rect.w:
                        self.text = new_text

                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def won():
    countdown_value = 100  # Initial countdown value
    font = pygame.font.Font(None, 36)

    game_over_text = font.render("Game ezzz", True, (255, 0, 0))
    screen.blit(game_over_text, (250, 400))
    pygame.display.update()

    # Pause for 2 seconds.
    time.sleep(2)

    while countdown_value > 0:
        # Display Start Screen
        screen.blit(start_screen_image, (0, 0))

        # Display the countdown value
        countdown_text = font.render("Closing in " + str(countdown_value), True, (137, 137, 137))
        countdown_rect = countdown_text.get_rect(center=(400, 400))
        screen.blit(countdown_text, countdown_rect)

        pygame.display.update()

        countdown_value -= 1  # Update the countdown value

    # Kick
    pygame.quit()
    sys.exit(0)

def waiting_for_others():
    print("i am here")
    while True:
        screen.blit(start_screen_image, (0, 0))
        waiting_font = pygame.font.Font(None, 42)
        waiting_surface = waiting_font.render('Waiting for other players to connect!', True, (137, 137, 137))
        screen.blit(waiting_surface, (250, 420))
        pygame.display.update()

        countdown_value = 10
        start_sginal = client_socket.recv(2048).decode()
        print(f"start: {start_sginal}")
        if start_sginal == "1":
            time.sleep(5)
            # while countdown_value > 0:
            #     # Display the countdown value
            #     countdown_surface = waiting_font.render("Starting in " + str(countdown_value), True, (137, 137, 137))
            #     screen.blit(countdown_surface, (230, 420))
            #
            #     pygame.display.update()
            #     clock.tick(1)  # Set the frame rate to 1 second per tick
            #
            #     countdown_value -= 1  # Update the countdown value
            break


def receive_player_names():
    while True:
        screen.blit(start_screen_image, (0, 0))
        waiting_font = pygame.font.Font(None, 42)
        waiting_surface = waiting_font.render('Waiting for other players to connect!', True, (137, 137, 137))
        screen.blit(waiting_surface, (250, 420))
        pygame.display.update()

        # Receive and decode the list of player names
        received_data = client_socket.recv(2048)
        player_names = received_data.decode().split(', ')
        print(player_names)

        if my_name in player_names:
            player_names.remove(my_name)
            player_names.insert(0, my_name)
        else:
            pass

        # Loop over the list of player names
        for name in player_names:
            players.append(name)
        break


def get_start_position(player):
    print("i am there")
    while True:
        start_position = client_socket.recv(2048).decode()
        print(start_position)
        if start_position == "35" or start_position == "180" or start_position == "325" or start_position == "470":
            player.x = int(start_position)
            time.sleep(1)
            break
        else:
            pass


# Create a socket for client-server communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 6666)  # Update with your server IP address and port
client_socket.connect(server_address)


def main():
    global screen, start_screen_image, track_image, car_image, allow, player1_game_over
    player1_previous_x = 0
    player1_previous_y = 0
    counter = 0
    reached_10000 = False

    # Initialize Pygame
    pygame.init()

    # Set screen size
    screen = pygame.display.set_mode((1000, 800))

    # Load images
    start_screen_image = pygame.image.load('start_screen.png')
    track_image = pygame.image.load('track.png')
    car_image = pygame.image.load('car.png')
    enemy_car_image = pygame.image.load('enemy_car.png')

    global player
    player = Player(35, 550, 60, 120, 0, 0, 0, False, None)

    global enemy_car
    enemy_car_width = 90
    enemy_car_height = 220
    enemy_car_x = 325
    enemy_car_y = -600
    enemy_car_speed = 7
    enemy_car = EnemyCar(enemy_car_x, enemy_car_y, enemy_car_width, enemy_car_height, enemy_car_speed)

    global track
    track_y = 0
    track_speed = 10
    track_y_speed = 30
    track = Track(track_y, track_speed, track_y_speed)

    # Chat
    chat_font = pygame.font.Font(None, 30)
    chat_box = ChatBox(600, 0, 400, 800, chat_font, 30)

    allow = True

    # Load font
    font = pygame.font.Font(None, 36)

    # Create clock object to control frame rate
    clock = pygame.time.Clock()

    # my_text = pygame.font.Font(24)

    input_box = InputBox(450, 400, 240, 30)
    input_box_font = pygame.font.Font(None, 32)
    welcome_text_font = pygame.font.Font(None, 22)
    text_surface = input_box_font.render('Enter Name: ', True, (137, 137, 137))
    welcome_surface = welcome_text_font.render('Write your name and press ENTER to start! ', True, (137, 137, 137))

    # Start input loop
    input_done = False
    while not input_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)  # exit the program if the user closes the window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and input_box.active:
                input_done = True
            input_box.handle_event(event)

        # Display Start Screen
        screen.blit(start_screen_image, (0, 0))

        # Draw the "Enter Name: " text
        screen.blit(text_surface, (input_box.rect.x - text_surface.get_width(), input_box.rect.y + 4))

        # Draw Welcome Text
        screen.blit(welcome_surface, (355, 480))

        # Draw the input box on the screen
        input_box.draw(screen)

        # Update the display
        pygame.display.update()

    receive_player_names()

    get_start_position(player)

    waiting_for_others()

    # Start a new thread to receive data from the server
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

    # Game Loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move('left')
                elif event.key == pygame.K_RIGHT:
                    player.move('right')
                elif event.key == pygame.K_UP:
                    player.move('up')
                elif event.key == pygame.K_DOWN:
                    player.move('down')
                elif event.key == pygame.K_x:
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.move('none')
                elif event.key == pygame.K_DOWN:
                    player.move('none')
                elif event.key == pygame.K_UP:
                    player.move('slow')
            if event.type == pygame.KEYDOWN:
                chat_box.handle_event(event)

        if not player.game_over:

            if chat_data:
                while len(chat_box.lines) > chat_box.max_lines:
                    chat_box.lines.pop(0)
                chat_box.lines.append(chat_data[0])
                chat_data.pop(0)

            # Update car position
            player.update()

            # Prevent car from going off-screen
            player.check_limits()

            # Extract relevant data from player object and send it to the server as a string
            player_data = f"{my_name}:{player.x}&{player.y}:{player.game_over}:p"
            client_socket.sendall(player_data.encode())

            # # Define car bounding rectangle
            # player.define_car()
            #
            # # Define enemy car bounding rectangle
            # enemy_car.define_car()

            # Define car bounding rectangle
            car_rect = pygame.Rect(player.x, player.y, car_image.get_width(), car_image.get_height())

            # Define enemy car bounding rectangle
            enemy_car_rect = pygame.Rect(enemy_car.x, enemy_car.y, enemy_car_image.get_width(), enemy_car_image.get_height())

            # Define car bounding rectangle
            # car_rect1 = pygame.Rect(player1.x, player1.y, car_image.get_width(), car_image.get_height())

            # if car_rect.colliderect(car_rect1):
            #     # If collision detected, stop the movement in the direction of the collision
            #     if player.speed > 0:  # moving right
            #         allowed_movement['right'] = False
            #     elif player.speed < 0:  # moving left
            #         allowed_movement['left'] = False
            #     if player.y_speed > 0:  # moving down
            #         allowed_movement['down'] = False
            #     elif player.y_speed < 0:  # moving up
            #         allowed_movement['up'] = False
            #
            # # Check if the cars are no longer colliding
            # if not car_rect.colliderect(car_rect1):
            #     allowed_movement['right'] = True
            #     allowed_movement['left'] = True
            #     allowed_movement['down'] = True
            #     allowed_movement['up'] = True

            # Check for collision between car and enemy car
            if car_rect.colliderect(enemy_car_rect):
                player.game_over = True

            # Update track position
            track.update()

            # Reset track
            track.reset()

            # Draw track
            track.draw()

            # Draw car
            player.draw(my_name)

            if player1_data:
                for player_data in player1_data:
                    try:
                        x, y = map(int, player_data.split("&"))
                        player1_previous_x, player1_previous_y = x, y
                        screen.blit(car_image, (x, y))
                        player_text = pygame.font.Font(None, 24)
                        player_surface = player_text.render(f"{players[1]}", True, (255, 255, 255))
                        screen.blit(player_surface, (x + 90, y + 0))
                    except (ValueError, IndexError):
                        # Handle the error, such as logging or skipping the problematic data
                        pass
                player1_data.clear()  # Clear the processed positions
            elif not player1_game_over:
                # Use the previous x and y positions to draw the player's car
                x, y = player1_previous_x, player1_previous_y
                screen.blit(car_image, (x, y))
                player_text = pygame.font.Font(None, 24)
                player_surface = player_text.render(f"{players[1]}", True, (255, 255, 255))
                screen.blit(player_surface, (x + 90, y + 0))
            else:
                x, y = -200, -200
                screen.blit(car_image, (x, y))
                player_text = pygame.font.Font(None, 24)
                player_surface = player_text.render(f"{players[1]}", True, (255, 255, 255))
                screen.blit(player_surface, (x + 90, y + 0))

            # if player2_data:
            #     # screen.fill((0, 0, 0, 0), (0, 0, 600, 800))  # Clear the screen with transparency
            #
            #     for player_data in player2_data:
            #         try:
            #             x, y = map(int, player_data.split("&"))
            #             screen.blit(car_image, (x, y))
            #             player_text = pygame.font.Font(None, 24)
            #             player_surface = player_text.render(f'{players[2]}', True, (255, 255, 255))
            #             screen.blit(player_surface, (x + 90, y + 0))
            #         except (ValueError, IndexError):
            #             # Handle the error, such as logging or skipping the problematic data
            #             pass
            #
            #     player2_data.clear()  # Clear the processed positions

            if enemy_data:
                # screen.fill((0, 0, 0, 0), (0, 0, 600, 800))  # Clear the screen with transparency
                if allow:
                    for enemy in enemy_data:
                        try:
                            x = int(enemy.split(",")[0])
                            # screen.blit(enemy_car_image, (x, enemy_car.y))
                            enemy_car.x = x
                        except (ValueError, IndexError):
                            print("xDDDDDDDDDDdd")
                    enemy_data.clear()  # Clear the processed positions
                    allow = False

            # Update enemy car position
            enemy_car.update()

            # If enemy_car goes down the window
            if enemy_car.y > 800:
                enemy_car.y = -600
                allow = True

            # Draw the enemy car on the screen
            screen.blit(enemy_car_image, (enemy_car.x, enemy_car.y))

            # Draw score
            score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
            screen.blit(score_text, (5, 5))

            counter += 1

            if counter % 200:
                # Increment score by one each time the game loop runs.
                player.score += 1
                if player.score > 3000:
                    score_message = f"s{my_name}:{str(player.score)}"
                    client_socket.sendall(score_message.encode())
                    won()

            # if player.score >= 10000 and not reached_10000:
            #     end = "end"
            #     client_socket.sendall(end.encode())
            #     won()
        else:

            player_data = f"{my_name}:{player.x}&{player.y}:{player.game_over}:p"
            client_socket.sendall(player_data.encode())

            countdown_value = 100  # Initial countdown value

            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (250, 400))
            pygame.display.update()

            # Pause for 2 seconds.
            time.sleep(2)

            while countdown_value > 0:
                # Display Start Screen
                screen.blit(start_screen_image, (0, 0))

                # Display the countdown value
                countdown_text = font.render("Closing in " + str(countdown_value), True, (137, 137, 137))
                countdown_rect = countdown_text.get_rect(center=(400, 400))
                screen.blit(countdown_text, countdown_rect)

                pygame.display.update()
                clock.tick(1)  # Set the frame rate to 1 second per tick

                countdown_value -= 1  # Update the countdown value

            # Kick
            pygame.quit()
            sys.exit(0)

        chat_box.draw(screen)

        # Update display
        pygame.display.flip()

        # Limit frame rate to 60 FPS.
        clock.tick(60)


if __name__ == '__main__':
    main()
