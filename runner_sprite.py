import pygame
from sys import exit 
from random import randint, choice 

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(loops=-1)

sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()
ground_y = 300


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_surf1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_surf2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()

        self.player_walk = [player_surf1, player_surf2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, ground_y))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            
            self.image = self.player_walk[int(self.player_index)]
            

    def update(self):
        self.player_input()
        self.apply_gravity()    
        self.animation_state()



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = ground_y

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))


    def animation_state(self):
         self.animation_index += 0.1
         if self.animation_index > len(self.frames):
            self.animation_index = 0
        
         self.image = self.frames[int(self.animation_index)]


    def destroy(self):
        if self.rect.x <= 100:
             self.kill

    
    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()



def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
 

# Score
score = 0
score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
score_rect = score_surf.get_rect(center=(WIDTH/2, 40))

# Game over stuff
player_end_surf = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_end_surf = pygame.transform.rotozoom(player_end_surf, 0, 2)
player_end_rect = player_end_surf.get_rect(center=(WIDTH/2,HEIGHT/2))

game_instructions = test_font.render("Press Enter to start game", False, (64,64,64))
game_instructions_rect = game_instructions.get_rect(center=(WIDTH/2, HEIGHT - 50))

# Game Active variable
game_active = False


# Timers
score_timer = pygame.USEREVENT + 1
pygame.time.set_timer(score_timer, 1000)

obstacle_timer = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_timer, 1500)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == score_timer:
                score += 1
                score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
            
            if event.type == obstacle_timer:
                # Add an obstacle to our group - randomize it, but get more snails than flies
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail"])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                score = 0
                score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
                # Get rid of obstacles, send player to original position
                game_active = True


    if game_active:
        # blit stands for block image transfer. the .blit() method takes a surface and position
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, ground_y))

        # Update and display score
        screen.blit(score_surf, score_rect)

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()
 
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_end_surf, player_end_rect)

        if score > 0:
            screen.blit(score_surf, score_rect)
            
        screen.blit(game_instructions, game_instructions_rect)
    

    pygame.display.update()
    clock.tick(FPS)
    