import pygame
from pygame import *
from player import *
from blocks import *

WIN_WIDTH = 800
WIN_HEIGHT = 840
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)
    t = max(-(camera.height-WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(0, t, 0, h)

class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color(BACKGROUND_COLOR)
        self.font_color = pygame.Color('orange')
        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)

def game():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Floor Is Lava")
    bg = Surface((WIN_WIDTH,WIN_HEIGHT))

    bg.fill(Color(BACKGROUND_COLOR))


    
    hero = Player(55,31500)
    left = right = False
    up = False
    
    entities = pygame.sprite.Group()
    platforms = []
    
    entities.add(hero)
    pf = Platform(55, 32100)
    entities.add(pf)
    platforms.append(pf)
           
    from level import level

    timer = pygame.time.Clock()
    x=y=0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            if col == '+':
                lv = Lava(x,y)
                entities.add(lv)
                platforms.append(lv)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    for i in range(800):
        lv = Lava(i, 32000)
        entities.add(lv)
        platforms.append(lv)
    total_level_width  = len(level[0])*PLATFORM_WIDTH
    total_level_height = len(level)*PLATFORM_HEIGHT
    
    camera = Camera(camera_configure, total_level_width, total_level_height)

    pygame.time.set_timer(USEREVENT, 500)

    lvlup = 0

    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_w:
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_w:
                up = False
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False
            if e.type == USEREVENT:
                lvlup += 15
                xcor = 0
                for i in range(25):
                    lv = Lava(xcor, 32000-lvlup)
                    entities.add(lv)
                    platforms.append(lv)
                    xcor += 32
                if hero.rect.bottom >= 32000-lvlup:
                    raise SystemExit

        screen.blit(bg, (0,0))

        camera.update(hero)
        hero.update(left, right, up,platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        
        
        pygame.display.update()
        

if __name__ == "__main__":
    game()
