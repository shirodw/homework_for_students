def zero(op=None):
    if not op:
        return 0
    else:
        return op(0)


def one(op=None):
    if not op:
        return 1
    else:
        return op(1)


def two(op=None):
    if not op:
        return 2
    else:
        return op(2)


def three(op=None):
    if not op:
        return 3
    else:
        return op(3)


def four(op=None):
    if not op:
        return 4
    else:
        return op(4)


def five(op=None):
    if not op:
        return 5
    else:
        return op(5)


def six(op=None):
    if not op:
        return 6
    else:
        return op(6)


def seven(op=None):
    if not op:
        return 7
    else:
        return op(7)


def eight(op=None):
    if not op:
        return 8
    else:
        return op(8)


def nine(op=None):
    if not op:
        return 9
    else:
        return op(9)


def plus(y):
    return lambda x: x + y


def minus(y):
    return lambda x: x - y


def times(y):
    return lambda x: x * y


def divided_by(y):
    return lambda x: x // y
