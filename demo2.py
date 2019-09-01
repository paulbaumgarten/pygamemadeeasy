import pygame, time, random
from pygame.locals import *
from pygamemadeeasy import *
from random import randint
import time

""" Custom functions """

def calculate_jump_effect( jump_started_at ):
    """ 
    This calculation is done using a quadratic equation (you'll learn about it in math in a couple of years). 
    I used it to make the jump and fall effect "smoother". Don't stress about the math 
    """
    x = float( time.time() - jump_started_at )      # x = number of seconds since jump started
    y = -350*(x**2) + 350*x                         # y = change in height to apply since jump started
    return int(y)

""" Initialise Pygame """

pygame.init()
window = pygame.display.set_mode((288,512))
fps = pygame.time.Clock()

# Images
background_image        = pygame.image.load("media/background.png").convert_alpha() # background.png is 288 x 512
base_image              = pygame.image.load("media/base.png").convert_alpha()       # base.png is 336 x 112
bottom_pipe_image       = pygame.image.load("media/pipe.png").convert_alpha()       # pipe.png is 52 x 320
top_pipe_image          = pygame.transform.rotate(bottom_pipe_image, 180)           # top pipe is a 180 degree rotation of bottom pipe
bird_animation          = SpriteAnimation("media/flappybird-animation.png", 32, 24) # each frame is 32 x 24

# Sounds
fly_sound               = pygame.mixer.Sound("media/wing.wav")
point_sound             = pygame.mixer.Sound("media/point.wav")
hit_sound               = pygame.mixer.Sound("media/hit.wav")
die_sound               = pygame.mixer.Sound("media/die.wav")

# Fonts
arial_24                = pygame.font.SysFont("Arial", 24)

# Game variables
player_x = 50                           # beginning x-value for player
jump_from_y = 250                       # beginning y-value for player
pipe_gap_top = randint(50,320)          # y-value for the top of the gap of the first pair of pipes
pipe_gap_height = randint(100,200)      # y-value for the size of the gap of the first pair of pipes
pipe_x = 288                            # x-value for the first pair of pipes
pipe_speed = 7                          # x-value speed per frame the pipes will move
jump_started_at = time.time()           # time code (in seconds) that the most recent jump started
previous_y = 0                          # y-value the player was at in the most recently previous frame
score = 0                               # player score
point_claimed = False                   # has the point for the current pipe been claimed yet?
lives = 3
quit = False

# Main game loop
while not quit:

    # Process events
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        elif event.type == KEYDOWN:
            k = keys.get_key_value(event.key)
            print(f"key pressed {k}")
            if event.key == K_ESCAPE:
                quit = True
            if event.key == K_SPACE:
                if lives > 0:
                    jump_from_y = jump_from_y - calculate_jump_effect( jump_started_at )
                    jump_started_at = time.time()
                    fly_sound.play()

    # draw background scene
    window.fill(colors.black)
    window.blit(background_image, (0, 0))
    window.blit(base_image, (0, 450))
    
    # move and draw the pipes
    pipe_x = pipe_x - pipe_speed                                                    # move the pipe for this frame
    window.blit(top_pipe_image,     ( pipe_x, pipe_gap_top - 320 ) )                # top pipe
    window.blit(bottom_pipe_image,  ( pipe_x, pipe_gap_top + pipe_gap_height ) )    # bottom pipe
    top_pipe_box = Rect( pipe_x, pipe_gap_top - 320, top_pipe_image.get_width(), top_pipe_image.get_height() )
    bottom_pipe_box = Rect( pipe_x, pipe_gap_top + pipe_gap_height, bottom_pipe_image.get_width(), bottom_pipe_image.get_height() )

    # if the player has cleared the pipes, and they haven't claimed the point yet
    if pipe_x < (player_x - 52) and not point_claimed:
        score = score + 1
        point_sound.play()
        point_claimed = True

    # if pipe has disappeared off screen, move it back to the otherside to reappear
    if pipe_x < -50:                            
        pipe_x = 288+randint(0,200)
        pipe_gap_height = randint(100,200)
        pipe_gap_top = randint(50,300)
        point_claimed = False                   # "new" pipe so new point to be claimed
    
    # move and draw the player
    draw_y = jump_from_y - calculate_jump_effect(jump_started_at)
    if draw_y < previous_y:
        angle = 30                              # if we are climbing, angle to face up
    else:
        angle = -30                             # if we are falling, angle to face down
    bird_frame = bird_animation.next_frame(rotate=angle)
    window.blit(bird_frame, (player_x, draw_y))
    bird_box = Rect(player_x, draw_y, 32, 24)
    previous_y = draw_y

    # check for collision with pipe
    if bird_box.colliderect(top_pipe_box) or bird_box.colliderect(bottom_pipe_box):
        if not point_claimed:
            lives = lives - 1
            hit_sound.play()
            point_claimed = True # stop us getting the point, and from losing multiple lives from the same pipe

    # check if we fell to the ground
    if draw_y >= 450:
        quit = True

    # Update screen
    window.blit( arial_24.render(f"Score {score}", 1, colors.black), (10, 10) )
    window.blit( arial_24.render(f"Lives {lives}", 1, colors.black), (200, 10) )
    pygame.display.update()
    fps.tick(25)

# Game over
die_sound.play()
time.sleep(1)   # let the sound effects finish ;-)
pygame.quit()
print(f"Game over! Your score was {score}")
