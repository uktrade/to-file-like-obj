from io import IOBase
from typing import Union, TypeVar, Iterable, Type, Iterator, overload

T = TypeVar('T', str, bytes)

@overload
def to_file_like_obj(iterable: Iterable[bytes]) -> IOBase:
    ...

@overload
def to_file_like_obj(iterable: Iterable[bytes], base: Type[bytes]) -> IOBase:
    ...

@overload
def to_file_like_obj(iterable: Iterable[str], base: Type[str]) -> IOBase:
    ...

def to_file_like_obj(iterable: Iterable[T], base=bytes) -> IOBase:
    chunk = base()
    offset: int = 0
    it = iter(iterable)

    def up_to_iter(size: Union[int, float]) -> Iterator[T]:
        nonlocal chunk, offset

        while size:
            if offset == len(chunk):
                try:
                    chunk = next(it)
                except StopIteration:
                    break
                else:
                    offset = 0
            to_yield = int(min(size, len(chunk) - offset))
            offset = offset + to_yield
            size -= to_yield
            yield chunk[offset - to_yield : offset]

    class FileLikeObj(IOBase):
        def readable(self) -> bool:
            return True

        def read(self, size: int=-1) -> T:
            return base().join(
                up_to_iter(float('inf') if size is None or size < 0 else size)
            )

    return FileLikeObj()
