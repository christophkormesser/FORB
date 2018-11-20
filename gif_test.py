import sys

import pyglet
from pyglet.window import Platform

if len(sys.argv) > 1:
    animation = pyglet.image.load_animation(sys.argv[1])
    bin = pyglet.image.atlas.TextureBin()
    animation.add_to_texture_bin(bin)
else:
    animation = pyglet.resource.animation('cuteface.gif')
    sprite = pyglet.sprite.Sprite(animation)

screen = Platform().get_default_display().get_default_screen()
window = pyglet.window.Window(width=screen.width, height=screen.height)
window.set_fullscreen(True)

pyglet.gl.glClearColor(1, 1, 1, 1)

@window.event
def on_draw():
    window.clear()
    sprite.draw()

pyglet.app.run()