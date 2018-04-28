# Under MIT License, see LICENSE.txt
import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox

from PyQt5.QtCore import QTimer

import pyqtgraph as pq
from pyqtgraph import PlotWidget

import numpy as np

from Controller.DrawingObject.color import Color

__author__ = 'RoboCupULaval'


class PlotterView(QWidget):
    id_to_colors = {
        0: Color.SKY_BLUE,
        1: Color.YELLOW,
        2: Color.WHITE,
        3: Color.ORANGE,
        4: Color.RED,
        5: Color.BLUE
    }

    def __init__(self, controller=None):
        QWidget.__init__(self, controller)
        self._controller = controller

        self.model_datain = None
        self.axes = {}
        self.time_at_start = time.time()
        self.pause = False
        self.init_ui()

        # Timer
        self._timer_update = QTimer()
        self._timer_update.timeout.connect(self.update_plotter)
        self._timer_update.start(100)


    def init_ui(self):
        self.canvas = pq.MultiPlotWidget()

        # set the layout for the plot and its toolbar
        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(self.canvas)
        canvas_widget.setLayout(canvas_layout)

        # Other config widget
        self.time_scale = QComboBox()
        self.time_scale.addItem("10s", 10)
        self.time_scale.addItem("30s", 30)
        self.time_scale.addItem("1min", 60)
        self.time_scale.addItem("10min", 10 * 60)
        self.time_scale.addItem("1h", 60 * 60)
        self.time_scale.addItem("All", np.inf)
        self.time_scale.setCurrentIndex(2)

        layout = QHBoxLayout()
        layout.addWidget(canvas_widget)
        layout.addWidget(self.time_scale)
        self.setLayout(layout)

    def update_plotter(self):
        if not self.pause:
            raw_data = self.fetch_latest_data()
            self.update_graph_data(raw_data)
            self.update_graph_scale()

    def update_graph_data(self, data):
        for datum in data:
            y_unit, y_label = datum["y_unit"], datum["y_label"]
            if y_unit not in self.axes:
                ax = self.canvas.addPlot()
                ax.setLabel('left', y_unit, None)
                self.canvas.nextRow()
                ax.addLegend()

                self.axes[y_unit] = {"axis": ax,
                                     "lines": {}}

            ax = self.axes[y_unit]

            if y_label not in ax["lines"]:
                curve_color = self.id_to_colors[len(ax["lines"])]
                ax["lines"][y_label] = ax["axis"].plot(datum["x"],
                                                       datum["y"],
                                                       name=y_label,
                                                       pen=pq.mkPen(curve_color, width=1))
                ax["lines"][y_label].x = datum["x"]
                ax["lines"][y_label].y = datum["y"]
            else:
                line = ax["lines"][y_label]
                line.x += datum["x"]
                line.y += datum["y"]
                line.setData(line.x,
                             line.y)

    def update_graph_scale(self):
        # update x axis
        now = time.time()
        if self.seconds_to_keep != np.inf:
            min_x = now-self.seconds_to_keep
        else:
            min_x = self.time_at_start
        for ax in self.axes.values():
            ax["axis"].setXRange(min_x, now, padding=0)

        # update y axis
        for ax in self.axes.values():
            min_y = np.inf
            max_y = -np.inf
            for line in ax["lines"].values():
                min_y = min(min_y, min(line.y))
                max_y = max(max_y, max(line.y))

            ax["axis"].setYRange(min_y, max_y, padding=0)

    def fetch_latest_data(self):
        return self.model_datain.fetch_plot_data() if self.model_datain else []
        # return [{"y_unit": "meters",
        #          "y_label": "my random",
        #          "x": [time.time()],
        #          "y": [np.random.random()]
        #          },
        #          {"y_unit": "meters",
        #          "y_label": "more random",
        #          "x": [time.time()],
        #          "y": [2 * np.random.random()]
        #          },
        #          {"y_unit": "radian",
        #          "y_label": "my angle",
        #          "x": [time.time()],
        #          "y": [10000 * np.random.random()]
        #          }]

    def set_model(self, model_datain):
        self.model_datain = model_datain

    @property
    def seconds_to_keep(self):
        return self.time_scale.itemData(self.time_scale.currentIndex())

    # def pauseEvent(self):
    #     self.pause = not self.pause
    #     if self.pause:
    #         self.btn_media_ctrl.setIcon(QIcon('Img/control_play.png'))
    #         self.btn_refresh_data.setDisabled(False)
    #         self.btn_clear.setDisabled(False)
    #         self.btn_save.setDisabled(False)
    #     else:
    #         self.btn_media_ctrl.setIcon(QIcon('Img/control_pause.png'))
    #         self.btn_clear.setDisabled(True)
    #         self.btn_refresh_data.setDisabled(True)
    #         self.btn_save.setDisabled(True)
    #         self.update()

    def show_hide(self):
        if self.isVisible():
            self.hide()
            self.pause = True
        else:
            self.show()
            self.pause = False
        self._controller.resize_window()
