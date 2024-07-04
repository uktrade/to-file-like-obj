from io import IOBase
from typing import Iterable, Type
from typing_extensions import Buffer


def to_file_like_obj(iterable: Iterable[bytes], base: Type[bytes]=bytes) -> IOBase:
    chunk: bytes = base()
    offset: int = 0
    it = iter(iterable)

    def up_to_iter(size: int) -> Iterable[Buffer]:
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
        def readable(self) -> bool:
            return True

        def read(self, size: int=-1) -> bytes:
            return base().join(
                up_to_iter(float('inf') if size is None or size < 0 else size)
            )

    return FileLikeObj()
