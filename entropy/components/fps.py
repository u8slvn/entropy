import pygame


class FPS:

    def __init__(self, value: float) -> None:
        self.value = value
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 12)
        self.fmt = "{fps} FPS"

    def tick(self) -> None:
        self.clock.tick(self.value)

    @property
    def text(self):
        return self.font.render(self.get_current_fps(), True, (255, 255, 255))

    def get_current_fps(self) -> str:
        return self.fmt.format(fps=round(self.clock.get_fps()))

    def render(self, display):
        display.blit(self.text, (200,150))
