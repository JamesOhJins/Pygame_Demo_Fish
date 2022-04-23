import pygame
import random
pygame.init()

size = [900,600]
screen = pygame.display.set_mode(size)

title = 'Raise rashi'
pygame.display.set_caption(title)

face_left = True
#settings
clock = pygame.time.Clock()

color = (0,0,0)
class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
    def put_img(self, url):
        if url[-3:] == 'png':
            self.img = pygame.image.load(url).convert_alpha()
        else:
            self.img = pygame.image.load(url)
    def rescale(self,width,height):
        self.img = pygame.transform.scale(self.img, (width,height))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img, (self.x,self.y))
    def face(self):
        self.img = pygame.transform.flip(self.img, True,False)
    def render(self):
        self.y = random.randint(0,size[1])
        fish_dir = random.randint(0,1)
        self.show()
        if fish_dir == 0:
            self.x = 0
            self.face()
            self.move = random.randint(3,7)      
        else:
            self.x = size[1]
            self.move = random.randint(3,7)
            self.move = self.move * -1
        self.x += self.move
rashi = obj()
rashi.put_img("Data/rashi.jpg")
rashi.rescale(60,60)

fish = obj()
fish.put_img("Data/fish.jpg")
fish.rescale(90,60)

f1 = obj()
f1.put_img("Data/F1.jpeg")
f1.rescale(150,150)

f2 = obj()
f2.put_img("Data/F2.jpeg")
f2.rescale(60,40)

shark = obj()
shark.put_img("Data/shark.jpg")
shark.rescale(250,100)

rashi.x = size[0]//2 - (rashi.sx//2)
rashi.y = size[1] - (rashi.sy//2) - 450
rashi.move = 5
flag = True
move_left, move_right, move_up, move_down = False,False,False,False


SB = 0
count = 0
while SB == 0:
    clock.tick(60) #FPS
    count+= 1
    if count == 120:
        count = 0
        new_fish = random.randint(0,3)   
        if new_fish == 0:
            fish.render()
            print("case1")
        elif new_fish == 1:
            f1.render()
            print("case2")
        elif new_fish == 2:
            f2.render()
            print("case3")
        elif new_fish == 3:
            shark.render()
            print("case4")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
                if face_left:
                    rashi.face()
                face_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = True
                if not face_left:
                    rashi.face()
                face_left = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False
    screen.fill(color)
    rashi.show()
    pygame.display.flip()
    if move_left == True:
        rashi.x -= rashi.move
        if rashi.x <= 0:
            rashi.x = 0
    elif move_right == True:
        rashi.x += rashi.move
        if rashi.x >= size[0] - 80:
            rashi.x = size[0] - 80
    if move_up == True:
        rashi.y -= rashi.move
        if rashi.y <= 0:
            rashi.y = 0
    elif move_down == True:
        rashi.y += rashi.move
        if rashi.y >= size[1]-rashi.sy:
            rashi.y = size[1] -rashi.sy
pygame.quit