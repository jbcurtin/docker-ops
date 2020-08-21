import os
import pytest
import shutil
import uuid

from docker_ops_tests.pytest_constants import TESTING_DIR, PROJECT_DIR, TESTING_TEMPLATE_DIR

def setup_testing_directory(name):
    source_dir = os.path.join(TESTING_TEMPLATE_DIR, name)
    target_dir = os.path.join(TESTING_DIR, name)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    if not os.path.exists(TESTING_DIR):
        os.makedirs(TESTING_DIR)

    shutil.copytree(source_dir, target_dir)
    return target_dir

@pytest.fixture(scope='function')
def empty_gitignore_directory():
    name = 'empty-gitignore-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='function')
def minimal_gitignore_directory():
    name = 'minimal-gitignore-directory'
    return setup_testing_directory(name)
    
@pytest.fixture(scope='function')
def basic_directory():
    name = 'basic-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='function')
def artifact_directory():
    name = 'artifact-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='function')
def dockerfile_directory():
    name = 'dockerfile-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='function')
def dockerfile_directory_with_source():
    name = 'dockerfile-directory-with-source'
    return setup_testing_directory(name)

@pytest.fixture(scope='function')
def images_directory_with_dockerfiles():
    name = 'images-directory-with-dockerfiles'
    return setup_testing_directory(name)

@pytest.fixture(scope='function')
def deeply_nested_source_files():
    name = 'deeply-nested-source-files'
    return setup_testing_directory(name)

