# to-file-like-obj

Python utility function to convert an iterable of `bytes` or `str` to a readable file-like object.

> Work in progress. This README serves as a rough design spec


## Features

- Inherits from `IOBase` - some APIs require this
- The file-like object is well-behaved - it does not return more data than requested
- It evaluates the iterable lazily - avoiding loading all the data into memory
- Under the hood copying is avoided as much as possible
- Supports iterables of `bytes`, which can be passed to [boto3's upload_fileobj](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_fileobj.html), or to [io.TextIOWrapper](https://docs.python.org/3/library/io.html#io.TextIOWrapper) which is useful to robustly parse CSV files in a streaming way.
- Supports iterables of `str`, which can be passed to the[psycopg2's copy_expert](https://www.psycopg.org/docs/cursor.html#cursor.copy_expert)


## Installation

```shell
pip install to-file-like-obj
```


## Usage

If you have an iterable of `bytes` instances, you can pass them to the `to_file_like_obj` function, and it will return the corresponding file-like object.

```python
from to_file_like_obj import to_file_like_obj

f = to_file_like_obj((b'one', b'two', b'three',))
```

If you have an iterable of `str` instances, you can pass them to the `to_file_like_obj`, along with `base=str` as a named argument, and it will return the corresponding file-like object.

```python
from to_file_like_obj import to_file_like_obj

f = to_file_like_obj(('one', 'two', 'three',), base=str)
```
