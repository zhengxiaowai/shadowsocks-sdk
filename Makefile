clean:
	@rm -rf *.pyc __pycache__ 

publish:
	pip install twine pypandoc
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY:
	clean



