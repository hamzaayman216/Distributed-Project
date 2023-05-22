# from multiprocessing import connection
#
# import pygame
# import random
# import time
# import sqlite3
#
# from test import cursor
#
#
# class Player:
#     def __init__(self, x, y, width, height, speed, score, game_over, holding_state):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.speed = speed
#         self.score = score
#         self.game_over = game_over
#         self.holding_state = holding_state
#
#     def move(self, direction):
#         if direction == 'left':
#             player.speed = -5
#         elif direction == 'right':
#             player.speed = 5
#         elif direction == 'none':
#             player.speed = 0
#
#     def draw(self):
#         screen.blit(car_image, (player.x, player.y))
#
#
# class EnemyCar:
#     def __init__(self, x, y, width, height, speed):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.speed = speed
#
#     def draw(self):
#         screen.blit(enemy_car_image, (self.x, self.y))
#
#
# class Track:
#     def __init__(self, y, speed):
#         self.y = y
#         self.speed = speed
#
#     def draw(self):
#         screen.blit(track_image, (0, self.y))
#         screen.blit(track_image, (0, self.y + 800))
#
#
# def restart():
#     # Wait for user to press 's' key
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_s:
#                     # Start game
#                     player.game_over = False
#                     break
#                 elif event.key == pygame.K_q:
#                     # Quit game
#                     # Delete the data inside the database
#                     cursor.execute("DELETE FROM scores")
#                     connection.commit()
#                     # Close the database connection and cursor
#                     close_database(connection, cursor)
#                     pygame.quit()
#                     exit()
#                 elif event.key == pygame.K_m:
#                     # Start the game session and connect to the server
#                     player.holding_state = True
#                     player.game_over = False
#                     break
#         else:
#             continue
#         break
#
#
#
# def initialize_database():
#     # Create a connection to the database
#     connection = sqlite3.connect('game_data.db')
#
#     # Create a cursor object
#     cursor = connection.cursor()
#
#     # Create a table if it doesn't exist
#     cursor.execute("CREATE TABLE IF NOT EXISTS scores (score INTEGER)")
#
#     # Return the connection and cursor
#     return connection, cursor
#
#
# def update_score(connection, cursor, score):
#     # Update the player's score in the database
#     cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
#     connection.commit()
#
#
# def close_database(connection, cursor):
#     # Close the cursor and connection
#     cursor.close()
#     connection.close()
#
#
# def main():
#     # Initialize the database
#     connection, cursor = initialize_database()
#
#     global screen, start_screen_image, track_image, car_image, enemy_car_image
#
#     # Initialize Pygame
#     pygame.init()
#
#     # Set screen size
#     screen = pygame.display.set_mode((1000, 800))
#
#     # fill white
#     screen.fill((255, 255, 255))
#
#     # Load images
#     start_screen_image = pygame.image.load('start_screen.png')
#     track_image = pygame.image.load('track.png')
#     car_image = pygame.image.load('car.png')
#     enemy_car_image = pygame.image.load('enemy_car.png')
#
#     global player
#     player = Player(300, 600, 60, 120, 5, 0, False, False)
#
#     global enemy_car
#     enemy_car_width = 90
#     enemy_car_height = 220
#     enemy_car_x = random.randint(-80, 400 - enemy_car_width)
#     enemy_car_y = -600
#     enemy_car_speed = 10
#     enemy_car = EnemyCar(enemy_car_x, enemy_car_y, enemy_car_width, enemy_car_height, enemy_car_speed)
#
#     global track
#     track_y = 0
#     track_speed = 20
#     track = Track(track_y, track_speed)
#
#     # Load font
#     font = pygame.font.Font(None, 36)
#
#     # Create clock object to control frame rate
#     clock = pygame.time.Clock()
#
#     # Display start screen
#     screen.blit(start_screen_image, (0, 0))
#     pygame.display.update()
#
#     # Check for input
#     restart()
#
#     # Game Loop
#     while True:
#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_LEFT:
#                     player.move('left')
#                 if event.key == pygame.K_RIGHT:
#                     player.move('right')
#                 if event.key == pygame.K_x:
#                     pygame.quit()
#                     exit()
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#                     player.move('none')
#
#         if not player.game_over:
#             if not player.game_over:
#                 # Increment score by one each time the game loop runs
#                 player.score += 1
#
#                 # Update the player's score in the database
#                 update_score(connection, cursor, player.score)
#
#             # multi
#             while (player.holding_state):
#                 player.speed = 0
#                 track.speed = 0
#                 enemy_car.speed = 0
#
#                 # Draw track
#                 track.draw()
#
#                 # Draw car
#                 player.draw()
#
#                 # Draw enemy car
#                 enemy_car.draw()
#
#                 # Draw score
#                 score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
#                 screen.blit(score_text, (5, 5))
#
#                 # Update display
#                 pygame.display.update()
#
#                 # Limit frame rate to 60 FPS.
#                 clock.tick(60)
#
#                 # Waiting for others
#                 game_over_text = font.render("Waiting fo' dem playerz bud", True, (255, 0, 0))
#                 screen.blit(game_over_text, (150, 400))
#                 pygame.display.update()
#
#             # Update car position
#             player.x += player.speed
#
#             # Prevent car from going off-screen
#             if player.x < -80:
#                 player.x = -80
#             if player.x > 490 - player.width:
#                 player.x = 490 - player.width
#
#             # Update enemy car position
#             enemy_car.y += enemy_car.speed
#
#             # Check for collision with enemy car
#             if enemy_car.y > 800:
#                 enemy_car.y = -600
#                 enemy_car.x = random.randint(0, 600 - enemy_car.width)
#
#             # Define car bounding rectangle
#             car_rect = pygame.Rect(player.x, player.y, player.width, player.height)
#
#             # Define enemy car bounding rectangle
#             enemy_car_rect = pygame.Rect(enemy_car.x, enemy_car.y, enemy_car.width, enemy_car.height)
#
#             # Check for collision between car and enemy car
#             if car_rect.colliderect(enemy_car_rect):
#                 player.game_over = True
#
#             # Update track position
#             track.y += track.speed
#
#             # Reset track position
#             if track.y > 0:
#                 track.y = -800
#
#             # Draw track
#             track.draw()
#
#             # Draw car
#             player.draw()
#
#             # Draw enemy car
#             enemy_car.draw()
#
#             # Draw score
#             score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
#             screen.blit(score_text, (5, 5))
#
#             # Increment score by one each time the game loop runs.
#             player.score += 1
#
#         else:
#             game_over_text = font.render("Game Over", True, (255, 0, 0))
#             screen.blit(game_over_text, (250, 400))
#             pygame.display.update()
#
#             # Pause for 2 seconds.
#             time.sleep(2)
#
#             # Reset game state and return to start screen.
#             player.x = 300
#             player.y = 600
#             enemy_car.x = random.randint(0, 600 - enemy_car.width)
#             enemy_car.y = -600
#             player.score = 0
#             player.game_over = False
#
#             # Display start screen
#             screen.blit(start_screen_image, (0, 0))
#             pygame.display.update()
#
#             # Close the database connection and cursor
#             close_database(connection, cursor)
#
#             # Check for input again
#             restart()
#
#         # Update display
#         pygame.display.update()
#
#         # Limit frame rate to 60 FPS.
#         clock.tick(60)
#
#
# if __name__ == '__main__':
#     main()
#
#
#
#



