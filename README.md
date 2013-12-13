# Fernet

Port of [Fernet-rb](https://github.com/fernet/fernet-rb) from ruby.

Fernet allows you to easily generate and verify **HMAC based authentication
tokens** for issuing API requests between remote servers. It also **encrypts**
the message so it can be used to transmit secure data over the wire.

## Installation

pip install fernet

## Installation on Heroku

Try this buildpack which supports building the M2Cryto package: 
  https://github.com/guybowden/heroku-buildpack-python-paybox
  
## Usage

Both client and server must share a secret.

You want to encode some data in the token as well, for example, an email
address can be used to verify it on the other end.


```python
import fernet
token = fernet.generate(secret, 'scottp@heroku.com')
```

On the server side, the receiver can use this token to verify whether it's
legit:

```python
verifer = fernet.verifier(secret, token)
if verifier.valid():
    operate_on(verifier.message) # the original, decrypted message
```

### Global configuration

It's possible to configure fernet via the `Configuration` class. To do so, put
this in an initializer:

```python
# default values shown here
import fernet.Configuration
fernet.Configuration.enforce_ttl = true
fernet.Configuration.ttl         = 60
```
