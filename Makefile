

release:
	pip install -U twine
	make clean
	python setup.py sdist bdist_wheel --universal
	python -m twine upload --verbose dist/*

clean :
	rm -rf dist
	rm -rf build
	rm -rf docker_ops.egg-info
	rm -rf .tox
    
install: clean
	pip uninstall docker-ops
	python setup.py build
	python setup.py install

