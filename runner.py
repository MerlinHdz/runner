import pygame
from sys import exit 
from random import randint

# pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)


sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_y = 300

# Obstacles
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
# snail_rect = snail_surface.get_rect(bottomleft=(WIDTH - 100, ground_y))

obstacle_rect_list = []


# Player
player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, ground_y))

player_end_surface = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_end_surface = pygame.transform.rotozoom(player_end_surface, 0, 2)
player_end_rect = player_end_surface.get_rect(center=(WIDTH/2,HEIGHT/2))

score = 0
score_surface = test_font.render(f'Score: {score}', False, (64, 64, 64))
score_rect = score_surface.get_rect(center=(WIDTH/2, 40))

game_instructions = test_font.render("Press Enter to start game", False, (64,64,64))
game_instructions_rect = game_instructions.get_rect(center=(WIDTH/2, HEIGHT - 50))

snail_vel = 4
player_g = 0

game_active = False


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= snail_vel
            screen.blit(snail_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if player_rect.collidepoint(event.pos):
                    player_g = -20

            if event.type == pygame.KEYDOWN and player_rect.bottom == 300:
                if event.key == pygame.K_SPACE:
                    player_g = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # snail_rect.left = WIDTH
                player_rect.bottom = ground_y
                score = 0
                score_surface = test_font.render(f'Score: {score}', False, (64, 64, 64))
                game_active = True

        if event.type == obstacle_timer and game_active:
            ran_x = randint(900, 1100)
            obstacle_rect_list.append(snail_surface.get_rect(bottomleft=(ran_x, ground_y)))
            

    if game_active:
        # blit stands for block image transfer. the .blit() method takes a surface and position
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, ground_y))
        screen.blit(score_surface, score_rect)

        # Snail
        # snail_rect.right -= snail_vel

        # if snail_rect.right <= 0:
        #     score += 1
        #     score_surface = test_font.render(f'Score: {score}', False, (64, 64, 64))

        #     snail_rect.right = WIDTH - 50

        # screen.blit(snail_surface, snail_rect)

        # Player
        player_g += 1
        player_rect.bottom += player_g

        if player_rect.bottom >= ground_y:
            player_rect.bottom = ground_y
        
        screen.blit(player_surface, player_rect)

        # Obstacle Movement
        obstacle_list = obstacle_movement(obstacle_rect_list)

        # Collision
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
    else:
        screen.fill((94,129,162))
        screen.blit(player_end_surface, player_end_rect)

        if score > 0:
            screen.blit(score_surface, score_rect)
            
        screen.blit(game_instructions, game_instructions_rect)
    

    pygame.display.update()
    clock.tick(FPS)
    