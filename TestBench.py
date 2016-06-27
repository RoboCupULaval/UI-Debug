# Under MIT License, see LICENSE.txt

from random import randint
from time import time
from Communication.UDPCommunication import UDPSending

__author__ = 'RoboCupULaval'


def create_basic_pkg():
    pkg = {'name': 'tester',
           'version': '1.0',
           'type': None,
           'link': None,
           'data': dict()
           }
    return pkg


def test_multiple_lines():
    pkg = create_basic_pkg()
    pkg['type'] = 3002
    pkg['data']['points'] = list()
    var1 = randint(-3000, 1000)
    var2 = randint(-3000, 1000)
    for _ in range(10):
        pkg['data']['points'].append(tuple([var1 + randint(-300, 300), var2 + randint(-300, 300)]))
        var1 += randint(150, 500)
        var2 += randint(150, 500)
    pkg['data']['style'] = 'DashLine'
    pkg['data']['width'] = 2
    pkg['data']['color'] = randint(0, 255), randint(0, 255), randint(0, 255)
    ex.send_message(pkg)


def test_line():
    """ Line """
    pkg = create_basic_pkg()
    pkg['type'] = 3001
    pkg['data']['start'] = randint(-3000, 3000), randint(-3000, 3000)
    pkg['data']['end'] = randint(-3000, 3000), randint(-3000, 3000)
    pkg['data']['style'] = 'DashLine'
    pkg['data']['width'] = 2
    pkg['data']['color'] = randint(0, 255), randint(0, 255), randint(0, 255)
    ex.send_message(pkg)


def test_influence_map():
    """ InfluenceMapTest"""
    pkg = create_basic_pkg()
    pkg['type'] = 3007
    pkg['data']['field_data'] = [[x + y for x in range(20)] for y in range(15)]
    pkg['data']['hottest_color'] = 255, 0, 0
    pkg['data']['coldest_color'] = 0, 255, 0
    pkg['data']['has_grid'] = True
    pkg['data']['grid_width'] = 1
    pkg['data']['grid_color'] = 255, 255, 255
    pkg['data']['grid_style'] = 'DashLine'
    pkg['data']['opacity'] = 10
    ex.send_message(pkg)


def test_circle():
    """ Circle """
    pkg = create_basic_pkg()
    pkg['type'] = 3003
    pkg['data']['center'] = randint(-4500, 4500), randint(-3000, 3000)
    pkg['data']['radius'] = randint(100, 600)
    pkg['data']['color'] = randint(0, 255), randint(0, 255), randint(0, 255)
    pkg['data']['style'] = 'SolidLine'
    pkg['data']['is_fill'] = True
    ex.send_message(pkg)


if __name__ == '__main__':
    ex = UDPSending(port=20021)

    # test_influence_map()
    # test_line()
    # test_multiple_lines()
    for _ in range(10):
        test_circle()
        test_multiple_lines()
        test_line()

    test_influence_map()
