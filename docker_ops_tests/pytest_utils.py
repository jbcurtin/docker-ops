import os
import pytest
import shutil

TESTING_DIR = '/tmp/docker-ops-testing'
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TESTING_TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'docker_ops_test_templates')

def setup_testing_directory(name):
    source_dir = os.path.join(TESTING_TEMPLATE_DIR, name)
    target_dir = os.path.join(TESTING_DIR, name)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    if not os.path.exists(TESTING_DIR):
        os.makedirs(TESTING_DIR)

    shutil.copytree(source_dir, target_dir)
    return target_dir

@pytest.fixture(scope='session')
def empty_gitignore_directory():
    name = 'empty-gitignore-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='session')
def minimal_gitignore_directory():
    name = 'minimal-gitignore-directory'
    return setup_testing_directory(name)
    
@pytest.fixture(scope='session')
def basic_directory():
    name = 'basic-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='session')
def artifact_directory():
    name = 'artifact-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='session')
def dockerfile_directory():
    name = 'dockerfile-directory'
    return setup_testing_directory(name)

@pytest.fixture(scope='session')
def dockerfile_directory_with_source():
    name = 'dockerfile-directory-with-source'
    return setup_testing_directory(name)

@pytest.fixture(scope='function')
def images_directory_with_dockerfiles():
    name = 'images-directory-with-dockerfiles'
    return setup_testing_directory(name)
