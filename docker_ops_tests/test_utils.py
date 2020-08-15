from docker_ops_tests.pytest_utils import basic_directory, artifact_directory, empty_gitignore_directory, minimal_gitignore_directory

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
    expected_hash = '21fc0fe406cd3b407d6924ec649a8928d98e1bf5b8d09f79907b931c060e5f25'
    assert expected_hash == hash_directory(basic_directory)

def test__hash_directory__artifact_directory(artifact_directory):
    from docker_ops.utils import hash_directory
    incorrect_hash = '7747f2a3eef9205d93cc6cbd44d713071cfdb1dde0192352a958eb0135c717a8'
    assert hash_directory(artifact_directory) != incorrect_hash
    expected_hash = '3032aa0e95f21926d8b797c582ffa51f3ad0b013110ab041488482e8aeb1854c'
    assert hash_directory(artifact_directory) == expected_hash

