# Under MIT License, see LICENSE.txt

from math import cos, sin, atan2
from .config import *

__author__ = 'RoboCupULaval'


class FieldController(object):
    """ La classe Field représente les informations relatives au terrain et ce qui s'y trouve """
    def __init__(self):
        self.type = 0

        # Paramètre caméra
        self._camera_position = [0, 0]
        self._camera_speed = 50
        self._cursor_last_pst = None
        self._lock_camera = False

        # Paramètre fenètre
        self.ratio_screen = 1 / 10
        self.is_x_axe_flipped = False
        self.is_y_axe_flipped = True

        # Dimension du terrain
        # TODO - Faire que ces paramètres soient paramétrables depuis le GUI
        self.marge = 250 # C'est quoi ca??
        self._ratio_field_mobs = 1 # C'est quoi ca??
        # TODO : Utiliser les dimensions en commentaires ci-dessous
        # self.line_width = 10
        self.field_length = 9000
        self.field_width = 6000
        # self.boundary_width = 300
        # self.referee_width = 400
        self.goal_width_ = 1000
        self.goal_depth = 180
        # self.goal_wall_width = 20
        self.center_circle_radius = 1000
        self.defense_radius_ = 1000
        self.defense_stretch_ = 500
        # self.free_kick_from_defense_dist = 700
        # self.penalty_spot_from_field_line_dist = 450
        # self.penalty_line_from_spot_dist = 350

        self.field_size = [self.field_length, self.field_width]
        self.goal_size = [self.goal_depth, self.goal_width_]



    @property
    def width(self):
        return self.field_size[0]

    @property
    def height(self):
        return self.field_size[1]

    @property
    def center_radius(self):
        return self.center_circle_radius

    @property
    def defense_radius(self):
        return self.defense_radius_

    @property
    def defense_stretch(self):
        return self.defense_stretch_

    @property
    def goal_width(self):
        return self.goal_size[0]

    @property
    def goal_height(self):
        return self.goal_size[1]

    @property
    def ratio_field_mobs(self):
        return self._ratio_field_mobs

    @ratio_field_mobs.setter
    def ratio_field_mobs(self, new_ratio):
        self._ratio_field_mobs = new_ratio

    def convert_real_to_scene_pst(self, x, y, theta=0.0):
        """ Convertit les coordonnées réelles en coordonnées du terrain """
        rot_x = cos(theta)
        rot_y = sin(theta)
        if self.is_x_axe_flipped:
            x *= -1
            rot_x *= -1
        if self.is_y_axe_flipped:
            y *= -1
            rot_y *= -1
        x = (x + self.field_size[0] / 2 + self.marge) * self.ratio_screen + self._camera_position[0]
        y = (y + self.field_size[1] / 2 + self.marge) * self.ratio_screen + self._camera_position[1]
        return x, y, atan2(rot_y, rot_x)

    def convert_screen_to_real_pst(self, x, y):
        """ Convertir les coordonnées du terrain en coordonnées réelles """
        x_2 = (x - self._camera_position[0]) / self.ratio_screen - self.field_size[0] / 2 - self.marge
        y_2 = (y - self._camera_position[1]) / self.ratio_screen - self.field_size[1] / 2 - self.marge
        if self.is_x_axe_flipped:
            x_2 *= -1
        if self.is_y_axe_flipped:
            y_2 *= -1
        return x_2, y_2

    def flip_x_axe(self):
        """ Retourne l'axe des X du terrain """
        self.is_y_axe_flipped = not self.is_y_axe_flipped

    def flip_y_axe(self):
        """ Retourne l'axe des Y du terrain """
        self.is_x_axe_flipped = not self.is_x_axe_flipped

    def get_top_left_to_screen(self):
        """ Donne la position à l'écran du terrain en haut à gauche """
        x = self.marge * self.ratio_screen + self._camera_position[0]
        y = self.marge * self.ratio_screen + self._camera_position[1]
        return x, y

    def get_size_to_screen(self):
        """ Donne la taille du terrain sur l'écran """
        return self.field_size[0] * self.ratio_screen, self.field_size[1] * self.ratio_screen

    def drag_camera(self, x, y):
        """ Déplacement de la caméra """
        if not self._lock_camera:
            if self._cursor_last_pst is None:
                self._cursor_last_pst = x, y
            else:
                real_cam_speed = self._camera_speed / self.ratio_screen
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
                self._camera_position[0] -= move_x
                self._camera_position[1] -= move_y
                self._cursor_last_pst = x, y
                self._limit_camera()

    def _limit_camera(self):
        """ Limite le déplacement de la caméra à la taille du terrain """
        max_width, max_height = self.get_size_to_screen()
        self._camera_position[0] = min(self._camera_position[0], max_width)
        self._camera_position[1] = min(self._camera_position[1], max_height)
        self._camera_position[0] = max(self._camera_position[0], -max_width)
        self._camera_position[1] = max(self._camera_position[1], -max_height)

    def zoom(self):
        """ Zoom la caméra de +10% """
        if not self._lock_camera:
            self.ratio_screen *= 1.10

    def dezoom(self):
        """ Dézoom la caméra de -10% """
        if not self._lock_camera:
            self.ratio_screen *= 0.90

    def toggle_lock_camera(self):
        """ Débloque/Bloque le mouvement et le zoom de la caméra """
        self._lock_camera = not self._lock_camera

    def camera_is_locked(self):
        """ Interroge pour savoir si la caméra est bloquée ou non """
        return self._lock_camera

    def reset_camera(self):
        """ Réinitialise la position et le zoom de la caméra par défaut """
        self._camera_position = (0, 0)
        self.ratio_screen = 1 / 10

    def set_field_size(self, field):
        """ Ajuste les dimensions du terrain """

        # TODO : Utiliser les dimensions en commentaires ci-dessous
        # self.line_width = field.line_width
        self.field_length = field.field_length
        self.field_width = field.field_width
        # self.boundary_width = field.boundary_width
        # self.referee_width = field.referee_width
        self.goal_width_ = field.goal_width
        self.goal_depth = field.goal_depth
        #self.goal_wall_width = field.goal_wall_width
        self.center_circle_radius = field.center_circle_radius
        self.defense_radius_ = field.defense_radius
        self.defense_stretch_ = field.defense_stretch
        # self.free_kick_from_defense_dist = field.free_kick_from_defense_dist
        # self.penalty_spot_from_field_line_dist = field.penalty_spot_from_field_line_dist
        # self.penalty_line_from_spot_dist = field.penalty_line_from_spot_dist

        self.field_size = [self.field_length, self.field_width]
        self.goal_size = [self.goal_depth, self.goal_width_]


