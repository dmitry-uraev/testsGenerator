set -ex

echo "Setting up dev environment"

export PYTHONPATH=$(pwd):$PYTHONPATH
python -m pip install poetry==1.4.2
poetry install --only dev

echo "Environment setup finished. Done"