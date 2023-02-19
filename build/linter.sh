#!/bin/bash

source venv/bin/activate

isort .
black .
flake8 .
