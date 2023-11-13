from to_file_like_obj import to_file_like_obj


def test_basic():
	bytes_iter = (b'ab', b'cd', b'ef')
	f = to_file_like_obj(bytes_iter)

	assert b''.join(iter(lambda: f.read(1), b'')) == b''.join(bytes_iter)
