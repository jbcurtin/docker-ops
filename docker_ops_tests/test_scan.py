import pytest

from docker_ops_tests.pytest_utils import dockerfile_directory, dockerfile_directory_with_source, \
    images_directory_with_dockerfiles

@pytest.fixture(scope='function', autouse=True)
def setup_environment(request):
    import os
    os.environ['IMAGE_REGISTRY_DOMAIN'] = 'jbcurtin.io'

    def destroy_environment():
        del os.environ['IMAGE_REGISTRY_DOMAIN']

    request.addfinalizer(destroy_environment)

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
    source_paths = [os.path.join(dockerfile_directory_with_source, 'python_codes')]
    expected_hash = '28d2cc4786430ce845a1d1d8297b64ed352342fd82a67b1a46c12ba2d227b74f'
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

def test__find_python_source_directories(images_directory_with_dockerfiles):
    from docker_ops.scan import find_python_source_directories

    source_paths = find_python_source_directories(images_directory_with_dockerfiles)
    assert 'image-three/python_codes' in source_paths
    assert 'image-four/python_codes' in source_paths

def test__find_build_infos(images_directory_with_dockerfiles):
    import os

    from docker_ops.scan import find_build_infos, BuildInfo
    for build_info in find_build_infos(images_directory_with_dockerfiles):
        assert build_info.version.get_version() == '0.0.0'

def test_scan():
    pass

