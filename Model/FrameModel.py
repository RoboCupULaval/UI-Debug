# Under MIT License, see LICENSE.txt

from time import sleep
from collections import deque
from threading import Thread

from PyQt4.QtCore import *

from Communication.vision import Vision
from Communication.UDPCommunication import UDPSending, UDPReceiving
from Model.Field import Field

__author__ = 'RoboCupULaval'


class FrameModel(QAbstractItemModel):
    # TODO : Revoir le modele pour le rendre standard à Qt
    def __init__(self, parent=None):
        QAbstractItemModel.__init__(parent)
        self.parent = parent
        self.field_info = Field()
        self.receive_data_queue = deque(maxlen=100)
        self.send_data_queue = deque(maxlen=100)
        self.row_header = list()
        self.col_header = list()
        self.init_headerdata()

        self.vision = Vision()

        # Communication inter programme
        self.udp_sender = UDPSending()
        self.udp_receiver = UDPReceiving()
        self.udp_receiver.start()

        self.frame_catcher = Thread(target=self.catch_frame)
        self.frame_catcher_stop = False
        self.frame_catcher.start()

    def init_headerdata(self):
        self.row_header.append('frame')
        self.row_header.append('balls')
        self.row_header.append('robot_yellow_0')
        self.row_header.append('robot_yellow_1')
        self.row_header.append('robot_yellow_2')
        self.row_header.append('robot_yellow_3')
        self.row_header.append('robot_yellow_4')
        self.row_header.append('robot_yellow_5')
        self.row_header.append('robot_blue_0')
        self.row_header.append('robot_blue_1')
        self.row_header.append('robot_blue_2')
        self.row_header.append('robot_blue_3')
        self.row_header.append('robot_blue_4')
        self.row_header.append('robot_blue_5')

        self.col_header.append('frame_number')
        self.col_header.append('t_capture')
        self.col_header.append('t_sent')
        self.col_header.append('camera_id')
        self.col_header.append('confidence')
        self.col_header.append('x')
        self.col_header.append('y')
        self.col_header.append('z')
        self.col_header.append('orientation')
        self.col_header.append('pixel_x')
        self.col_header.append('pixel_y')

    def catch_frame(self):
        while not self.frame_catcher_stop:
            frame = self.vision.get_latest_frame()
            if frame is None:
                continue
            if len(self.receive_data_queue) == 0 or not frame.detection.frame_number == self.receive_data_queue[-1].detection.frame_number:
                self.receive_data_queue.append(frame)
            sleep(0.001)
        print('@model.catch_frame: stopped')
        exit(1)

    def is_connected(self):
        if len(self.receive_data_queue) > 0:
            return True
        return False

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.col_header)

    def rowCount(self, parent=None, *args, **kwargs):
        # TODO : Faire algo de comptage dynamique en fonction du contenu des frames
        return len(self.row_header)

    def data(self, index, int_role=None):
        # TODO : Rendre dynamique les données (dans le cas de Vanish)
        if index.row() >= self.rowCount():
            return None

        if index.row() == 0:
            if index.col() == 0:
                return self.receive_data_queue[-1].detection.frame_number
            elif index.col() == 1:
                return self.receive_data_queue[-1].detection.t_capture
            elif index.col() == 2:
                return self.receive_data_queue[-1].detection.t_sent
            elif index.col() == 3:
                return self.receive_data_queue[-1].detection.camera_id
            else:
                return None
        elif index.row() == 1:
            if index.col() == 4:
                return self.receive_data_queue[-1].detection.balls.confidence
            elif index.col() == 5:
                return self.receive_data_queue[-1].detection.balls[0].x
            elif index.col() == 6:
                return self.receive_data_queue[-1].detection.balls[0].y
            elif index.col() == 7:
                return self.receive_data_queue[-1].detection.balls.z
            elif index.col() == 9:
                return self.receive_data_queue[-1].detection.balls.pixel_x
            elif index.col() == 10:
                return self.receive_data_queue[-1].detection.balls.pixel_y
            else:
                return None
        elif 2 <= index.row() < 8:
            if not index.row() - 2 == self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].robot_id:
                raise IndexError
            if index.col() == 4:
                return self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].confidence
            elif index.col() == 5:
                return self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].x
            elif index.col() == 6:
                return self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].y
            elif index.col() == 7:
                return self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].z
            elif index.col() == 8:
                return self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].orientation
            elif index.col() == 9:
                return self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].pixel_x
            elif index.col() == 10:
                return self.receive_data_queue[-1].detection.robots_yellow[index.row() - 2].pixel_y
            else:
                return None
        elif 8 <= index.row() <= 13:
            if not index.row() - 8 == self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].robot_id:
                raise IndexError
            if index.col() == 4:
                return self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].confidence
            elif index.col() == 5:
                return self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].x
            elif index.col() == 6:
                return self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].y
            elif index.col() == 7:
                return self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].z
            elif index.col() == 8:
                return self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].orientation
            elif index.col() == 9:
                return self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].pixel_x
            elif index.col() == 10:
                return self.receive_data_queue[-1].detection.robots_blue[index.row() - 8].pixel_y
            else:
                return None
        else:
            return None

    def add_target(self, p_x, p_y):
        position = p_x, p_y
        if not len(self.send_data_queue) or not position == self.send_data_queue[-1]:
            self.send_data_queue.append(position)
            self.udp_sender.send_message(self.send_data_queue[-1])

    def quit(self):
        self.frame_catcher_stop = True
        self.udp_receiver.stop()


class MyModelIndex(object):
    # WARN: Classe temporaire le temps de modifier le modèle
    def __init__(self, row, column):
        self._row = row
        self._column = column

    def row(self):
        return self._row

    def col(self):
        return self._column

    def isValid(self):
        if not isinstance(self._row, int) and 0 < self._row:
            return False
        elif not isinstance(self._column, int) and 0 < self._row:
            return False
        else:
            return True
