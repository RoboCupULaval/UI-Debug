# Under MIT License, see LICENSE.txt

from math import cos, sin, atan2

__author__ = 'RoboCupULaval'


class FieldController(object):
    """ La classe Field représente les informations relatives au terrain et ce qui s'y trouve """
    def __init__(self):
        self.type = 0
        self.camera_position = [0, 0]
        self.camera_speed = 50
        self._cursor_last_pst = None
        self.ratio_screen = 1 / 10
        self.ratio_field_mobs = 1
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
        x = (x + self.size[0] / 2 + self.marge) * self.ratio_screen + self.camera_position[0]
        y = (y + self.size[1] / 2 + self.marge) * self.ratio_screen + self.camera_position[1]
        return x, y, atan2(rot_y, rot_x)

    def convert_screen_to_real_pst(self, x, y):
        x_2 = (x - self.camera_position[0]) / self.ratio_screen - self.size[0] / 2 - self.marge
        y_2 = (y - self.camera_position[1]) / self.ratio_screen - self.size[1] / 2 - self.marge
        if self.is_x_axe_flipped:
            x_2 *= -1
        if self.is_y_axe_flipped:
            y_2 *= -1
        return x_2, y_2

    def flip_x_axe(self):
        # Retourne l'axe des X du terrain
        self.is_x_axe_flipped = not self.is_x_axe_flipped

    def flip_y_axe(self):
        # Retourne l'axe des Y du terrain
        self.is_y_axe_flipped = not self.is_y_axe_flipped

    def get_top_left_to_screen(self):
        x = self.marge * self.ratio_screen + self.camera_position[0]
        y = self.marge * self.ratio_screen + self.camera_position[1]
        return x, y

    def get_size_to_screen(self):
        return self.size[0] * self.ratio_screen, self.size[1] * self.ratio_screen

    def drag_camera(self, x, y):
        if self._cursor_last_pst is None:
            self._cursor_last_pst = x, y
        else:
            real_cam_speed = self.camera_speed / self.ratio_screen
            move_x = self._cursor_last_pst[0] - x
            move_y = self._cursor_last_pst[1] - y
            if move_x < -real_cam_speed:
                move_x = -real_cam_speed
            if move_x > real_cam_speed:
                move_x = real_cam_speed
            if move_y < -real_cam_speed:
                move_y = -real_cam_speed
            if move_y > real_cam_speed:
                move_y = real_cam_speed
            self.camera_position[0] -= move_x
            self.camera_position[1] -= move_y
            self._cursor_last_pst = x, y
            self._limit_camera()

    def _limit_camera(self):
        self.camera_position[0] = min(self.camera_position[0], self.size[0] * self.ratio_screen)
        self.camera_position[1] = min(self.camera_position[1], self.size[1] * self.ratio_screen)
        self.camera_position[0] = max(self.camera_position[0], -self.size[0] * self.ratio_screen)
        self.camera_position[1] = max(self.camera_position[1], -self.size[1] * self.ratio_screen)

    def zoom(self):
        self.ratio_screen *= 1.10

    def dezoom(self):
        self.ratio_screen *= 0.90
