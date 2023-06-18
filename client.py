import json
import socket
import sys
import pygame
import random
import time
import threading

# # Initialize variables
counter = 0
enemy_pos = [35, 325, 180, 325, 470, 35, 470]
my_name = ""
players = []
player1_data = []
player2_data = []
allow = True
data_sent = ""
index = 0
sent_500 = sent_1000 = sent_1500 = sent_2000 = sent_2500 = sent_3000 = False

# Open the JSON file
with open('client_data.json', 'r') as file:
    # Load the JSON data
    data = json.load(file)


def receive_data(player, chat_box):
    global player1_game_over, allow
    while True:
        received_data = client_socket.recv(2048)

        if received_data:
            data_list = received_data.decode().split(",")

            for data in data_list:
                if data == "end":
                    player.game_over = True
                elif data.endswith(':m'):
                    while len(chat_box.lines) > chat_box.max_lines:
                        chat_box.lines.pop(0)
                    chat_box.lines.append(data[:-2])
                elif data.startswith(str(players[1])):
                    data = data.replace(':p', '')
                    player_data = data.split(':')[1]
                    player1_data.append(player_data)
                    game_over_text = data.split(':')[2]
                    boolean_value = (game_over_text == "True")
                    player1.game_over = bool(boolean_value)
                elif data.startswith(str(players[2])):
                    data = data.replace(':p', '')
                    player_data = data.split(':')[1]
                    player2_data.append(player_data)
                    game_over_text = data.split(':')[2]
                    boolean_value = (game_over_text == "True")
                    player2.game_over = bool(boolean_value)


class Player:
    def __init__(self, x, y, previous_x, previous_y, speed, y_speed, score, game_over, car_image):
        self.x = x
        self.y = y
        self.previous_x = previous_x
        self.previous_y = previous_y
        self.speed = speed
        self.y_speed = y_speed
        self.score = score
        self.game_over = game_over
        self.car_image = car_image
        self.car_rect = pygame.Rect(self.x, self.y, car_image.get_width(), car_image.get_height())

    def move(self, direction):
        if direction == 'left':
            self.speed = -5
        elif direction == 'right':
            self.speed = 5
        elif direction == 'up':
            self.y_speed = -5
            # self.score += 50
        elif direction == 'down':
            self.y_speed = 5
        elif direction == 'slow':
            self.y_speed = 3
        elif direction == 'none':
            self.speed = 0

    def check_limits(self):
        # Limit the car's movement to within 600 pixels from the left edge of the screen.
        if self.x < 10:
            self.x = 10
        if self.x > 560 - self.car_image.get_width():
            self.x = 560 - self.car_image.get_width()
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
        screen.blit(my_text_surface, (self.x + 46, self.y + 53))
        self.car_rect = pygame.Rect(self.x, self.y, car_image.get_width(), car_image.get_height())


class EnemyCar:
    def __init__(self, x, y, speed, enemy_car_image):
        self.x = x
        self.y = y
        self.speed = speed
        self.enemy_car_image = enemy_car_image
        self.car_rect = pygame.Rect(self.x, self.y, enemy_car_image.get_width(), enemy_car_image.get_height())

    def update(self):
        self.y += self.speed
        self.car_rect = pygame.Rect(self.x, self.y, enemy_car_image.get_width(), enemy_car_image.get_height())

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
                client_socket.sendall(f"{my_name}: {str(self.text)}:m".encode())
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


def write_name():
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

def won(player):
    countdown_value = 10  # Initial countdown value
    countdown_font = pygame.font.Font(None, 30)
    screen.blit(start_screen_image, (0, 0))
    won_font = pygame.font.Font(None, 60)
    won_surface = won_font.render('You won!', True, (137, 137, 137))
    screen.blit(won_surface, (410, 320))
    score_surface = won_font.render(f'Your score: {player.score}', True, (137, 137, 137))
    screen.blit(score_surface, (330, 400))
    pygame.display.update()

    while countdown_value > 0:
        # Display Start Screen
        screen.blit(start_screen_image, (0, 0))
        screen.blit(won_surface, (410, 320))
        screen.blit(score_surface, (330, 400))

        # Display the countdown value
        countdown_text = countdown_font.render("Closing in " + str(countdown_value) + " seconds.", True, (137, 137, 137))
        countdown_rect = countdown_text.get_rect(center=(500, 550))
        screen.blit(countdown_text, countdown_rect)

        pygame.display.update()

        time.sleep(1)
        countdown_value -= 1  # Update the countdown value

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the close button is clicked
                pygame.quit()
                sys.exit(0)

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
server_address = (data['ip'], data['port'])  # Update with your server IP address and port
client_socket.connect(server_address)

# Initialize Pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((1000, 800))

# Load images
start_screen_image = pygame.image.load(data['start_screen_image'])
track_image = pygame.image.load(data['track_image'])
car_image = pygame.image.load(data['car_image'])
enemy_car_image = pygame.image.load(data['enemy_car_image'])

# Player, Enemy, & Track
player = Player(35, 550, 0, 0, 0, 0, 0, False, car_image)
player1 = Player(-100, 550, 180, 550, 0, 0, 0, False, car_image)
player2 = Player(-100, 550, 325, 550, 0, 0, 0, False, car_image)
enemy_car = EnemyCar(325, -600, 5, enemy_car_image)
track = Track(0, 10, 30)

# Chat
chat_font = pygame.font.Font(None, 30)
chat_box = ChatBox(600, 0, 400, 800, chat_font, 30)

# Load font
font = pygame.font.Font(None, 36)

