class InvalidInput(Exception):
    pass


class BadTriangle(Exception):
    pass


def dst(x, y):
    return ((x[0] - x[1])** 2 + (y[0] - y[1])** 2) ** 0.5


def triangleSquare(inp):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(inp)
    except Exception:
        raise InvalidInput

    try:
        s1 = dst((x1,x2), (y1,y2))
        s2 = dst((x2,x3), (y2,y3))
        s3 = dst((x1,x3), (y1,y3))
    except Exception:
        raise BadTriangle

    if max(s1, s2, s3) >= min(s1 + s2, s2 + s3, s1 + s3):
        raise BadTriangle

    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2


while b := input():
    try:
        sq = triangleSquare(b)
    except InvalidInput:
        print("Invalid input")
    except BadTriangle:
        print("Not a triangle")
    except Exception:
        break
    else:
        print("%.2f"%sq)
        break

