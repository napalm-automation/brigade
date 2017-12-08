import ast
import os


import yaml


CONF = {
    'num_workers': {
        'description': 'Number of Brigade worker processes',
        'type': 'int',
        'default': 20,
    },
    'raise_on_error': {
        'description': "If set to ``True``, (:obj:`brigade.core.Brigade.run`) method of will raise "
                       "an exception if at least a host failed.",
        'type': 'bool',
        'default': True,
    },
    'ssh_config_file': {
        'description': 'User ssh_config_file',
        'type': 'str',
        'default': os.path.join(os.path.expanduser("~"), ".ssh", "config"),
        'default_doc': '~/.ssh/config'
    },
}

types = {
    'int': int,
    'str': str
}


class Config:
    """
    Documentation

    """

    def __init__(self, config_file=None):

        if config_file:
            with open(config_file, 'r') as f:
                c = yaml.load(f.read())
        else:
            c = {}

        self._assign_properties(c)

    def _assign_properties(self, c):

        for p in CONF:
            env = CONF[p].get('env') or 'BRIGADE_' + p.upper()
            print(env)
            if CONF[p]['type'] == 'bool':
                if os.environ.get(env) is not None:
                    v = os.environ.get(env)
                elif c.get(p) is not None:
                    v = c.get(p)
                else:
                    v = CONF[p]['default']
                v = ast.literal_eval(str(v).title())
            else:
                v = os.environ.get(env) or c.get(p) or CONF[p]['default']
                v = types[CONF[p]['type']](v)
            setattr(self, p, v)