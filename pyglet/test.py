import pyglet

window = pyglet.window.Window()

# Create a text label
label = pyglet.text.Label(
    "Hello, world!",
    font_name="Arial",
    font_size=36,
    x=window.width // 2,
    y=window.height // 2,
    anchor_x="center",
    anchor_y="center",
)


@window.event
def on_draw():
    window.clear()
    label.draw()


pyglet.app.run()
