import io

import pytest

from to_file_like_obj import to_file_like_obj


def test_basic():
    bytes_iter = (b'ab', b'cd', b'ef')
    f = to_file_like_obj(bytes_iter)

    assert b''.join(iter(lambda: f.read(1), b'')) == b''.join(bytes_iter)


def test_basic_bytes_base():
    bytes_iter = (b'ab', b'cd', b'ef')
    f = to_file_like_obj(bytes_iter, base=bytes)

    assert b''.join(iter(lambda: f.read(1), b'')) == b''.join(bytes_iter)


def test_basic_str_base():
    bytes_iter = ('ab', 'cd', 'ef')
    f = to_file_like_obj(bytes_iter, base=str)

    assert ''.join(iter(lambda: f.read(1), '')) == ''.join(bytes_iter)


def test_well_behaved():
    bytes_iter = (b'ab', b'cd', b'ef')
    f = to_file_like_obj(bytes_iter)

    assert list(iter(lambda: len(f.read(1)), 0)) == [1, 1, 1, 1, 1, 1]


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


def test_textiowrapper_groups_into_lines():
    bytes_iter = (b'a\nb', b'c\nd', b'e\nf')
    f = to_file_like_obj(bytes_iter)

    lines = io.TextIOWrapper(f, newline='', encoding='utf=8')
    assert list(lines) == ['a\n', 'bc\n', 'de\n', 'f']
