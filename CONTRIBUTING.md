# Contributing to SMOCKS

Publishing
----------

To prepare for publishing, you need to clear out the dist directory.

1) Update the version in setup.py; you can publish a version only once
2) Prepare the distribution with `python setup.py sdist bdist_wheel`
3) Ensure the PyPI environment variables for directory and authentication are correct
* TWINE_USERNAME=(redacted)
* TWINE_PASSWORD=(redacted)
* TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/ or https://pypi.org/
3) Publish to the directory with `twine upload dist/*`

Testing
-------
To isoloate generated test code from the source for this project, set the 
SMOACKS_ROOT environment variable to a subdirectory name for generated
output:

`export SMOACKS_ROOT=temp`

To ensure no runtime errors before publishing, start a python session, then

`import smoacks.command_line`
`smoacks.command_line.main()`
`smoacks.command_line.gen()`

This should run the environment and code generation.