# Create clock object to control frame rate
clock = pygame.time.Clock()

write_name()

receive_player_names()

get_start_position(player)

waiting_for_others()

# Start a new thread to receive data from the server
receive_thread = threading.Thread(target=receive_data, args=(player, chat_box))
receive_thread.start()

# Game Loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.game_over = True
            player_data_over = f"{my_name}:{player.x}&{player.y}:{player.game_over}:p"
            client_socket.sendall(player_data_over.encode())
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move('left')
            elif event.key == pygame.K_RIGHT:
                player.move('right')
            elif event.key == pygame.K_UP:
                player.move('up')
                player.score += 50
            elif event.key == pygame.K_DOWN:
                player.move('down')
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

        if allow:
            enemy_car.x = enemy_pos[index]
            index = (index + 1) % len(enemy_pos)
            allow = False

        # Update car position
        player.update()

        # Prevent car from going off-screen
        player.check_limits()

        # Extract relevant data from player object and send it to the server as a string
        player_data = f"{my_name}:{player.x}&{player.y}:{player.game_over}:p"
        if player_data != data_sent:
            client_socket.sendall(player_data.encode())
            data_sent = player_data

        # Check for collision between car and enemy car
        if player.car_rect.colliderect(enemy_car.car_rect):
            player.game_over = True

        # Update track position
        track.update()

        # Reset track
        track.reset()

        # Draw track
        track.draw()

        # Draw car
        player.draw(my_name)

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

        if counter % 400:
            # Increment score by one each time the game loop runs.
            player.score += 1

            if player.score > 3000:
                score_message = f"s{my_name}:{str(player.score)}"
                client_socket.sendall(score_message.encode())
                score_message = f"x{my_name}:{str(3000)}"
                client_socket.sendall(score_message.encode())
                won(player)

            elif player.score > 2500 and not sent_2500:
                score_message = f"x{my_name}:{str(2500)}"
                client_socket.sendall(score_message.encode())
                sent_2500 = True

            elif player.score > 2000 and not sent_2000:
                score_message = f"x{my_name}:{str(2000)}"
                client_socket.sendall(score_message.encode())
                sent_2000 = True

            elif player.score > 1500 and not sent_1500:
                score_message = f"x{my_name}:{str(1500)}"
                client_socket.sendall(score_message.encode())
                sent_1500 = True

            elif player.score > 1000 and not sent_1000:
                score_message = f"x{my_name}:{str(1000)}"
                client_socket.sendall(score_message.encode())
                sent_1000 = True

            elif player.score > 500 and not sent_500:
                score_message = f"x{my_name}:{str(500)}"
                client_socket.sendall(score_message.encode())
                sent_500 = True

        if player1_data:
            for player_data in player1_data:
                try:
                    player1.x, player1.y = map(int, player_data.split("&"))
                    player1.previous_x, player1.previous_y = player1.x, player1.y
                    player1.draw(players[1])
                except (ValueError, IndexError):
                    pass
            player1_data.clear()  # Clear the processed positions
        elif not player1.game_over:
            player1.x, player1.y = player1.previous_x, player1.previous_y
            player1.draw(players[1])
        elif player1.game_over:
            player1.x, player1.y = -300, -300
            player1.draw(players[1])

        if player2_data:
            for player_data in player2_data:
                try:
                    player2.x, player2.y = map(int, player_data.split("&"))
                    player2.previous_x, player2.previous_y = player2.x, player2.y
                    player2.draw(players[2])
                except (ValueError, IndexError):
                    pass
            player2_data.clear()  # Clear the processed positions
        elif not player2.game_over:
            player2.x, player1.y = player2.previous_x, player2.previous_y
            player2.draw(players[2])
        elif player2.game_over:
            player2.x, player2.y = -300, -300
            player2.draw(players[2])

        if player.car_rect.colliderect(player1.car_rect) or player1.car_rect.colliderect(player.car_rect):
            player.score -= 5

        if player.car_rect.colliderect(player2.car_rect) or player2.car_rect.colliderect(player.car_rect):
            player.score -= 5

    else:

        player_data_over = f"{my_name}:{player.x}&{player.y}:{player.game_over}:p"
        client_socket.sendall(player_data_over.encode())

        countdown_value = 10  # Initial countdown value
        countdown_font = pygame.font.Font(None, 30)
        screen.blit(start_screen_image, (0, 0))
        won_font = pygame.font.Font(None, 60)
        won_surface = won_font.render('You lost!', True, (137, 137, 137))
        screen.blit(won_surface, (410, 320))
        score_surface = won_font.render(f'Your score: {player.score}', True, (137, 137, 137))
        screen.blit(score_surface, (330, 400))
        pygame.display.update()

        while countdown_value > 0:
            # Display Start Screen
            screen.blit(start_screen_image, (0, 0))
            screen.blit(won_surface, (410, 320))
            screen.blit(score_surface, (330, 400))

            # Display the countdown value
            countdown_text = countdown_font.render("Closing in " + str(countdown_value) + " seconds.", True,
                                                   (137, 137, 137))
            countdown_rect = countdown_text.get_rect(center=(500, 550))
            screen.blit(countdown_text, countdown_rect)

            pygame.display.update()

            time.sleep(1)
            countdown_value -= 1  # Update the countdown value

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the close button is clicked
                    pygame.quit()
                    sys.exit(0)

        pygame.quit()
        sys.exit(0)

    chat_box.draw(screen)

    # Update display
    pygame.display.flip()

    # Limit frame rate to 60 FPS.
    clock.tick(60)


