class InvalidInput(Exception):
    pass


class BadTriangle(Exception):
    pass


def dst(x, y):
    return (x ** 2 + y ** 2) ** 0.5


def triangleSquare(inp):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(inp)
    except Exception:
        raise InvalidInput

    s1 = dst(x1 - x2, y1 - y2)
    s2 = dst(x2 - x3, y2 - y3)
    s3 = dst(x3 - x1, y3 - y1)
    if max(s1, s2, s3) >= min(s1 + s2, s2 + s3, s1 + s3):
        raise BadTriangle

    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2


while True:
    try:
        sq = triangleSquare(input())
    except InvalidInput:
        print("InvalidInput")
    except BadTriangle:
        print("Not a triangle")
    else:
        print(sq)
        break

