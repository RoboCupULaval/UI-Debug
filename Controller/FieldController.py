# Under MIT License, see LICENSE.txt

from math import cos, sin, atan2

__author__ = 'RoboCupULaval'


class FieldController(object):
    """ La classe Field représente les informations relatives au terrain et ce qui s'y trouve """
    def __init__(self):
        self.type = 0
        self.ratio_screen = 1 / 10
        self.ratio_real = 1
        self.marge = 250
        self.size = 9000, 6000
        self.is_x_axe_flipped = False
        self.is_y_axe_flipped = True

    def convert_real_to_scene_pst(self, x, y, theta=0.0):
        rot_x = cos(theta)
        rot_y = sin(theta)
        if self.is_x_axe_flipped:
            x *= -1
            rot_x *= -1
        if self.is_y_axe_flipped:
            y *= -1
            rot_y *= -1
        x = (x + self.size[0] / 2 + self.marge) * self.ratio_screen
        y = (y + self.size[1] / 2 + self.marge) * self.ratio_screen
        return x, y, atan2(rot_y, rot_x)

    def convert_screen_to_real_pst(self, x, y):
        x = (x / self.ratio_screen - self.size[0] / 2 - self.marge)
        y = (y / self.ratio_screen - self.size[1] / 2 - self.marge)

        if self.is_x_axe_flipped:
            x *= -1
        if self.is_y_axe_flipped:
            y *= -1
        return x, y

    def flip_x_axe(self):
        # Retourne l'axe des X du terrain
        self.is_x_axe_flipped = not self.is_x_axe_flipped

    def flip_y_axe(self):
        # Retourne l'axe des Y du terrain
        self.is_y_axe_flipped = not self.is_y_axe_flipped
