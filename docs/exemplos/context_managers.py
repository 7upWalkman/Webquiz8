from contextlib import contextmanager

@contextmanager
def cmA():
    print("Acquiring A")
    try:
        yield 'A'
    finally:
        print("Releasing A")

@contextmanager
def cmB():
    print("Acquiring B")
    try:
        yield 'B'
    finally:
        print("Releasing B")


def test_a_b():
    with cmA():
        with cmB():
            print("TEST_A_B")


@contextmanager
def cmX():
    with cmA():
        with cmB():
            print("Aquiring X")
            try: 
                yield 'X'
            finally:
                print("Releasing X")

@contextmanager
def cmXX():
    with cmA():
        with cmB():
            print("Aquiring X")
            yield 'X'
            print("Releasing X")

