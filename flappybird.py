from ursina import *
import random

gravity = 9 # الجاذبية
flap_velocity = 4.2
velocity = 0
offset = 0
run = True
num = 5 # عدد ال pipes
pipe_speed = 3 # سرعة تحرك ال pipes
class Pipe(Entity):
    def __init__(self, x, y, img, flipped=False):
        super().__init__()

        self.model = "quad"
        self.scale = (1, 7)
        self.position = (x, y, 0)
        self.texture = img
        self.color = color.white
        self.collider = "box"

        if flipped:
            self.rotation_z = 180

def update():
    global velocity, offset, run, pipe_pairs, pipe_speed
    # دي علشان تحريك الطائر
    if run:
        velocity -= gravity * time.dt
        bird.y += velocity * time.dt
    # علشان ال pipes و الOffset
    if run:
        offset += time.dt * 0.2
        bg.texture_offset = (offset, 0)
        for bottom, top in pipe_pairs:
            bottom.x -= pipe_speed * time.dt
            top.x -= pipe_speed * time.dt
            if bottom.x < -12:
                new_x = max(pair[0].x for pair in pipe_pairs) + 4
                gap_center = random.randint(-1, 2)
                bottom.x = top.x = new_x
                bottom.y = gap_center - 5
                top.y = gap_center + 5
            if bird.intersects(bottom).hit or bird.intersects(top).hit:
                run = False
                die_sound.play()
                bird.pause()
                Sprite(
                    "assets/sprites/gameover.png",
                    scale=(4,4),
                    z=-1
                )
def input(key):
    global velocity
    if run and key == "space":
        jump_sound.play()
        velocity = flap_velocity

app = Ursina()
jump_sound = Audio("assets/audio/point.wav",autoplay=False)
die_sound = Audio("assets/audio/die.wav",autoplay=False)
bg = Entity(
    model="quad",
    scale=(20, 10),
    texture="assets/sprites/bg.png",
    z=1
)

bird = Animation(
    "assets/sprites/bird/yellowbird",
    fps=8,
    collider="box",
    scale=(1.0,0.7),
    y=1.5
)

pipe_pairs = []

for i in range(num):
    pipe_x = 6 + i * 4
    gap_center = random.randint(-1,2)
    img = "assets/sprites/pipe-green.png"
    bottom = Pipe(
        pipe_x,
        gap_center - 5,
        img
    )
    top = Pipe(
        pipe_x,
        gap_center + 5,
        img,
        flipped=True
    )
    pipe_pairs.append((bottom, top))

app.run()