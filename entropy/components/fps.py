import pygame

from entropy.colors import WHITE, BLACK


class FPS:

    def __init__(self, value: float) -> None:
        self.value = value
        self.font = pygame.font.SysFont("Verdana", 12)
        self.clock = pygame.time.Clock()
        self.visible = False
        self.format = "{fps} FPS"
        self.text = self._build_text()

    def _build_text(self) -> pygame.Surface:
        fps = self.format.format(fps=round(self.clock.get_fps()))
        return self.font.render(fps, True, WHITE, BLACK)

    def toggle(self, key: int) -> None:
        if key == pygame.K_F5:
            self.visible = not self.visible

    def tick(self) -> None:
        self.clock.tick(self.value)

    def update(self) -> None:
        if self.visible:
            self.text = self._build_text()

    def render(self, display) -> None:
        if self.visible:
            display.blit(self.text, (200, 150))
