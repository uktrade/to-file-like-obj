# to-file-like-obj

Python utility function to convert an iterable of `bytes` or `str` to a readable file-like object.

It can be seen as the inverse of the [two-argument iter function](https://docs.python.org/3/library/functions.html#iter). The iter function allows conversion of file-like objects to iterables, but the function here converts from iterables to file-like objects. This allows you to bridge the gap between incompatible streaming APIs - passing data from sources that offer data as iterables to destinations that only accept file-like objects.


## Features

- Inherits from `IOBase` - some APIs require this
- The resulting file-like object is well-behaved - it does not return more data than requested
- It evaluates the iterable lazily - avoiding loading all its data into memory
- Under the hood copying is avoided as much as possible
- Converts iterables of `bytes` to bytes-based file-like objects, which can be passed to [boto3's upload_fileobj](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_fileobj.html) or to [io.TextIOWrapper](https://docs.python.org/3/library/io.html#io.TextIOWrapper)
- Converts iterables of `str` to text-based file-like objects, which can be passed to [psycopg2's copy_expert](https://www.psycopg.org/docs/cursor.html#cursor.copy_expert)


## Installation

```shell
pip install to-file-like-obj
```


## Usage

If you have an iterable of `bytes` instances, you can pass them to the `to_file_like_obj` function, and it will return the corresponding file-like object.

```python
from to_file_like_obj import to_file_like_obj

f = to_file_like_obj((b'one', b'two', b'three',))

print(f.read(5))  # b'onetw'
print(f.read(6))  # b'othree'
```

If you have an iterable of `str` instances, you can pass them to the `to_file_like_obj`, along with `base=str` as a named argument, and it will return the corresponding file-like object.

```python
from to_file_like_obj import to_file_like_obj

f = to_file_like_obj(('one', 'two', 'three',), base=str)

print(f.read(5))  # 'onetw'
print(f.read(6))  # 'othree'
```

These examples have the iterables hard coded and so loaded all into memory. However, `to_file_like_obj` works equally well with iterables that are generated dynamically, and without loading them all into memory.