import pygame
import random
import time

class Player:
    def __init__(self, x, y, width, height, speed, score, game_over, holding_state):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.score = score
        self.game_over = game_over
        self.holding_state = holding_state

    def move(self, direction):
        if direction == 'left':
            player.speed = -5
        elif direction == 'right':
            player.speed = 5
        elif direction == 'none':
            player.speed = 0

    def draw(self):
        screen.blit(car_image, (player.x, player.y))

class EnemyCar:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self):
        screen.blit(enemy_car_image, (self.x, self.y))

class Track:
    def __init__(self, y, speed):
        self.y = y
        self.speed = speed

    def draw(self):
        screen.blit(track_image, (0, self.y))
        screen.blit(track_image, (0, self.y + 800))

def restart():
    # Wait for user to press 's' key
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    # Start game
                    player.game_over = False
                    break
                elif event.key == pygame.K_q:
                    # Quit game
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_m:
                    # Start the game session and connect to the server
                    player.holding_state = True
                    player.game_over = False
                    break
        else:
            continue
        break

def main():
    global screen, start_screen_image, track_image, car_image, enemy_car_image

    # Initialize Pygame
    pygame.init()

    # Set screen size
    screen = pygame.display.set_mode((1000, 800))

    # fill white
    screen.fill((255, 255, 255))

    # Load images
    start_screen_image = pygame.image.load('start_screen.png')
    track_image = pygame.image.load('track.png')
    car_image = pygame.image.load('car.png')
    enemy_car_image = pygame.image.load('enemy_car.png')

    global player
    player = Player(300, 600, 60, 120, 5, 0, False, False)

    global enemy_car
    enemy_car_width = 90
    enemy_car_height = 220
    enemy_car_x = random.randint(-80, 400 - enemy_car_width)
    enemy_car_y = -600
    enemy_car_speed = 10
    enemy_car = EnemyCar(enemy_car_x, enemy_car_y, enemy_car_width, enemy_car_height, enemy_car_speed)

    global track
    track_y = 0
    track_speed = 20
    track = Track(track_y, track_speed)

    # Load font
    font = pygame.font.Font(None, 36)

    # Create clock object to control frame rate
    clock = pygame.time.Clock()

    # Display start screen
    screen.blit(start_screen_image, (0, 0))
    pygame.display.update()

    # Check for input
    restart()

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
                if event.key == pygame.K_RIGHT:
                    player.move('right')
                if event.key == pygame.K_x:
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.move('none')

        if not player.game_over:
            # multi
            while (player.holding_state):
                player.speed = 0
                track.speed = 0
                enemy_car.speed = 0

                # Draw track
                track.draw()

                # Draw car
                player.draw()

                # Draw enemy car
                enemy_car.draw()

                # Draw score
                score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
                screen.blit(score_text, (5, 5))

                # Update display
                pygame.display.update()

                # Limit frame rate to 60 FPS.
                clock.tick(60)

                # Waiting for others
                game_over_text = font.render("Waiting fo' dem playerz bud", True, (255, 0, 0))
                screen.blit(game_over_text, (150, 400))
                pygame.display.update()

            # Update car position
            player.x += player.speed

            # Prevent car from going off-screen
            if player.x < -80:
                player.x = -80
            if player.x > 490 - player.width:
                player.x = 490 - player.width

            # Update enemy car position
            enemy_car.y += enemy_car.speed

            # Check for collision with enemy car
            if enemy_car.y > 800:
                enemy_car.y = -600
                enemy_car.x = random.randint(0, 600 - enemy_car.width)

            # Define car bounding rectangle
            car_rect = pygame.Rect(player.x, player.y, player.width, player.height)

            # Define enemy car bounding rectangle
            enemy_car_rect = pygame.Rect(enemy_car.x, enemy_car.y, enemy_car.width, enemy_car.height)

            # Check for collision between car and enemy car
            if car_rect.colliderect(enemy_car_rect):
                player.game_over = True

            # Update track position
            track.y += track.speed

            # Reset track position
            if track.y > 0:
                track.y = -800

            # Draw track
            track.draw()

            # Draw car
            player.draw()

            # Draw enemy car
            enemy_car.draw()

            # Draw score
            score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
            screen.blit(score_text, (5, 5))

            # Increment score by one each time the game loop runs.
            player.score += 1

        else:
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (250, 400))
            pygame.display.update()

            # Pause for 2 seconds.
            time.sleep(2)

            # Reset game state and return to start screen.
            player.x = 300
            player.y = 600
            enemy_car.x = random.randint(0, 600 - enemy_car.width)
            enemy_car.y = -600
            player.score = 0
            player.game_over = False

            # Display start screen
            screen.blit(start_screen_image, (0, 0))
            pygame.display.update()

            # Check for input again
            restart()

        # Update display
        pygame.display.update()

        # Limit frame rate to 60 FPS.
        clock.tick(60)


if __name__=='__main__':
    main()