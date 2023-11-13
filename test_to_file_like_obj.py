import io

import pytest

from to_file_like_obj import to_file_like_obj


def test_basic():
    bytes_iter = (b'ab', b'cd', b'ef')
    f = to_file_like_obj(bytes_iter)

    assert [f.read(1) for _ in range(0, 7)] == [b'a', b'b', b'c', b'd', b'e', b'f', b'']


def test_basic_bytes_base():
    bytes_iter = (b'ab', b'cd', b'ef')
    f = to_file_like_obj(bytes_iter, base=bytes)

    assert [f.read(1) for _ in range(0, 7)] == [b'a', b'b', b'c', b'd', b'e', b'f', b'']


def test_basic_str_base():
    bytes_iter = ('ab', 'cd', 'ef')
    f = to_file_like_obj(bytes_iter, base=str)

    assert [f.read(1) for _ in range(0, 7)] == ['a', 'b', 'c', 'd', 'e', 'f', '']


def test_read_crossing_chunk_boundaries():
    bytes_iter = (b'ab', b'cd', b'ef')
    f = to_file_like_obj(bytes_iter)

    assert [f.read(3), f.read(2), f.read(2), f.read(2)] == [b'abc', b'de', b'f', b'']


def test_lazy_iteration():
    bytes_iter = (b'ab', b'cd', b'ef')

    log = []
    def logged(it):
        for v in it:
            log.append(v)
            yield v

    f = to_file_like_obj(logged(bytes_iter))

    while c := f.read(1):
        log.append(c)

    assert log == [b'ab', b'a', b'b', b'cd', b'c', b'd', b'ef', b'e', b'f']


def test_exception_propagates():
    def bytes_iter():
        yield from ()
        raise Exception("My exception")

    f = to_file_like_obj(bytes_iter())

    with pytest.raises(Exception, match="My exception"):
        f.read()


def test_textiowrapper_groups_into_lines():
    bytes_iter = (b'a\nb', b'c\nd', b'e\nf')
    f = to_file_like_obj(bytes_iter)

    lines = io.TextIOWrapper(f, newline='', encoding='utf=8')
    assert list(lines) == ['a\n', 'bc\n', 'de\n', 'f']


@pytest.mark.parametrize(
    "args,kwargs",
    [
        ((), {}),
        ((-1,), {}),
        ((), {"size": -1}),
        ((None,), {}),
        ((), {"size": None}),
    ]
)
def test_default(args, kwargs):
    bytes_iter = (b'ab', b'cd', b'ef')
    f = to_file_like_obj(bytes_iter)

    assert f.read(*args, **kwargs) == b'abcdef'
