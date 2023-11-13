import io

from to_file_like_obj import to_file_like_obj


def test_basic():
	bytes_iter = (b'ab', b'cd', b'ef')
	f = to_file_like_obj(bytes_iter)

	assert b''.join(iter(lambda: f.read(1), b'')) == b''.join(bytes_iter)


def test_textiowrapper_groups_into_lines():
	bytes_iter = (b'a\nb', b'c\nd', b'e\nf')
	f = to_file_like_obj(bytes_iter)

	lines = io.TextIOWrapper(f, newline='', encoding='utf=8')
	assert list(lines) == ['a\n', 'bc\n', 'de\n', 'f']
