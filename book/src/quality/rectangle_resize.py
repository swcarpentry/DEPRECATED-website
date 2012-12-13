def normalize_rectangle(rect):
    [[x0, y0], [x1, y1]] = rect
    assert x0 < x1, 'Invalid X coordinates'
    assert y0 < y1, 'Invalid Y coordinates'
    dx = x1 - x0
    dy = y1 - y0
    if dx > dy:
        scaled = float(dy) / dx
        upper = [1.0, scaled]
    else:
        scaled = float(dx) / dy
        upper = [scaled, 1.0]

    assert 0 < upper[0] <= 1.0, 'Calculated upper X coordinate invalid'
    assert 0 < upper[1] <= 1.0, 'Calculated upper Y coordinate invalid'

    return [[0, 0], upper]
