def convert_dimension_to_ratio(
    ratio: float, dimension: tuple[int, int]
) -> tuple[int, int]:
    width, height = dimension

    if width / height == ratio:
        return width, height
    elif height > width / ratio:
        return width, int(width / ratio)
    else:
        return int(height * ratio), height
