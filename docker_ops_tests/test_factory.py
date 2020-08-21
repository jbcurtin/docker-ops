from docker_ops_tests.pytest_utils import images_directory_with_dockerfiles

def test__obtain_options__empty():
    import os

    from docker_ops.factory import obtain_options

    # If we pass None to argparse.ArgumentParser().parse_args, it'll sys.exit(2)
    options = obtain_options([])
    assert options.build is True
    assert options.cron_entry is None
    assert options.directory == os.getcwd()
    assert options.schedule is False
    assert options.source_paths == []

def test__obtain_options__source_paths():
    from docker_ops.factory import obtain_options

    source_paths = ['one.py', 'two.cfg', 'three.etc']
    options = obtain_options(['-p', ','.join(source_paths)])
    assert options.source_paths == source_paths

# def test__factory_mode__build(images_directory_with_dockerfiles):
#     import os
#     os.environ['IMAGE_REGISTRY_DOMAIN'] = 'index.docker.io'
# 
#     from docker_ops import scan
#     source_paths = ['python_codes/factory.py']
#     infos = [info for info in scan.find_build_infos(images_directory_with_dockerfiles, source_paths)]
#     scan.scan_and_build(images_directory_with_dockerfiles, source_paths)
#     import pdb; pdb.set_trace()
#     import sys; sys.exit(1)
