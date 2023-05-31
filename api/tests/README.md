APP_CONFIG=env/local/xrpl-poc-python-app.env pytest -q api/tests/test_*.py -o log_cli=true

APP_CONFIG=env/local/xrpl-poc-python-app.env \
    pytest -q api/tests/test_encrypt.py \
    --log-cli-level=INFO \
    -o log_cli=true

api/tests/test_encrypt.py