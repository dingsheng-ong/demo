"""
Create `config` object corresponding to specified `FLASK_ENV` in the environment.
You can use:-

    $ export FLASK_ENV=<value>
to specify the environment. The available options are:
- `development`
- `test`

All the configurations are defined in demo.config.config, and the environment
specific configurations are defined in `demo.config.config.developmentConfig` and
`demo.config.config.testConfig` respectively.

One can change the value by either modifying the `demo/config/config.py` file, or
using an environment variable to overwrite the value.
"""
from demo.config import config
import os
import sys

FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
assert FLASK_ENV in ('development', 'test'), f'Unknown FLASK_ENV: "{FLASK_ENV}"'

_config = eval(f'config.{FLASK_ENV}Config')()

for attr in filter(lambda f: not '__' in f, dir(_config)):
    value = os.environ.get(attr, getattr(_config, attr))
    setattr(sys.modules[__name__], attr, value)

# delete not relevant attributes
del _config, attr, config, os, sys, value