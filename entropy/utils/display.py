def convert_size_to_ratio(ratio: float, size: tuple[int, int]) -> tuple[int, int]:
    width, height = size

    if width / height == ratio:
        return width, height
    elif height > width / ratio:
        return width, int(width / ratio)
    else:
        return int(height * ratio), height
