# Under MIT License, see LICENSE.txt

from math import cos, sin, atan2, sqrt

__author__ = 'RoboCupULaval'


class FieldCircularArc:
    def __init__(self, protobuf_arc):
        self.center = (protobuf_arc.center.x,
                       protobuf_arc.center.y)
        self.radius      = protobuf_arc.radius
        self.angle_start = protobuf_arc.a1 # Counter clockwise order
        self.angle_end  = protobuf_arc.a2
        self.thickness   = protobuf_arc.thickness
class FieldLineSegment:
    def __init__(self, protobuf_line):
        self.p1 = (protobuf_line.p1.x, protobuf_line.p1.y)
        self.p2 = (protobuf_line.p2.x, protobuf_line.p2.y)
        self.length = sqrt(protobuf_line.p1.x**2 + protobuf_line.p1.y**2)
        self.thickness = protobuf_line.thickness

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
        self.marge = 250 # C'est quoi ca??
        self._ratio_field_mobs = 1 # C'est quoi ca??
        # TODO (pturgeon): Utiliser les dimensions de compétition en commentaires ci-dessous
        self._line_width = 10
        self._field_length = 9000
        self._field_width = 6000
        # self._boundary_width = 250
        # self._referee_width = 425
        self._goal_width = 1000
        self._goal_depth = 200
        # self._goal_wall_width = 20
        self._center_circle_radius = 500
        self._defense_radius = 1000
        self._defense_stretch = 500
        # self._free_kick_from_defense_dist = 200
        self._penalty_spot_from_field_line_dist = 750 # Dist. d'un penality kick de la ligne du fond de terrain
        self._penalty_line_from_spot_dist = 400 # limite derrière le penality kick pour les autres robots

    @property
    def line_width(self):
        return self._line_width

    @property
    def penalty_spot_from_field_line_dist(self):
        return self._penalty_spot_from_field_line_dist

    @property
    def penalty_line_from_spot_dist(self):
        return self._penalty_line_from_spot_dist

    @property
    def field_length(self):
        return self._field_length

    @property
    def field_width(self):
        return self._field_width

    @property
    def center_circle_radius(self):
        return self._center_circle_radius

    @property
    def defense_radius(self):
        return self._defense_radius

    @property
    def defense_stretch(self):
        return self._defense_stretch

    @property
    def goal_width(self):
        return self._goal_width

    @property
    def goal_depth(self):
        return self._goal_depth

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
        x = (x + self.field_length / 2 + self.marge) * self.ratio_screen + self._camera_position[0]
        y = (y + self.field_width / 2 + self.marge) * self.ratio_screen + self._camera_position[1]
        return x, y, atan2(rot_y, rot_x)

    def convert_screen_to_real_pst(self, x, y):
        """ Convertir les coordonnées du terrain en coordonnées réelles """
        x_2 = (x - self._camera_position[0]) / self.ratio_screen - self.field_length / 2 - self.marge
        y_2 = (y - self._camera_position[1]) / self.ratio_screen - self.field_width / 2 - self.marge
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
        return self.field_length * self.ratio_screen, self.field_width * self.ratio_screen

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
        if len(field.field_lines) == 0:
            raise RuntimeError("Receiving legacy geometry message instead of the new geometry message. Update your grsim or check your vision port.")
        self._set_field_size_new(field)

    def _set_field_size_legacy(self, field):
        self._line_width = field.line_width
        self._field_length = field.field_length
        self._field_width = field.field_width

        self._goal_width = field.goal_width
        self._goal_depth = field.goal_depth

        self._center_circle_radius = field.center_circle_radius
        self._defense_radius = field.defense_radius
        self._defense_stretch = field.defense_stretch
        
        self._penalty_spot_from_field_line_dist = field.penalty_spot_from_field_line_dist
        self._penalty_line_from_spot_dist = field.penalty_line_from_spot_dist

    def _set_field_size_new(self, field):
        self.field_lines = self._convert_field_line_segments(field.field_lines)
        self.field_arcs = self._convert_field_circular_arc(field.field_arcs)

        self._field_length = field.field_length
        self._field_width = field.field_width
        self._boundary_width = field.boundary_width

        self._goal_width = field.goal_width
        self._goal_depth = field.goal_depth

        self._center_circle_radius = self.field_arcs['CenterCircle'].radius
        self._defense_radius = self.field_arcs['RightFieldLeftPenaltyArc'].radius
        self._defense_stretch = self.field_lines['LeftPenaltyStretch'].length/2


    def _convert_field_circular_arc(self, field_arcs):
        result = {}
        for arc in field_arcs:
            result[arc.name] = FieldCircularArc(arc)
        return result

    def _convert_field_line_segments(self, field_lines):
        result = {}
        for line in field_lines:
            result[line.name] = FieldLineSegment(line)
        return result


