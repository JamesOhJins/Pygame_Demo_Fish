import pygame
import random
pygame.init()

size = [1400,800]
screen = pygame.display.set_mode(size)

title = 'Raise rashi'
pygame.display.set_caption(title)

face_left = True
#settings
clock = pygame.time.Clock()


color = (0,0,30)
class obj:
    def __init__(self):
        self.x = -300
        self.y = -300
        self.facing_Left = False
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
        self.y = random.randint(0,size[1]-self.sy)
        fish_dir = random.randint(0,1)
        if fish_dir == 0:
            self.x = 0 - self.sx
            if self.facing_Left:
                self.face()
            self.move = random.randint(2,5)      
            self.facing_Left = False
        else:
            self.x = size[0]+self.sx
            if not self.facing_Left:
                self.face()
            self.move = random.randint(2,5)
            self.move = self.move * -1
            self.facing_left = True
    
def consume(a,b):
    if a.x-(b.sx*0.85) <= b.x and b.x <= a.x + (0.85*a.sx):
        if a.y-(0.6*b.sy) <= b.y and b.y <= a.y + (0.6*a.sy):
            if a.sx * a.sy > b.sx *b.sy:
                return False
            else:
                return True
    return False

rashi = obj()
rashi.put_img("Data/rashi.png")
rashi.rescale(60,60)

rashi.x = size[0]//2 - (rashi.sx//2)
rashi.y = size[1] - (rashi.sy//2) - 450
rashi.move = 4
flag = True
move_left, move_right, move_up, move_down = False,False,False,False


run = True
count = 0
fish_list = []
d_list = []
score = 0
gameover = False
pausetimerevent = pygame.USEREVENT + 1
paused = False
game_font = pygame.font.Font("font.ttf", 30)
game_over = pygame.font.Font("font.ttf", 80)
while run:
    clock.tick(80) #FPS
    if not paused:
        count+= 1
    if count == 60:
        count = 0
        new_fish = random.randint(rashi.sx//20,30+rashi.sx//2)   
        if new_fish < 35:
            f2 = obj()
            f2.put_img("Data/F2.png")
            f2.rescale(60,40)
            f2.render()
            fish_list.append(f2)
        elif new_fish < 50:
            f3 = obj()
            f3.put_img("Data/F3.png")
            f3.rescale(85,65)
            f3.render()
            fish_list.append(f3)
        elif new_fish < 70:
            n_fish = obj()
            n_fish.put_img("Data/fish.png")
            n_fish.rescale(130,95)
            n_fish.render()
            fish_list.append(n_fish)
        elif new_fish < 95:
            f1 = obj()
            f1.put_img("Data/F1.png")
            f1.rescale(150,150)
            f1.render()
            fish_list.append(f1)
        else:
            shark = obj()
            shark.put_img("Data/shark.png")
            shark.rescale(350,180)
            shark.render()
            fish_list.append(shark)
        
    for i in fish_list:
        fish = i
        fish.x += fish.move
        if fish.x <= -500 or fish.x >= size[0] + 500:
            d_list.append(i)
    for d in d_list:
        if d in fish_list:
            fish_list.remove(d)
        d_list.remove(d)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if paused:
                rashi.rescale(60,60)
                score = 0
                gameover = False
                paused = False
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
    for fish in fish_list:
        if consume(fish,rashi):
            score += ((fish.sx+fish.sy)/10)**2
            if face_left:
                rashi.put_img("Data/rashi.png")
            else:
                rashi.put_img("Data/rashi.png")
                rashi.face()
            rashi.rescale(rashi.sx + (fish.sx+fish.sy)/70 + 1, rashi.sy + (fish.sx+fish.sy)/70 + 1)
            if fish in fish_list:
                fish_list.remove(fish)
        if consume(rashi,fish):
            gameover = True
            paused = True
            fish_list = []
            d_list = []
            count = 0
            
    screen.fill(color)
    bg = pygame.image.load("Data/bg.jpg")
    screen.blit(bg,(0,0))
    rashi.show()
    for fish in fish_list:
        fish.show()
    text = game_font.render("Score: {}".format(int(score)),True,(255,255,255))
    screen.blit(text,(size[0]//2 - 60, 5))
    if gameover:
        game = game_over.render("Game over",True,(255,0,0))
        screen.blit(game,(size[0]//2 - 200, size[1]//2 - 100))

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