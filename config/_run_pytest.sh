set -ex

echo "Running pytest"

export PYTHONPATH=$(pwd):$PYTHONPATH
python -m pytest tests

echo "All tests passed. Done"