# Testing
We test the install using pytest and simulate user interaction with the plugin pytest-qt, all addional dependancies can be found under dev_resources/requirements-dev.txt 

## Running tests
It is important to run all tests on a separate process to avoid conflicts. We do this using pytest-forked by:
```
pytest --forked
```
or if you want to speed it up with multiprocessing use
```
pytest --forked --numprocesses=auto
```

## Windows
I believe that --forked doesn't work on windows so you must run all test separately using
```
pytest tests/test_1_making_the_UI.py
pytest tests/test_2_simple_customisation.py
pytest tests/test_3_customisation_details.py
pytest tests/test_4_experiment.py
```
