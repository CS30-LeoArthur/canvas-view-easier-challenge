import pygame

# Define Colors
GREY = (128, 128, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GROUND_HEIGHT = SCREEN_HEIGHT - 200
platform_list = []
    
def rectCollide(rect1, rect2):
    return rect1.x < rect2.x + rect2.width and rect1.y < rect2.y + rect2.height and rect1.x + rect1.width > rect2.x and rect1.y + rect1.height > rect2.y

def check_collision(object1, object2):
    for i in range(len(object1)):
        if rectCollide(object1[i], object2):
            return i
    return -1

class Player():
    def __init__(self, x, y, width, height, change_x, change_y, jump_count):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.change_x = change_x
        self.change_y = change_y
        self.jump_count = jump_count
    
    def jump(self):
        if self.jump_count > 0:
            self.change_y = -7
            self.jump_count = 0

    def go_left(self):
        self.change_x = -3
    
    def go_right(self):
        self.change_x = 3

    def hzstop(self):
        self.change_x = 0
    
    def vt_default(self):
        self.change_y = 0.1

    def update(self):
        self.change_y = min(5, self.change_y + 0.2)
        self.x = self.x + self.change_x
        self.y = self.y + self.change_y
        
        platform_index = check_collision(platform_list, self)
        if platform_index != -1:
            self.vt_default()
            self.jump_count += 1
            if self.change_y > 0:
                self.y = platform_list[platform_index].y - self.height
            elif self.change_y < 0:
                self.y = platform_list[platform_index].y - self.height

    
    def draw_player(self, screen):
        pygame.draw.rect(screen, RED, [self.x, self.y, self.width, self.height])

class Platform():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw_platform(self, screen):
        pygame.draw.rect(screen, GREY, [self.x, self.y, self.width, self.height])

platform_list.append(Platform(0, GROUND_HEIGHT, SCREEN_WIDTH, 200))
platform_list.append(Platform(300, GROUND_HEIGHT - 100, 150, 20))
platform_list.append(Platform(500, GROUND_HEIGHT - 200, 150, 20))

def main():
    # Initialize pygame
    pygame.init()
    # Set screen
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    screen = pygame.display.set_mode(size)
    
    clock = pygame.time.Clock()
    # Variables
    frame_count = 0
    
    ground_height = SCREEN_HEIGHT - 200
    
    player_height = 20
    
    player = Player(100, ground_height - player_height, 20, player_height, 0, 0, 1)
    # create loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Player movement 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                elif event.key == pygame.K_d:
                    player.go_right()
                elif event.key == pygame.K_w:
                    player.jump()    
            # Stop player
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0 or event.key == pygame.K_d and player.change_x > 0:
                    player.hzstop()
        # Logic

        player.update()


        # Drawing
        screen.fill(WHITE)
        for i in range(len(platform_list)):
            platform_list[i].draw_platform(screen)
        player.draw_player(screen)

        pygame.display.flip()
        # frame rate
        frame_count += 1
        clock.tick(60)

    pygame.quit

if __name__ == "__main__":
    main()

