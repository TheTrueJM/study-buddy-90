# How to setup
```sh
# Create a virtual environment
python -m venv .venv

# activate venv
source .venv/bin/activate # for windows its activate.bat i think

# install uv
pip install uv

# install required packages
uv pip install -r requirements.txt
```

## How to run backend server
```sh
fastapi dev
```
Then go to server `http://localhost:8000`
