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
    pkg['data']['field_data'] = [[x+y for x in range(5)] for y in range(5)]
    ex.send_message(pkg)
    '''
    x = 0
    x_ecart = 10
    t_ref = time()
    while True:
        if time() - t_ref > 0.002:
            pkg['data']['start'] = 0, -3000 + x
            pkg['data']['end'] = 1000, -3000 + x
            ex.send_message(pkg)
            t_ref = time()
            x += x_ecart
        if x == 600 * x_ecart:
            print('TOTAL', time()-t_ref)
            break
            '''
