from io import IOBase


def to_file_like_obj(iterable, base=bytes):
    chunk = base()
    offset = 0
    it = iter(iterable)

    def up_to_iter(size):
        nonlocal chunk, offset

        while size:
            if offset == len(chunk):
                try:
                    chunk = next(it)
                except StopIteration:
                    break
                else:
                    offset = 0
            to_yield = min(size, len(chunk) - offset)
            offset = offset + to_yield
            size -= to_yield
            yield chunk[offset - to_yield : offset]

    class FileLikeObj(IOBase):
        def readable(self):
            return True

        def read(self, size=-1):
            return base().join(
                up_to_iter(float('inf') if size is None or size < 0 else size)
            )

    return FileLikeObj()
