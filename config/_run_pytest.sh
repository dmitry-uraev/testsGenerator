set -ex

echo "Running pytest"

export PYTHONPATH=$(pwd):$PYTHONPATH
pip list
python3 -m pytest tests

echo "All tests passed. Done"