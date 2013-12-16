# Note: test_verify.py will fail on a token with bad padding if using Pycrypto instead
# of M2Crypto.

python -m unittest discover -s test
