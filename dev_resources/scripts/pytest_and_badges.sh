#!/usr/bin/bash
# Author: Matt Clifford <matt.clifford@bristol.ac.uk>
# License: BSD 3-Clause License

pytest
genbadge tests --input-file tests/reports/junit/junit.xml --output-file tests/reports/tests_badge.svg 
coverage xml -o tests/reports/coverage/coverage.xml 
genbadge coverage --input-file tests/reports/coverage/coverage.xml --output-file tests/reports/coverage_badge.svg
