# Under MIT License, see LICENSE.txt

from random import randint
from time import time, sleep
from Communication.UDPCommunication import UDPSending

__author__ = 'RoboCupULaval'

ex = UDPSending(port=20021)

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
    pkg['data']['timeout'] = randint(2, 10)
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
    pkg['data']['timeout'] = randint(2, 10)
    pkg['data']['color'] = randint(0, 255), randint(0, 255), randint(0, 255)
    ex.send_message(pkg)


def test_influence_map():
    """ InfluenceMapTest"""
    pkg = create_basic_pkg()
    pkg['type'] = 3007
    pkg['data']['field_data'] = [[randint(0, 100) for x in range(120)] for y in range(180)]
    pkg['data']['hottest_color'] = 255, 0, 0
    pkg['data']['coldest_color'] = 0, 255, 0
    pkg['data']['has_grid'] = False
    pkg['data']['grid_width'] = 1
    pkg['data']['grid_color'] = 255, 255, 255
    pkg['data']['grid_style'] = 'SolidLine'
    pkg['data']['opacity'] = 10
    pkg['data']['timeout'] = randint(2, 10)
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
    pkg['data']['timeout'] = randint(2, 10)
    ex.send_message(pkg)


def test_rect():
    """ Rectangle """
    pkg = create_basic_pkg()
    pkg['type'] = 3006
    pkg['data']["top_left"] = randint(-3000, 3000), randint(-3000, 3000)
    pkg['data']["bottom_right"] = pkg['data']["top_left"][0] + randint(100, 1000),pkg['data']["top_left"][1] + randint(100, 1000)
    pkg['data']['color'] = randint(0, 255), randint(0, 255), randint(0, 255)
    pkg['data']['is_fill'] = True
    pkg['data']['timeout'] = randint(2, 10)
    ex.send_message(pkg)


def test_point():
    """ Point """
    pkg = create_basic_pkg()
    pkg['type'] = 3004
    pkg['data']["point"] = randint(-3000, 3000), randint(-3000, 3000)
    pkg['data']['color'] = randint(0, 255), randint(0, 255), randint(0, 255)
    pkg['data']['timeout'] = randint(2, 10)
    ex.send_message(pkg)


def test_multiple_points():
    """ Point """
    pkg = create_basic_pkg()
    pkg['type'] = 3005
    pkg['data']["points"] = [tuple([randint(-3000, 3000), randint(-3000, 3000)]) for _ in range(5)]
    pkg['data']['color'] = randint(0, 255), randint(0, 255), randint(0, 255)
    pkg['data']['width'] = randint(2, 5)
    pkg['data']['timeout'] = randint(2, 10)
    ex.send_message(pkg)


def test_strat():
    pkg = create_basic_pkg()
    pkg['type'] = 1001
    pkg['data']['strategy'] = ['Start1', 'Start2']
    pkg['data']['tactic'] = ['Tact1', 'Tact2']
    ex.send_message(pkg)


def test_text(msg=''):
    pkg = create_basic_pkg()
    pkg['type'] = 2
    pkg['data']['level'] = 2
    pkg['data']['message'] = 'HelloWorld' + msg
    ex.send_message(pkg)


def stress_test():
    """
        Test tous les paquest :
        /!\ Éviter de tester l'influenceMap en même temps que le reste /!\
    """
    for _ in range(5):
        #test_influence_map()
        test_circle()
        test_multiple_lines()
        test_line()
        test_rect()
        test_point()
        test_multiple_points()
        test_tree()


def test_tree():
    pkg = create_basic_pkg()
    pkg['type'] = 3009
    pkg['data']['timeout'] = 5
    pkg['data']['tree'] = [((0, 0), (100, 100)),
                           ((100, 100), (200, 100)),
                           ((100, 100), (100, 150))]
    ex.send_message(pkg)

if __name__ == '__main__':
    # stress_test()
    test_tree()

