# Under MIT License, see LICENSE.txt
import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


__author__ = 'RoboCupULaval'


class PlotterView(QWidget):
    def __init__(self, controller=None):
        QWidget.__init__(self, controller)
        self._controller = controller


        self.time_at_start = time.time()
        self.pause = False
        self.init_ui()
        self.init_plot()

        # Timer
        self._timer_update = QTimer()
        self._timer_update.timeout.connect(self.update_plotter)
        self._timer_update.start(100)


    def init_ui(self):

        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout for the plot and its toolbar
        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(self.canvas)
        canvas_layout.addWidget(self.toolbar)
        canvas_widget.setLayout(canvas_layout)

        # Other config widget
        self.time_scale = QComboBox()
        self.time_scale.addItem("10s", 10)
        self.time_scale.addItem("30s", 30)
        self.time_scale.addItem("1min", 60)
        self.time_scale.addItem("10min", 10 * 60)
        self.time_scale.addItem("1h", 60 * 60)
        self.time_scale.addItem("All", np.inf)
        self.time_scale.setCurrentIndex(5)


        layout = QHBoxLayout()
        layout.addWidget(canvas_widget)
        layout.addWidget(self.time_scale)
        self.setLayout(layout)

    def init_plot(self):
        ''' plot some random stuff '''
        # random data
        self.x = []
        self.y = []

        # instead of ax.hold(False)
        self.figure.clear()
        #self.figure.tight_layout()

        # create an axis
        #self.ax = self.figure.add_subplot(111) # sharex=True

        # self.ax.autoscale(True, 'y')
        # self.ax.autoscale(False, 'x')
        # self.ax.set_xlim([0, 10])
        self.axes = {}

        # plot data
        #self.points = self.ax.plot(self.x, self.y, '-')[0]

        # refresh canvas
        self.canvas.draw()

    def fetch_latest_data(self):
        return [{"y_unit": "meters",
                 "y_label": "my random",
                 "x": [time.time()],
                 "y": [np.random.random()]
                 },
                 {"y_unit": "meters",
                 "y_label": "more random",
                 "x": [time.time()],
                 "y": [2 * np.random.random()]
                 },
                 {"y_unit": "radian",
                 "y_label": "my angle",
                 "x": [time.time()],
                 "y": [10000 * np.random.random()]
                 }]

    def update_plotter(self):
        if not self.pause:
            raw_data = self.fetch_latest_data()
            self.update_graph_data(raw_data)
            self.update_graph_scale()



    def update_graph_data(self, data):
        # Create new subplot for new unit and add data
        for datum in data:
            y_unit, y_label = datum["y_unit"], datum["y_label"]
            if y_unit not in self.axes:
                ax = self._append_plot()
                ax.set_ylabel(y_unit)
                ax.legend(loc='upper right')

                self.axes[y_unit] = {"axis": ax,
                                     "labels": {},
                                     "background": self.figure.canvas.copy_from_bbox(ax.bbox)}
                self.canvas.draw()

            ax = self.axes[y_unit]

            if y_label not in ax["labels"]:
                ax["labels"][y_label] = ax["axis"].plot(datum["x"], datum["y"], label=y_label)[0]
            else:
                pts = ax["labels"][y_label]
                pts.set_data(list(pts.get_xdata()) + datum["x"],
                             list(pts.get_ydata()) + datum["y"])

                # Fast redraw hack
                self.figure.canvas.restore_region(ax["background"])
                ax["axis"].draw_artist(pts)
                self.figure.canvas.blit(ax["axis"].bbox)

    def update_graph_scale(self):
        for ax in self.axes.values():
            min_y = np.inf
            max_y = -np.inf
            for label in ax["labels"].values():
                min_y = min(min_y, min(label.get_ydata()))
                max_y = max(max_y, max(label.get_ydata()))

            ax["axis"].set_ylim((min_y, max_y))

        # update x axis
        seconds_to_keep = self.time_scale.itemData(self.time_scale.currentIndex())
        now = time.time()
        if seconds_to_keep != np.inf:
            min_x = now-seconds_to_keep
        else:
            min_x = self.time_at_start
        for ax in self.axes.values():
            ax["axis"].set_xlim((min_x, now))

    def _append_plot(self):
        n = len(self.figure.axes)
        for i, ax in enumerate(self.figure.axes):
            ax.change_geometry(n + 1, 1, i + 1)

        return self.figure.add_subplot(n + 1, 1, n + 1)


    def pauseEvent(self):
        self.pause = not self.pause
        if self.pause:
            self.btn_media_ctrl.setIcon(QIcon('Img/control_play.png'))
            self.btn_refresh_data.setDisabled(False)
            self.btn_clear.setDisabled(False)
            self.btn_save.setDisabled(False)
        else:
            self.btn_media_ctrl.setIcon(QIcon('Img/control_pause.png'))
            self.btn_clear.setDisabled(True)
            self.btn_refresh_data.setDisabled(True)
            self.btn_save.setDisabled(True)
            self.update()

    def show_hide(self):
        if self.isVisible():
            self.hide()
            self.pause = True
        else:
            self.show()
            self.pause = False
        self._controller.resize_window()
