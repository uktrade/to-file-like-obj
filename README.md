# to-file-like-obj

[![PyPI package](https://img.shields.io/pypi/v/to-file-like-obj?label=PyPI%20package&color=%234c1)](https://pypi.org/project/to-file-like-obj/) [![Test suite](https://img.shields.io/github/actions/workflow/status/uktrade/to-file-like-obj/test.yml?label=Test%20suite)](https://github.com/uktrade/to-file-like-obj/actions/workflows/test.yml) [![Code coverage](https://img.shields.io/codecov/c/github/uktrade/to-file-like-obj?label=Code%20coverage)](https://app.codecov.io/gh/uktrade/to-file-like-obj)

Python utility function to convert an iterable of `bytes` or `str` to a readable file-like object.

It can be seen as the inverse of the [two-argument iter function](https://docs.python.org/3/library/functions.html#iter). The iter function allows conversion of file-like objects to iterables, but the function here converts from iterables to file-like objects. This allows you to bridge the gap between incompatible streaming APIs - passing data from sources that offer data as iterables to destinations that only accept file-like objects.


## Features

- Inherits from `IOBase` - some APIs require this
- The resulting file-like object is well-behaved - it does not return more data than requested
- It evaluates the iterable lazily - avoiding loading all its data into memory
- Under the hood copying is avoided as much as possible
- Converts iterables of `bytes` to bytes-based file-like objects, which can be passed to [boto3's upload_fileobj](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_fileobj.html) or to [io.TextIOWrapper](https://docs.python.org/3/library/io.html#io.TextIOWrapper) which is useful in stream CSV parsing.
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


## Recipe: parsing a CSV file while downloading it

Using [httpx](https://www.python-httpx.org/) it's possible to use the `to_file_like_obj` function to parse a CSV file while downloading it.

```python
import csv
import io

import httpx
from to_file_like_obj import to_file_like_obj

with httpx.stream("GET", "https://www.example.com/my.csv") as r:
    bytes_iter = r.iter_bytes()
    f = to_file_like_obj(bytes_iter)
    lines_iter = io.TextIOWrapper(f, newline='', encoding='utf=8')
    rows_iter = csv.reader(lines):
    for row in rows_iter:
        print(row)
```


## Recipe: parsing a zipped CSV file while downloading it

Similarly, using [httpx](https://www.python-httpx.org/) and [stream-unzip](https://stream-unzip.docs.trade.gov.uk/), it's possible to use the `to_file_like_obj` function to robustly parse a zipped CSV file while downloading it.

```python
import csv
import io

import httpx
from stream_unzip import stream_unzip
from to_file_like_obj import to_file_like_obj

with httpx.stream("GET", "https://www.example.com/my.zip") as r:
    zipped_bytes_iter = r.iter_bytes()
    # Assumes a single CSV file in the ZIP (in the case of more, this will concatanate them together)
    unzipped_bytes_iter = (
        chunks
        for _, _, chunks in stream_unzip(zipped_bytes_iter)
        for chunk in chunks
    )
    f = to_file_like_obj(unzipped_bytes_iter)
    lines_iter = io.TextIOWrapper(f, newline='', encoding='utf=8')
    rows_iter = csv.reader(lines):
    for row in rows_iter:
        print(row)
```


## Recipe: uploading large objects to S3 while receiving their contents

[boto3's upload_fileobj](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/upload_fileobj.html) is a powerful function, but it's not obvious that it can be used with iterables of bytes that are returned from various APIs, such as those in [httpx](https://www.python-httpx.org/).

```python
import httpx
from to_file_like_obj import to_file_like_obj

s3 = boto3.client('s3')

with httpx.stream("GET", "https://www.example.com/my.zip") as r:
    bytes_iter = r.iter_bytes()
    f = to_file_like_obj(bytes_iter)
    s3.upload_fileobj(f, 'my-bucket', 'my.zip')
```


## Recipe: stream-zipping while uploading to S3

[stream-zip](https://stream-zip.docs.trade.gov.uk/) can be used with boto3 and this package to upload objects to S3 while zipping them.

```python
import datetime
import httpx
from stat import S_IFREG
from to_file_like_obj import to_file_like_obj
from stream_zip import ZIP_32, stream_zip

s3 = boto3.client('s3')

with httpx.stream("GET", "https://www.example.com/my.txt") as r:
    unzipped_bytes_iter = r.iter_bytes()
    member_files = (
        (
            'my.txt',
            datetime.now(),
            S_IFREG | 0o600,
            ZIP_32,
            unzipped_bytes_iter,
        ),
    )
    zipped_bytes_iter = stream_zip(member_files)
    f = to_file_like_obj(zipped_bytes_iter)
    s3.upload_fileobj(f, 'my-bucket', 'my.zip')
```
