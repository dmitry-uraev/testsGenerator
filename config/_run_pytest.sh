set -ex

echo "Running pytest"

export PYTHONPATH=$(pwd):$PYTHONPATH
poetry run pytest tests

echo "All tests passed. Done"