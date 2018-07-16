# core



## Setup

Create virtualenv:
```
virtualenv --python=/usr/bin/python3.5 ~/.virtualenvs/core

```

Install requirements:
```
pip install -r requirements.txt
```

# RUN

```
FLASK_APP=src/app.py flask run
```

# API

- `[GET] /network_status`
- `[GET] /blockchain_status`
- `[GET] /wallet_address`
- `[GET] /nodes`
- `[POST] /node`
- `[GET] /token_validation_key`
- `[POST] /check_transaction_status`
- `[POST] /token`
