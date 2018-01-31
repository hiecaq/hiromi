.PHONY: test install uninstall create clean upload

test:
	@pytest --pep8 -q

install:
	@pip install -e .

uninstall:
	@pip uninstall hiromi

create:
	@python setup.py sdist bdist_wheel

clean:
	@rm -rfv ./dist ./build ./.pytest_cache ./*/__pycache__ ./*/*/__pycache__

upload:
	@twine upload -s dist/*
