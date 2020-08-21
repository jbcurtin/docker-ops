from docker_ops_tests.pytest_utils import basic_directory, artifact_directory, empty_gitignore_directory, \
    minimal_gitignore_directory, images_directory_with_dockerfiles, deeply_nested_source_files

def test__entry_inside_gitignore__none():
    import uuid

    from docker_ops.utils import entry_inside_gitignore
    assert entry_inside_gitignore(f'/tmp/{uuid.uuid4()}', 'env') is False
    assert entry_inside_gitignore(f'/tmp/{uuid.uuid4()}', 'data') is False
    assert entry_inside_gitignore(f'/tmp/{uuid.uuid4()}', 'other') is False

def test__entry_inside_gitignore__empty(empty_gitignore_directory):
    from docker_ops.utils import entry_inside_gitignore
    assert entry_inside_gitignore(empty_gitignore_directory, 'env') is False
    assert entry_inside_gitignore(empty_gitignore_directory, 'data') is False
    assert entry_inside_gitignore(empty_gitignore_directory, 'other') is False

def test__entry_inside_gitignore__minimal(minimal_gitignore_directory):
    from docker_ops.utils import entry_inside_gitignore
    assert entry_inside_gitignore(minimal_gitignore_directory, 'env') is True
    assert entry_inside_gitignore(minimal_gitignore_directory, 'data') is True
    assert entry_inside_gitignore(minimal_gitignore_directory, 'other') is False

def test__hash_directory__basic_directory(basic_directory):
    from docker_ops.utils import hash_directory
    expected_hash = '6e176af702e6a782f030093f51342d2406249d6369d1f9beb48f34f4b24d303b'
    assert expected_hash == hash_directory(basic_directory)

def test__hash_directory__artifact_directory(artifact_directory):
    from docker_ops.utils import hash_directory
    # incorrect_hash should match the expected_hash from test__hash_directory__basic_directory
    incorrect_hash = '6e176af702e6a782f030093f51342d2406249d6369d1f9beb48f34f4b24d303b'
    assert hash_directory(artifact_directory) != incorrect_hash
    expected_hash = 'efd071191337b48c1d6c2429ee801d09c52c2a965498d920ae00a7de72dce794'
    assert hash_directory(artifact_directory) == expected_hash

def test__find_source_directories(images_directory_with_dockerfiles):
    from docker_ops.utils import find_source_directories 

    source_paths = find_source_directories(images_directory_with_dockerfiles, 'python_codes/factory.py')
    assert 'image-three' in source_paths
    assert 'image-four' in source_paths

