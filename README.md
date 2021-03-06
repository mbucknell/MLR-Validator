# MLR-Validator
Validates inserts and updates to the MLR system

[![Build Status](https://travis-ci.org/USGS-CIDA/MLR-Validator.svg?branch=master)](https://travis-ci.org/USGS-CIDA/MLR-Validator)
[![Coverage Status](https://coveralls.io/repos/github/USGS-CIDA/MLR-Validator/badge.svg)](https://coveralls.io/github/USGS-CIDA/MLR-Validator)


This project has been built and tested with python 3.6.x. To build the project locally you will need
python 3 and virtualenv installed.
```bash
% virtualenv --python=python3 env
% env/bin/pip install -r requirements.txt
```
To run the tests:
```bash
env/bin/python -m unittest
```

To run the application locally execute the following:
```bash
% env/bin/python app.py
```

The swagger documentation can then be accessed at http://127.0.0.1:5000/api

## Configuration
Configuration is read from `config.py`. `config.py` tries to read most values from environment variables and provides defaults if they do not exist. A user running this app can customize config values by defining environment variables referenced in `config.py`.

Configuration is also read from an optional `.env` Python file. Any python variable defined in `.env` overrides values set in `config.py` For instance, though `DEBUG = False` in `config.py`, you can turn debug on by creating a `.env` file with the following:

```python
DEBUG = True
```

For local development, you will need to provide a JWT token to the service. This can be done through the Swagger 
documents by clicking the Authorize button and entering 'Bearer your.jwt.token'.

You can use a valid JWT token generated by another service. You will need to set it's JWT_PUBLIC_KEY to the public 
key used to generate the token, as well as the JWT_DECODE_AUDIENCE (if any) and the JWT_ALGORITHM 
(if different than RS256). If you don't want to verify the cert on this service, set AUTH_CERT_PATH to False.

Alternatively, you can generate your own token by using the python package jwt. In the python interpreter, do the following
```python
import jwt
jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret', algorithm='HS256')
```

The output of this command will be the token that you can use. You will need to set JWT_SECRET_KEY to 'secret' in 
your local .env file. See http://flask-jwt-simple.readthedocs.io/en/latest/options.html for the other options that 
you can use.
