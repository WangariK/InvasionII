import pygame
import sys
import random


pygame.init()

width = 800
height = 600

pink = (250, 127, 80)
black = (0, 0, 0)
yellow = (255, 255, 0)
background_color = (139, 69, 19)

player_size = 50
player_pos = [width/2, height-2*player_size]

opponent_size = 50
opponent_pos = [random.randint(0, width-opponent_size), 0]
opponent_list = [opponent_pos]

speed = 10

screen = pygame.display.set_mode((width, height))

game_over = False

score = 0

clock = pygame.time.Clock()

font = pygame.font.SysFont("monospace", 35)


def set_level(score, speed):
    if score < 20:
        speed = 5
    elif score < 40:
        speed = 8
    elif score < 60:
        speed = 12
    else:
        speed = 15
    return speed


def opponents_drop(opponent_list):
    delay = random.random()
    if len(opponent_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, width-opponent_size)
        y_pos = 0
        opponent_list.append([x_pos, y_pos])


def create_opponents(opponent_list):
    for opponent_pos in opponent_list:
        pygame.draw.rect(screen, black, (opponent_pos[0],
                                         opponent_pos[1], opponent_size, opponent_size))


def update_opponent_positions(opponent_list, score):
    for position, opponent_pos in enumerate(opponent_list):
        if opponent_pos[1] >= 0 and opponent_pos[1] < height:
            opponent_pos[1] += speed
        else:
            opponent_list.pop(position)
            score += 1
    return score


def collision_check(opponent_list, player_pos):
    for opponent_pos in opponent_list:
        if detect_a_collision(opponent_pos, player_pos):
            return True
    return False


def detect_a_collision(player_pos, opponent_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = opponent_pos[0]
    e_y = opponent_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+opponent_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+opponent_size)):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x, y]

    screen.fill(background_color)

    opponents_drop(opponent_list)
    score = update_opponent_positions(opponent_list, score)
    speed = set_level(score, speed)

    text = "Score:" + str(score)
    label = font.render(text, 1, yellow)
    screen.blit(label, (width-200, height-40))

    if collision_check(opponent_list, player_pos):
        game_over = True
        break

    create_opponents(opponent_list)

    pygame.draw.rect(screen, pink, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update()
