# Under MIT License, see LICENSE.txt
import logging
from time import time

from PyQt5.QtCore import Qt, pyqtSignal, QMutex, QTimer, QEvent
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter

from Controller.QtToolBox import QtToolBox
from Controller.DrawingObject.InfluenceMapDrawing import InfluenceMapDrawing
from Controller.DrawingObject.MultiplePointsDrawing import MultiplePointsDrawing

__author__ = 'RoboCupULaval'


class FieldView(QWidget):
    """
    FieldView est un QWidget qui représente la vue du terrain et des éléments qui y sont associés.
    """
    frame_rate = 30
    vanishing_delay = 0.0

    def __init__(self, controller, debug=False):
        super().__init__(controller)
        self._logger = logging.getLogger(FieldView.__name__)
        if debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
        self.tool_bar = QToolBar(self)
        self.controller = controller
        self.last_frame = 0
        self.graph_mobs = dict()
        self.vanishing_memory = dict()
        self.graph_draw = dict()
        self.draw_filterable = dict()
        self.list_filter = ['None']
        self.graph_map = None
        self.multiple_points_map = dict()
        self.setCursor(Qt.OpenHandCursor)

        # Option
        self.option_vanishing = False
        self.option_show_vector = False
        self.option_target_mode = False

        # Targeting
        self.last_target = None
        self._cursor_position = 0, 0

        # Thread Core
        self._mutex = QMutex()
        self.timer_screen_update = QTimer()

        # Frame
        self._real_frame_rate = 0
        self._real_frame_rate_last_time = time()

        # Initialisation de l'interface
        self.init_window()
        self.init_graph_mobs()
        self.init_view_event()
        self.init_tool_bar()
        self._init_logger()
        self.show()

    def init_view_event(self):
        """ Initialise les boucles de rafraîchissement des dessins """
        self.timer_screen_update.timeout.connect(self.emit_painting_signal)
        self.timer_screen_update.start((1 / self.frame_rate) * 1000)

    def init_window(self):
        """ Initialisation de la fenêtre du widget qui affiche le terrain"""
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def init_tool_bar(self):
        """ Initialisation de la barre d'outils de la vue du terrain """
        self.tool_bar.setOrientation(Qt.Horizontal)

        self._action_lock_camera = QAction(self)
        self._action_lock_camera.triggered.connect(self.toggle_lock_camera)
        #self.toggle_lock_camera()
        self.tool_bar.addAction(self._action_lock_camera)

        self._action_delete_draws = QAction(self)
        self._action_delete_draws.setToolTip('Effacer tous les dessins')
        self._action_delete_draws.setIcon(QIcon('Img/map_delete.png'))
        self._action_delete_draws.triggered.connect(self.delete_all_draw)
        self.tool_bar.addAction(self._action_delete_draws)

    def _init_logger(self):
        """ Initialisation du logger """
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.debug('INIT: Logger')

    def emit_painting_signal(self):
        """ Émet un signal pour bloquer les ressources et afficher les éléments """
        #self._emit_signal.emit()
        self.update()

    def timeout_handler(self):
        """ Gère la durée d'affichage des éléments avec le timeout de ces derniers """
        ref_time = time()
        if self.graph_map is not None and self.graph_map.time_is_up(ref_time):
            self.graph_map = None
        for key, value in self.multiple_points_map.items():
            if value.time_is_up(ref_time):
                del self.multiple_points_map[key]

        for key, list_effects in self.draw_filterable.items():
            temp_list_draw = []
            for effect in list_effects:
                if not effect.time_is_up(ref_time):
                    temp_list_draw.append(effect)
            self.draw_filterable[key] = temp_list_draw

    def draw_map(self, painter):
        """ Dessine une InfuenceMap unique """
        if self.graph_map is not None and 'None' in self.list_filter:
            self.graph_map.draw(painter)

    def draw_multiple_points(self, painter):
        """ Dessine une série de points unique """
        for key, value in self.multiple_points_map.items():
            self._logger.debug('Valeur de la cle envoyer: {}, type {}'.format(key, type(key)))
            if str(key) in self.list_filter:
                value.draw(painter)

    def draw_field_lines(self, painter):
        """ Dessine les lignes du terrains """
        self.graph_draw['field-lines'].draw(painter)
        self.graph_draw['frame-rate'].draw(painter, self._real_frame_rate)

    def draw_effects(self, painter):
        """ Dessine les effets """
        for key, list_effect in self.draw_filterable.items():
            if key in self.list_filter:
                for effect in list_effect:
                    effect.draw(painter)

    def draw_field_ground(self, painter):
        """ Dessine le sol du terrain """
        self.graph_draw['field-ground'].draw(painter)

    def draw_mobs(self, painter):
        """ Dessine les objets mobiles """
        self.graph_mobs['ball'].draw(painter)
        self.graph_mobs['target'].draw(painter)
        for mob in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            mob.draw(painter)

    def toggle_lock_camera(self):
        """ Déverrouille/Verrouille la position et le zoom de la caméra """
        QtToolBox.field_ctrl.toggle_lock_camera()
        if QtToolBox.field_ctrl.camera_is_locked():
            self.setCursor(Qt.ArrowCursor)
            self._action_lock_camera.setIcon(QIcon('Img/lock.png'))
            self._action_lock_camera.setToolTip('Déverrouiller caméra')
        else:
            self.setCursor(Qt.OpenHandCursor)
            self._action_lock_camera.setIcon(QIcon('Img/lock_open.png'))
            self._action_lock_camera.setToolTip('Verrouiller caméra')

    def toggle_frame_rate(self):
        """ Afficher/Cacher la fréquence de rafraîchissement de l'écran """
        if self.graph_draw['frame-rate'].isVisible():
            self.graph_draw['frame-rate'].hide()
        else:
            self.graph_draw['frame-rate'].show()

    def reset_camera(self):
        """ Réinitialise la position et le zoom de la caméra """
        QtToolBox.field_ctrl.reset_camera()

    def init_graph_mobs(self):
        """ Initialisation des objets graphiques """
        max_robots_in_team = 12   # TODO : Variable globale?

        # Élément graphique pour les dessins
        self.graph_draw['field-ground'] = self.controller.get_drawing_object('field-ground')()
        self.graph_draw['field-ground'].show()
        self.graph_draw['field-lines'] = self.controller.get_drawing_object('field-lines')()
        self.graph_draw['field-lines'].show()
        self.graph_draw['frame-rate'] = self.controller.get_drawing_object('frame-rate')()
        self.graph_draw['frame-rate'].hide()
        self.graph_draw['robots_yellow'] = [list() for _ in range(max_robots_in_team)]
        self.graph_draw['robots_blue'] = [list() for _ in range(max_robots_in_team)]

        self.vanishing_memory['ball'] = 0
        self.vanishing_memory['robots_yellow'] = [0 for _ in range(max_robots_in_team)]
        self.vanishing_memory['robots_blue'] = [0 for _ in range(max_robots_in_team)]

        # Élément mobile graphique (Robots, balle et cible)
        self.graph_mobs['ball'] = self.controller.get_drawing_object('ball')()

        self.graph_mobs['robots_yellow'] = [self.controller.get_drawing_object('robot')(x, 'yellow')
                                            for x in range(max_robots_in_team)]
        self.graph_mobs['robots_blue'] = [self.controller.get_drawing_object('robot')(x, 'blue')
                                          for x in range(max_robots_in_team)]


        self.graph_mobs['target'] = self.controller.get_drawing_object('target')()
        # TODO : show // init setters

    def delete_all_draw(self):
        """ Efface tous les dessins enregistrés """
        self.graph_map = None
        self.draw_filterable = dict()
        self.multiple_points_map = dict()

    def set_ball_pos(self, x, y):
        """ Modifie la position de la balle sur la fenêtre du terrain """
        if not self.graph_mobs['ball'].getX() == x and not self.graph_mobs['ball'].getY() == y:
            self.graph_mobs['ball'].setPos(x, y)
        self.graph_mobs['ball'].show()

    def set_bot_pos(self, bot_id, team_color, x, y, theta):
        """ Modifie la position et l'orientation d'un robot sur la fenêtre du terrain """
        if team_color =='yellow':
            self.graph_mobs['robots_yellow'][bot_id].setPos(x, y)
            self.graph_mobs['robots_yellow'][bot_id].setRotation(theta)
        elif team_color == 'blue':
            self.graph_mobs['robots_blue'][bot_id].setPos(x, y)
            self.graph_mobs['robots_blue'][bot_id].setRotation(theta)
        self.show_bot(bot_id, team_color)

    def set_target_pos(self, x, y):
        """ Modifie la position de la cible """
        self.graph_mobs['target'].setPos(x, y)

    def hide_ball(self):
        """ Cache la balle dans la fenêtre de terrain """
        if (time() - self.vanishing_memory['ball']) >= self.vanishing_delay:
            self.graph_mobs['ball'].hide()
            self.vanishing_memory['ball'] = time()

    def hide_bot(self, bot_id, team_color):
        """ Cache un robot dans la fenêtre de terrain """
        if team_color =='yellow' and\
                (time() - self.vanishing_memory['robots_yellow'][bot_id]) >= self.vanishing_delay:
            self.graph_mobs['robots_yellow'][bot_id].hide()
            self.vanishing_memory['robots_yellow'][bot_id] = time()
        elif team_color == 'blue'and\
                (time() - self.vanishing_memory['robots_blue'][bot_id]) >= self.vanishing_delay:
            self.graph_mobs['robots_blue'][bot_id].hide()
            self.vanishing_memory['robots_blue'][bot_id] = time()

    def show_ball(self):
        """ Affiche la balle dans la fenêtre de terrain """
        self.graph_mobs['ball'].show()
        self.vanishing_memory['ball'] = time()

    def show_bot(self, bot_id, team_color):
        """ Affiche un robot dans la fenêtre du terrain """
        if team_color == 'yellow':
            self.graph_mobs['robots_yellow'][bot_id].show()
            self.vanishing_memory['robots_yellow'][bot_id] = time()
        elif team_color == 'blue':
            self.graph_mobs['robots_blue'][bot_id].show()
            self.vanishing_memory['robots_blue'][bot_id] = time()

    def show_number_option(self):
        """ Affiche les numéros des robots """
        for mob in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            if mob.number_isVisible():
                mob.hide_number()
            else:
                mob.show_number()

    def deselect_all_robots(self):
        for mob in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            mob.deselect()

    def select_robot(self, bot_id, team_color):
        for i, mob in enumerate(self.graph_mobs['robots_yellow'] if team_color == 'yellow' else self.graph_mobs['robots_blue']):
            if i == bot_id:
                mob.select()
            else:
                mob.deselect()

    def toggle_vanish_option(self):
        """ Active/Désactive l'option pour afficher le vanishing sur les objets mobiles """
        self.option_vanishing = not self.option_vanishing

    def toggle_vector_option(self):
        """ Active/Désactive l'option pour afficher les vecteurs de direction des robots """
        self.option_show_vector = not self.option_show_vector
        for mob in self.graph_mobs['robots_yellow'] + self.graph_mobs['robots_blue']:
            if self.option_show_vector:
                mob.show_speed_vector()
            else:
                mob.hide_speed_vector()

    def auto_toggle_visible_target(self):
        """ Met à jour la vue de la cible en fonction des onglets ouverts """
        # TODO refaire en passant par une méthode du MainController
        if self.controller.view_controller.isVisible() and self.controller.view_controller.page_tactic.isVisible():
            self.graph_mobs['target'].show()
        else:
            self.graph_mobs['target'].hide()

    def load_draw(self, draw):
        """ Charge un dessin sur l'écran """
        draw.show()
        if isinstance(draw, InfluenceMapDrawing):
            self.graph_map = draw
        elif type(draw).__name__ == MultiplePointsDrawing.__name__:
            self.multiple_points_map[draw.filter] = draw
        else:
            if draw.filter in self.draw_filterable.keys():
                self.draw_filterable[draw.filter].append(draw)
            else:
                self.draw_filterable[draw.filter] = [draw]

    def get_nearest_mob_from_position(self, x, y):
        """ Requête pour obtenir la distance, le numéro et le dessin du robot le plus près d'une position """
        nearest = []
        for id, mob in enumerate(self.graph_mobs['robots_yellow']):
            team_color = 'yellow'
            mob_x, mob_y, _ = mob.get_position_on_screen()
            distance = ((x - mob_x) ** 2 + (y - mob_y) ** 2) ** 0.5
            mob_ordered = distance, id, team_color, mob
            nearest.append(mob_ordered)

        for id, mob in enumerate(self.graph_mobs['robots_blue']):
            team_color = 'blue'
            mob_x, mob_y, _ = mob.get_position_on_screen()
            distance = ((x - mob_x) ** 2 + (y - mob_y) ** 2) ** 0.5
            mob_ordered = distance, id, team_color, mob
            nearest.append(mob_ordered)
        return min(nearest)

    def get_cursor_position(self):
        """ Récupère la position du curseur """
        return self._cursor_position

    def get_fps(self):
        """ Récupère la fréquence de rafraîchissement de l'écran """
        return self._real_frame_rate

    def eventFilter(self, source, event):
        """ Gère l'événement filtré """
        if event.type() == QEvent.MouseMove:
            self._cursor_position = event.pos().x(), event.pos().y()
        return super().eventFilter(source, event)

    def mousePressEvent(self, event):
        """ Gère l'événement du clic simple de la souris """
        if self.controller.get_tactic_controller_is_visible():
            distance, robot_id, team_color, mob = self.get_nearest_mob_from_position(event.pos().x(), event.pos().y())
            if distance < mob.get_radius() * QtToolBox.field_ctrl.ratio_screen and team_color == self.controller.get_team_color():
                self.select_robot(robot_id, team_color)
                self.controller.force_tactic_controller_select_robot(robot_id, team_color)

    def mouseDoubleClickEvent(self, event):
        """ Gère l'événement double-clic de la souris """
        if not QtToolBox.field_ctrl.camera_is_locked():
            self.setCursor(Qt.ClosedHandCursor)
        if self.controller.view_controller.isVisible() and self.controller.view_controller.page_tactic.isVisible():
            x, y = QtToolBox.field_ctrl.convert_screen_to_real_pst(event.pos().x(), event.pos().y())
            self.controller.model_dataout.target = (x, y)
            self.graph_mobs['target'].setPos(x, y)

    def mouseReleaseEvent(self, event):
        """ Gère l'événement de relâchement de la touche de la souris """
        if not QtToolBox.field_ctrl.camera_is_locked():
            self.setCursor(Qt.OpenHandCursor)
        QtToolBox.field_ctrl._cursor_last_pst = None

    def mouseMoveEvent(self, event):
        """ Gère l'événement du mouvement de la souris avec une touche enfoncée """
        if event.buttons() == Qt.LeftButton:
            if not QtToolBox.field_ctrl.camera_is_locked():
                self.setCursor(Qt.ClosedHandCursor)
            QtToolBox.field_ctrl.drag_camera(event.pos().x(), event.pos().y())

    def wheelEvent(self, event):
        """ Gère l'événement de la molette de la souris """
        if event.angleDelta().y() > 0:
            QtToolBox.field_ctrl.zoom()
        else:
            QtToolBox.field_ctrl.dezoom()

    def frame_rate_event(self):
        """ Met à jour la fréquence de rafraîchissement de l'écran """
        current_time = time()
        dt = current_time - self._real_frame_rate_last_time
        self._real_frame_rate = int(1 / dt)
        self._real_frame_rate_last_time = current_time

    def paintEvent(self, e):
        """ Gère l'événement du signal pour dessiner les éléments du terrain """
        self.frame_rate_event()
        self.timeout_handler()
        painter = QPainter()
        painter.begin(self)
        painter.setBackground(QtToolBox.create_brush())
        self.draw_field_ground(painter)
        self.draw_map(painter)
        self.draw_multiple_points(painter)
        self.draw_effects(painter)
        self.draw_field_lines(painter)
        self.draw_mobs(painter)
        painter.end()
