import hashlib
import os

ENCODING = 'utf-8'
CHUNK_SIZE = 1024

def entry_inside_gitignore(directory_path: str, rel_filepath: str) -> bool:
    git_ignore_filepath = os.path.join(directory_path, '.gitignore')
    if not os.path.exists(git_ignore_filepath):
        return False

    with open(git_ignore_filepath, 'rb') as stream:
        git_ignore_data = [line for line in stream.read().decode(ENCODING).split('\n') if line]

    for line in git_ignore_data:
        if line == rel_filepath:
            return True

        if '*' in line:
            raise NotImplementedError

    return False

def hash_directory(directory_path: str) -> str:
    file_hashes = []
    directory_hash = hashlib.sha256()
    for root, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            rel_path = root.replace(directory_path, '').strip('/') or None
            if rel_path is None:
                filepath = f'{directory_path}/{filename}'
                rel_filepath = filename

            else:
                filepath = f'{directory_path}/{rel_path}/{filename}'
                rel_filepath = f'{rel_path}/{filename}'

            if entry_inside_gitignore(directory_path, rel_filepath):
                continue

            directory_hash.update(filepath.encode(ENCODING))
            with open(filepath, 'rb') as stream:
                while True:
                    data = stream.read(CHUNK_SIZE)
                    if not data:
                        break

                    directory_hash.update(data)

    return directory_hash.hexdigest()
