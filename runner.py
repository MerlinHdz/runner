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

sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()
ground_y = 300

# Snail
snail_index = 0
snail_surf1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_surf2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snails = [snail_surf1, snail_surf2]
snail_surf = snails[snail_index]

# Fly
fly_index = 0
fly_surf1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_surf2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
flies = [fly_surf1, fly_surf2]
fly_surf = flies[fly_index]

obstacle_rect_list = []

# Player
player_index = 0
player_surf1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_surf2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
players = [player_surf1, player_surf2]
player_jump_surf = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_surf = players[player_index]

player_rect = player_surf.get_rect(midbottom=(80, ground_y))

player_end_surf = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_end_surf = pygame.transform.rotozoom(player_end_surf, 0, 2)
player_end_rect = player_end_surf.get_rect(center=(WIDTH/2,HEIGHT/2))

score = 0
score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
score_rect = score_surf.get_rect(center=(WIDTH/2, 40))

game_instructions = test_font.render("Press Enter to start game", False, (64,64,64))
game_instructions_rect = game_instructions.get_rect(center=(WIDTH/2, HEIGHT - 50))

snail_vel = 4
player_g = 0

game_active = False


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= snail_vel

            if obstacle_rect.bottom == ground_y:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    # The return value of this function will determine if game is active or not
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False

    return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < ground_y:
        player_surf = player_jump_surf
    else:
        player_index += 0.1
        if player_index >= len(players): player_index = 0

        player_surf = players[int(player_index)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if player_rect.collidepoint(event.pos):
                    player_g = -25

            if event.type == pygame.KEYDOWN and player_rect.bottom == 300:
                if event.key == pygame.K_SPACE:
                    player_g = -20

            
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf1.get_rect(bottomleft=(WIDTH, ground_y)))
                else:
                    obstacle_rect_list.append(fly_surf1.get_rect(bottomleft=(WIDTH, 150)))

            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snails[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surf = flies[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                obstacle_rect_list.clear()
                player_rect.bottom = ground_y
                score = 0
                score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
                game_active = True


    if game_active:
        # blit stands for block image transfer. the .blit() method takes a surface and position
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, ground_y))
        screen.blit(score_surf, score_rect)

        # Player
        player_g += 1
        player_rect.bottom += player_g

        player_animation()

        if player_rect.bottom >= ground_y:
            player_rect.bottom = ground_y
        
        screen.blit(player_surf, player_rect)

        obstacle_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_end_surf, player_end_rect)

        if score > 0:
            screen.blit(score_surf, score_rect)
            
        screen.blit(game_instructions, game_instructions_rect)
    

    pygame.display.update()
    clock.tick(FPS)
    