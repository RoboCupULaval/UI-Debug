from collections import namedtuple


def set_simulation():
    pass


def set_real_life():
    pass


config_dispatch = {'simulation': set_simulation,
                   'real-life': set_real_life}


def set_config(mode="simulation"):
    config_dispatch[mode]()
