import hashlib
import zlib
import os


def compress_data(object_to_store):
    return zlib.compress(str_to_bytes(object_to_store))


def str_to_bytes(input: str) -> bytes:
    return input.encode("utf-8")


def compute_sha1(input: str) -> str:
    sha = hashlib.sha1()
    sha.update(str_to_bytes(input))
    return sha.hexdigest()


def str_utf8_size(input: str) -> int:
    return len(str_to_bytes(input))


def add_to_store(input: str):
    """
    Create a Git blob from input and add it to the Git object store.

    The function must be run at the root of a Git repository. It cannot be ran two times
    in a row with the same input, because it will crash due to the object already being
    in the data store.


    Examples:
    ```
    add_to_store("is python a real programming language?")
    ```
    """

    # Create header and concatenate with the input
    header = f"blob {str_utf8_size(input)}\0"
    object_to_store = header + input

    # Compute the SHA1 of the object to store
    sha = compute_sha1(object_to_store)
    print(f"Object SHA: {sha}")

    # Compress the object to store using Zlib
    to_store_compressed = compress_data(object_to_store)
    print(f"Compressed data: {to_store_compressed}")

    # Create directory to store the compressed data
    object_store_path = f".git/objects/{sha[0:2]}"
    os.makedirs(object_store_path)
    print(f"Created directory at: {object_store_path}")

    # Write compressed data to disk
    f = open(f"{object_store_path}/{sha[2:]}", "xb")
    f.write(to_store_compressed)
    f.close()
    print(f"Wrote compressed data at: {object_store_path}/{sha[2:]}")

    print(f"Run `git cat-file -p {sha}` to double check!")


# Uncomment the following lines to test

# m = "what is up, doc?"
# add_to_object_store(m)
