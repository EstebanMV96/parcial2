#!/usr/bin/env bash
set -e 

. ~/.virtualenvs/testproject/bin/activate

PYTHONPATH=. py.test --junitxml=informe.xml
