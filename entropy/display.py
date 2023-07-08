import pygame


class Monitor:
    def __init__(self) -> None:
        self.info = pygame.display.Info()
        self.driver = pygame.display.get_driver()


class Resolution:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    def __str__(self) -> str:
        return f"{self.width} x {self.height}"


class FullScreenResolution(Resolution):
    def __init__(self, monitor: Monitor):
        super().__init__(width=monitor.info.current_w, height=monitor.info.current_h)

    def __str__(self):
        return "Fullscreen"


class Screen:
    def __init__(self, resolution: Resolution):
        self.resolution = resolution
        self.display = pygame.display.set_mode(self.resolution.size)
