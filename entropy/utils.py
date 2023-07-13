def dimension_to_ratio(dimension: tuple[int, int], ratio: float) -> tuple[int, int]:
    w, h = dimension
    if w / h == ratio:
        return w, h
    elif h > w / ratio:
        return w, int(w / ratio)
    else:
        return int(h * ratio), h
