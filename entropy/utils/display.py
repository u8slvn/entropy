def dimension_to_ratio(dimension: tuple[int, int], ratio: float) -> tuple[int, int]:
    width, height = dimension
    if width / height == ratio:
        return width, height
    elif height > width / ratio:
        return width, int(width / ratio)
    else:
        return int(height * ratio), height
