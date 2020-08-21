import pytest

from docker_ops_tests.pytest_constants import TESTING_DIR
from docker_ops_tests.pytest_utils import dockerfile_directory, dockerfile_directory_with_source, \
    images_directory_with_dockerfiles, deeply_nested_source_files

def test_Hash(dockerfile_directory):
    import os

    from docker_ops.scan import Hash

    dockerfile_path = os.path.join(dockerfile_directory, 'Dockerfile')
    expected_hash = '6ccfd093a9c755debee29b63a88144c867feb6e51e442abd99455e74bf886af2'
    assert Hash(dockerfile_path).get_hash() == expected_hash

def test_Hash__with_source(dockerfile_directory_with_source):
    import os

    from docker_ops.scan import Hash
    dockerfile_path = os.path.join(dockerfile_directory_with_source, 'Dockerfile')
    source_paths = [os.path.join(dockerfile_directory_with_source, 'python_codes/factory.py')]
    expected_hash = '4c424b3272800bc07e07baf5792602ff77bc45bd1d729a024e513526eeedcb02'
    assert Hash(dockerfile_path, []).get_hash() != expected_hash
    assert Hash(dockerfile_path, source_paths).get_hash() == expected_hash

def test__Version():
    from docker_ops.scan import Version

    version = Version('0.0.0')
    assert version._major == 0
    assert version._minor == 0
    assert version._minor_minor == 0
    assert version.get_version() == '0.0.0'

    version_none = Version(None)
    assert version_none._major == 0
    assert version_none._minor == 0
    assert version_none._minor_minor == 0
    assert version_none.get_version() == '0.0.0'

    version_other = Version('1.2.3')
    assert version_other._major == 1
    assert version_other._minor == 2
    assert version_other._minor_minor == 3
    assert version_other.get_version() == '1.2.3'

    version_inc = Version('3.2.1')
    assert version_inc._major == 3
    assert version_inc._minor == 2
    assert version_inc._minor_minor == 1
    assert version_inc.get_version() == '3.2.1'
    version_inc.inc_minor_minor()
    assert version_inc._major == 3
    assert version_inc._minor == 2
    assert version_inc._minor_minor == 2
    assert version_inc.get_version() == '3.2.2'

def test__find_build_infos(images_directory_with_dockerfiles):
    from docker_ops.scan import find_build_infos, BuildInfo
    for build_info in find_build_infos(images_directory_with_dockerfiles, []):
        assert build_info.version.get_version() == '0.0.0'
        assert len(build_info._source_paths) is 0

def test__find_build_infos__source_paths(images_directory_with_dockerfiles):
    from docker_ops.scan import find_build_infos, BuildInfo

    for build_info in find_build_infos(images_directory_with_dockerfiles, ['python_codes/factory.py']):
        assert build_info.version.get_version() == '0.0.0'
        if build_info.name in ['image-three', 'image-four']:
            assert build_info._source_paths[0].endswith('python_codes')

        else:
            assert len(build_info._source_paths) is 0

def test__Docker(dockerfile_directory_with_source):
    import docker
    import os

    from docker_ops.scan import Docker
    from docker_ops.constants import IMAGE_REGISTRY_DOMAIN

    dockerfile_path = os.path.join(dockerfile_directory_with_source, 'Dockerfile')
    docker_instance = Docker(dockerfile_directory_with_source, dockerfile_path)
    assert docker_instance._dockerfile_path == 'Dockerfile'
    assert docker_instance._build_dir == dockerfile_directory_with_source
    assert isinstance(docker_instance._client, docker.APIClient)
    build_name = os.path.basename(dockerfile_directory_with_source)
    build_name_full = f'{IMAGE_REGISTRY_DOMAIN}/{build_name}'
    assert docker_instance._build_name == build_name
    assert docker_instance._build_name_full == build_name_full

import json
import types
class DockerAPIClientMock:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def _mock_build(self) -> str:
        for idx in range(1, 4):
            stream = f'Build: {idx}'
            yield json.dumps({'stream': stream}).encode('utf-8')

    def build(self, path: str, dockerfile: str, tag: str) -> types.GeneratorType:
        return self._mock_build()

    def _mock_push(self) -> types.GeneratorType:
        for idx in range(1, 4):
            stream = f'Pushing: {idx}'
            yield stream

    def push(self, path: str, version: str, stream: bool, decode: bool) -> types.GeneratorType:
        return self._mock_push()

    def tag(self, existing_tag: str, new_tag: str, version: str) -> None:
        pass

def test__Docker__build(dockerfile_directory_with_source, monkeypatch):
    import docker
    import os

    from docker_ops.scan import Docker

    # monkeypatch.setattr(docker, 'APIClient', DockerAPIClientMock)
    dockerfile_path = os.path.join(dockerfile_directory_with_source, 'Dockerfile')
    docker_instance = Docker(dockerfile_directory_with_source, dockerfile_path)
    build_version = 'latest'
    build_name = docker_instance.build(build_version, verbose=False)
    assert build_name == f'{docker_instance._build_name}:{build_version}'
    build_version = '0.0.0'
    build_name = docker_instance.build(build_version, verbose=False)
    assert build_name == f'{docker_instance._build_name}:{build_version}'

def test__Docker__push(dockerfile_directory_with_source, monkeypatch):
    import docker
    import os

    from docker_ops.scan import Docker

    monkeypatch.setattr(docker, 'APIClient', DockerAPIClientMock)
    dockerfile_path = os.path.join(dockerfile_directory_with_source, 'Dockerfile')
    docker_instance = Docker(dockerfile_directory_with_source, dockerfile_path)
    build_version = 'latest'
    build_name = docker_instance.build(build_version, verbose=False)
    assert ':'.join([docker_instance._build_name, build_version]) == build_name
    push_build_name = docker_instance.push(build_version, verbose=False)
    assert ':'.join([docker_instance._build_name_full, build_version]) == push_build_name

def test__Docker__push_custom_registry(dockerfile_directory_with_source, monkeypatch):
    import docker
    import os

    os.environ['IMAGE_REGISTRY_DOMAIN'] = 'registry.jbcurtin.io'
    from docker_ops.scan import Docker

    monkeypatch.setattr(docker, 'APIClient', DockerAPIClientMock)
    dockerfile_path = os.path.join(dockerfile_directory_with_source, 'Dockerfile')
    docker_instance = Docker(dockerfile_directory_with_source, dockerfile_path)
    build_version = 'latest'
    build_name = docker_instance.build(build_version, verbose=False)
    assert ':'.join([docker_instance._build_name, build_version]) == build_name
    push_build_name = docker_instance.push(build_version, verbose=False)
    assert ':'.join([docker_instance._build_name_full, build_version]) == push_build_name
    del os.environ['IMAGE_REGISTRY_DOMAIN']

