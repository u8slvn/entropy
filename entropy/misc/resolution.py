class Resolution:
    def __init__(self, width: int, height: int, alias: str = ""):
        self.width = width
        self.height = height
        self.alias = f"{width}x{height}" if alias == "" else alias

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height


r720P = Resolution(width=1280, height=720)
r900P = Resolution(width=1600, height=900)
r1080P = Resolution(width=1920, height=1080)
r1440P = Resolution(width=2560, height=1440)
r2160P = Resolution(width=3840, height=2160)
