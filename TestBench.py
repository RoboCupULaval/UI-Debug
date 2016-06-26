# Under MIT License, see LICENSE.txt

from random import randint
from time import time
from Communication.UDPCommunication import UDPSending

__author__ = 'RoboCupULaval'

if __name__ == '__main__':
    ex = UDPSending(port=20021)
    pkg = {'name': 'tester',
           'version': '1.0',
           'type': 3007,
           'link': None,
           'data': dict()
           }
    pkg['data']['field_data'] = [[x+y for x in range(20)] for y in range(15)]
    pkg['data']['hotest_color'] = 255, 0, 0
    pkg['data']['coldest_color'] = 0, 255, 0
    pkg['data']['has_grid'] = True
    pkg['data']['grid_width'] = 1
    pkg['data']['grid_color'] = 255, 255, 255
    pkg['data']['grid_style'] = 'DashLine'
    pkg['data']['opacity'] = 10

    ex.send_message(pkg)
