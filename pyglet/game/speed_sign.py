from pyglet.shapes import Rectangle, Circle
from pyglet.graphics import Batch
from pyglet.text import Label


from .constants import *


class SpeedSign:
    def __init__(self, limit, position):
        self.batch = Batch()

        self.limit = limit
        self.position = position
        self.width = 80
        self.height = 80

    # def create_image(self):
    #     # Create the image only when needed
    #     self.image = pygame.Surface(self.size, pygame.SRCALPHA)
    #     pygame.draw.circle(
    #         self.image, (255, 255, 255), (40, 40), 40
    #     )  # White background
    #     pygame.draw.circle(self.image, (255, 0, 0), (40, 40), 40, 10)  # Red circle
    #     font = pygame.font.SysFont(None, 42)
    #     text = font.render(str(self.limit * 10), True, (0, 0, 0))
    #     text_rect = text.get_rect(center=(40, 40))
    #     self.image.blit(text, text_rect)

    def draw(self):
        speed_sign_rect = self.get_speed_sign_rect()
        red_outer_circle = self.get_red_outer_circle()
        white_inner_circle = self.get_white_inner_circle()
        limit_text = self.get_limit_text()
        # limit_text.draw()

        self.batch.draw()

    def get_speed_sign_rect(self):
        speed_sign_rect = Rectangle(
            x=self.position[0],
            y=self.position[1],
            width=self.width,
            height=self.height,
            batch=self.batch,
        )
        speed_sign_rect.visible = False

        return speed_sign_rect

    def get_white_inner_circle(self):
        white_inner_circle = Circle(
            x=self.position[0] + self.width / 2,
            y=self.position[1] + self.height / 2,
            radius=30,
            batch=self.batch,
        )

        return white_inner_circle

    def get_red_outer_circle(self):
        red_outer_circle = Circle(
            x=self.position[0] + self.width / 2,
            y=self.position[1] + self.height / 2,
            radius=40,
            color=(255, 0, 0),
            batch=self.batch,
        )

        return red_outer_circle

    def get_limit_text(self):
        limit_text = Label(
            text=str(self.limit * 10),
            # font_name="Times New Roman",
            # font_size=10,
            x=self.position[0],
            y=self.position[1],
            # anchor_x="center",
            # anchor_y="center",
        )

        return limit_text
