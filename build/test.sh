source venv/bin/activate

coverage run --omit='env/*,tests/*' --parallel-mode -m pytest -s --durations=10 --junitxml results.xml --capture=no --strict-markers tests
coverage combine
coverage xml --omit='env/*,tests/*' -o ./reports/cobertura.xml
coverage html
coverage report -m --omit='env/*,tests/*'

rm -f .coverage
rm -rf .pytest_cache
rm -rf htmlcov
rm -rf reports
rm -f results.xml
