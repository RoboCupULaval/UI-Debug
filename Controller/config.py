from collections import namedtuple

FieldParameter = namedtuple('FieldParameter', ['field_width', 'field_height', 'goal_width', 'goal_height',
                                               'goalzone_radius', 'goalzone_height', 'center_radius', 'field_ratio'])

config = FieldParameter(9000, 6000, 200, 1000, 500, 1000, 500, 1)


def set_simulation():
    pass


def set_real_life():
    global config
    field_width = 3272
    field_height = 2181
    goal_width = 72
    goal_height = 363
    goalzone_rayon = 363
    goalzone_height = 363
    center_radius = 181
    field_ratio = 1
    config = FieldParameter(field_width, field_height, goal_width, goal_height, goalzone_rayon, goalzone_height,
                            center_radius, field_ratio)


config_dispatch = {'simulation': set_simulation,
                   'real-life': set_real_life}


def set_config(mode="simulation"):
    config_dispatch[mode]()
