# Testing
We test the install using pytest and simulate user interaction with the plugin pytest-qt, all addional dependancies can be found under dev_resources/requirements-dev.txt 

To run all tests and make badges automatically use the bash script
```
./scripts/pytest_and_badges.sh 
```
Other wise refer below for running the individual steps


## Running tests
It is important to run all tests on a separate process to avoid conflicts. We do this using pytest-forked by:
```
pytest --forked
```

If you want to speed it up with multiprocessing use
```
pytest --forked --numprocesses=auto
```

If you want a coverage report use (this should happen automatically though):
```
pytest --forked --cov=IQM_Vis
```

## Badges
To generate the test success report badge use
```
genbadge tests --input-file tests/reports/junit/junit.xml --output-file tests/reports/tests_badge.svg 
```

To get the coverage badge use
```
coverage xml -o tests/reports/coverage/coverage.xml 
genbadge coverage --input-file tests/reports/coverage/coverage.xml--output-file tests/reports/coverage_badge.svg
```

## Linux (Ubuntu 22.04 and 24.04)
If you are having issues with the tests not running/hanging then try to use XOrg display server instead of Wayland (default for many distros without Nvidia GPU). To do this, log out and when you log in again click the gear icon in the bottom right on the screen and select XOrg instead of default/wayland.

Sometimes when using multiple displays it can cause issues/create weird window artifacts when running the tests, the tests should still be performed but use a single display or run on a laptops internal display if any errors occur.

## Windows
I believe that --forked doesn't work on windows so you must run all test separately using
```
pytest tests/test_1_making_the_UI.py
pytest tests/test_2_simple_customisation.py
pytest tests/test_3_customisation_details.py
pytest tests/test_4_experiment.py
```
