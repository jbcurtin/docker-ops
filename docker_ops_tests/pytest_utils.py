import os
import pytest
import shutil

TESTING_DIR = '/tmp/docker-ops-testing'
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TESTING_TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'docker_ops_test_templates')

def setup_templates():
    if not os.path.exists(TESTING_DIR):
        os.makedirs(TESTING_DIR)

@pytest.fixture(scope='session')
def empty_gitignore_directory():
    source_dir = os.path.join(TESTING_TEMPLATE_DIR, 'empty-gitignore-directory')
    target_dir = os.path.join(TESTING_DIR, 'empty-gitignore-directory')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    setup_templates()
    shutil.copytree(source_dir, target_dir)
    return target_dir

@pytest.fixture(scope='session')
def minimal_gitignore_directory():
    source_dir = os.path.join(TESTING_TEMPLATE_DIR, 'minimal-gitignore-directory')
    target_dir = os.path.join(TESTING_DIR, 'minimal-gitignore-directory')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    setup_templates()
    shutil.copytree(source_dir, target_dir)
    return target_dir

@pytest.fixture(scope='session')
def basic_directory():
    source_dir = os.path.join(TESTING_TEMPLATE_DIR, 'basic-directory')
    target_dir = os.path.join(TESTING_DIR, 'basic-directory')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    setup_templates()
    shutil.copytree(source_dir, target_dir)
    return target_dir

@pytest.fixture(scope='session')
def artifact_directory():
    source_dir = os.path.join(TESTING_TEMPLATE_DIR, 'artifact-directory')
    target_dir = os.path.join(TESTING_DIR, 'artifact-directory')
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    setup_templates()
    shutil.copytree(source_dir, target_dir)
    return target_dir
