import pygame
from network import Network

pygame.init()
width = 1000
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Track:
    def __init__(self, y, speed):
        self.y = y
        self.speed = speed

    def draw(self):
        win.blit(track_image, (0, self.y))
        win.blit(track_image, (0, self.y + 800))


class Player():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vel = 3

    def draw(self, win):
        win.blit(self.image,self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        self.update()


    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

def read_pos(str):
    str=str.split(",")
    return int(str[0]),int(str[1])

def make_pos(tup):
    return str(tup[0])+","+str(tup[1])


def redrawWindow(win,player,player2):
    win.fill((255,255,255))
    win.blit(track_image,(0,0))
    track.draw()
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():

    global screen, start_screen_image, track_image, car_image, enemy_car_image


    # Load images
    start_screen_image = pygame.image.load('start_screen.png')
    track_image = pygame.image.load('track.png')
    car_image = pygame.image.load('car.png')
    enemy_car_image = pygame.image.load('enemy_car.png')




    run = True
    n=Network()
    startPos=read_pos(n.getPos())
    p = Player(startPos[0],startPos[1],100,100,car_image)
    p2=Player(0,0,100,100,car_image)
    clock = pygame.time.Clock()

    #track
    global track
    track_y = 0
    track_speed = 20
    track = Track(track_y, track_speed)

    while run:


        clock.tick(60)

        p2Pos=read_pos(n.send(make_pos((p.x,p.y))))
        p2.x=p2Pos[0]
        p2.y=p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



        track.y += track.speed
        if track.y > 0:
            track.y = -800
        p.move()
        redrawWindow(win, p,p2)

main()