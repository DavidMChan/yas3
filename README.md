# YAS3 - Yet Another S3 Client

Yas3 is a simple client for managing buckets/storage in S3 (and S3 compatible endpoints) for people who don't want the complexity of learning boto3.

## Uploading Objects

You can upload from Object paths:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.upload('test.txt', 'Object.txt', bucket='bucket')
```

Or as bytes:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.upload(Object_bytes, 'Object.txt', bucket='bucket', type='application/octet-stream')
```

The Object type is guessed using mimetypes, but it can be easily specified using ```mimetype='text/json'```.

## Downloading Objects

You can download the Object locally:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.download('Object.txt', 'test.txt', bucket='bucket')
```

Or you can get the response directly:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    bucket_data = conn.get('Object.txt', bucket='bucket')
    print(bucket_data)
```

## Object Operations

Moving Objects:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.move('Object.txt', 'new_Object.txt', source_bucket='bucket', target_bucket='bucket')
```

Copying Objects:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.copy('Object.txt', 'new_Object.txt', source_bucket='bucket', target_bucket='bucket')
```

Deleting Objects:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.delete('Object.txt', bucket='bucket')
```

Listing Objects in a bucket
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.list_Objects(bucket='bucket', prefix=None)
```

<!-- Update Object Metadata:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.update_metadata('Object.txt', metadata={'x-amz-storage-class': 'REDUCED_REDUNDANCY'}, bucket='bucket')
```

Update Object Permissions:
```python
with yas3.Connection(access_key=ACCESS_KEY, secret_key=SECRET_KEY, endpoint=ENDPOINT) as conn:
    conn.update_metadata('Object.txt', metadata={'x-amz-storage-class': 'REDUCED_REDUNDANCY'}, private=False, bucket='bucket')
``` -->

## Using it as an object

If you want to create an object, feel free:
```python
conn = yas3.Connection(...)
...
conn.close()
```

<!-- ## Multithreading

If you want to use multithreading, we support that too:
```python
conn = yas3.Connection(..., threads=10)

futures = []
for obj, obj_path in convenient_list_of_objects:
    futures.append(conn.async_upload(obj, obj_path, bucket='bucket', type='application/octet-stream'))

# Wait for a Object to be done
futures[-1].wait()

# Or upload synchronously (will wait for the data to finish uploading before continuing)
conn.upload(obj, obj_path, bucket='bucket', type='application/octet-stream')

# Wait for everything to finish
conn.wait_all()
```

Note: If you kill the program without waiting for the futures, there's no guarantee that every operation will be finished. That's on you. Be careful. -->


## Full Docs

See the full API documentation here.
