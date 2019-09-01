from pygamemadeeasy import *
from random import randint
import time

game = PygameMadeEasy(288, 512)

player_x = 50                           # beginning x-value for player
jump_from_y = 250                       # beginning y-value for player
pipe_gap_top = randint(50,320)          # y-value for the top of the gap of the first pair of pipes
pipe_gap_height = randint(100,200)      # y-value for the size of the gap of the first pair of pipes
pipe_x = 288                            # x-value for the first pair of pipes
pipe_speed = 7                           # x-value speed per frame the pipes will move
jump_started_at = 0                     # time code (in seconds) that the most recent jump started
previous_y = 0                          # y-value the player was at in the most recently previous frame
score = 0                               # player score
point_claimed = False                   # has the point for the current pipe been claimed yet?
alive = True

def click(mousex, mousey):
    global pipe_gap_height, pipe_gap_top
    pipe_gap_height = randint(100,200)
    pipe_gap_top = randint(50,350)

def preview(ui, window):
    game.image(0, 0, "media/background.png")      # background.png is 288 x 512
    game.image(0, 450, "media/base.png")          # base.png is 336 x 112
    game.set_stroke(colors.black)
    game.text(20, 150, "Flappy Bird!", size=36)
    game.text(20, 200, "Press [SPACE] to start", size=18)
    game.image_piskel_animation(50, 250, "media/flappybird-animation.png", 34, 24, rotate=30)       # 32x72 pixels, 3 frames
    if ui.space:
        return False

def calculate_jump_effect( jump_started_at ):
    """ This calculation is done using a quadratic equation (you'll learn about it in math in a couple of years). I used it to make the jump and fall effect "smoother". Don't stress about the math """
    x = float(time.time() - jump_started_at )
    y = -350*(x**2) + 350*x
    y = int(y)
    return y

def keydown(key):
    global jump_from_y, jump_started_at, alive
    if key == " " and alive:
        jump_from_y = jump_from_y - calculate_jump_effect( jump_started_at )
        jump_started_at = time.time()
        game.sound("media/wing.wav")

def main(ui, window):
    global player_x, jump_from_y, previous_y, score, alive
    global pipe_gap_height, pipe_gap_top, pipe_x, point_claimed
    
    # background
    game.image(0,0,"media/background.png")      # background.png is 288 x 512
    game.image(0,450,"media/base.png")          # base.png is 336 x 112
    
    # pipes
    pipe_x = pipe_x - pipe_speed                                        # move the pipe for this frame
    box1 = game.image(pipe_x,pipe_gap_top-320,"media/pipe.png", rotate=180)    # top pipe
    box2 = game.image(pipe_x,pipe_gap_top+pipe_gap_height,"media/pipe.png")    # bottom pipe
    if pipe_x < (player_x - 52) and not point_claimed:                  # player has cleared the pipe
        score = score + 1
        game.sound("media/point.wav")
        point_claimed = True
    if pipe_x < -50:                            # pipe has disappeared off screen, move it back to the otherside to reappear
        pipe_x = 288+randint(0,200)
        pipe_gap_height = randint(100,200)
        pipe_gap_top = randint(50,300)
        point_claimed = False                   # "new" pipe so new point to be claimed
    
    # player
    draw_y = jump_from_y - calculate_jump_effect(jump_started_at)
    if draw_y < previous_y:
        angle = 30
    else:
        angle = -30
    players_box = game.image_piskel_animation(player_x,draw_y,"media/flappybird-animation.png",34,24, rotate=angle)       # 32x72 pixels, 3 frames
    previous_y = draw_y

    # check for collision with pipe
    if alive:
        if game.is_collision(players_box, box1) or game.is_collision(players_box, box2):
            alive = False
            game.sound("media/hit.wav")
            game.sound("media/die.wav")

    # check if we fell to the ground
    if draw_y >= 450:
        return False

def gameover(ui, window):
    global score
    game.image(0, 0, "media/background.png")      # background.png is 288 x 512
    game.image(0, 450, "media/base.png")          # base.png is 336 x 112
    game.text(20, 150, "Game over!", size=36)
    game.text(20, 200, "Your score:", size=18)
    game.text(20, 250, str(score), size=72)
    game.text(20, 400, "Press [ESC] to quit", size=18)

game.play(preview)
jump_started_at = time.time()
game.play(main, keydown=keydown)
game.play(gameover)
