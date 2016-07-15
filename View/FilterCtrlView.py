# Under MIT License, see LICENSE.txt

from PyQt4 import QtGui
from PyQt4 import QtCore

__author__ = 'RoboCupULaval'


class FilterCtrlView(QtGui.QWidget):
    def __init__(self, controller):
        QtGui.QWidget.__init__(self)
        self._ctrl = controller
        self._layout_v = QtGui.QVBoxLayout()

        # Timer
        # TODO - Changer par emit signal stateChanged()
        self._timer_refresh = QtCore.QTimer()
        self._timer_refresh.timeout.connect(self.load_new_filter)
        self._timer_refresh.start(100)

        # Initialisation
        self.init_ui()
        self.init_checkbox()
        self.hide()

    def init_ui(self):
        """ Initialise l'UI du widget """
        self._layout_v.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self._layout_v)
        self._layout_v.activate()

    def init_checkbox(self):
        """ Recharge toutes les checkbox avec les filtres présents """
        self.reset_layout()
        for name in self._ctrl.get_list_of_filters():
            widget_check = QtGui.QCheckBox(name)
            widget_check.setChecked(True)
            self._layout_v.addWidget(widget_check)

    def load_new_filter(self):
        """ Recharge les nouveaux filtres et les convertis en checkbox """
        list_current_checkbox = set()
        for i in range(1, self._layout_v.count()):
            try:
                list_current_checkbox.add(self._layout_v.itemAt(i).widget().text())
            except Exception as e:
                pass

        list_filter = self._ctrl.get_list_of_filters()

        if len(list_filter) > len(list_current_checkbox):
            for filter_str in list_filter - list_current_checkbox:
                self.add_filter(filter_str)
        elif len(list_filter) < len(list_current_checkbox):
            for filter_str in list_current_checkbox - list_filter:
                self.delete_specific_filter(filter_str)
        self._ctrl.set_filter(self.get_checked_box())

    def add_filter(self, name):
        """ Ajoute une chackbox spécifiée par le nom """
        widget_check = QtGui.QCheckBox(name, self)
        widget_check.setChecked(True)
        self._layout_v.insertWidget(self._layout_v.count(), widget_check)

    def delete_specific_filter(self, name):
        """ Détruit la checkbox spécifiée par le nom """
        for i in range(1, self._layout_v.count()):
            try:
                widget = self._layout_v.itemAt(i).widget()
                if widget.text() == name:
                    widget.hide()
                    self._layout_v.removeWidget(widget)
                    del widget
            except Exception as e:
                print(e)

    def reset_layout(self):
        """ Efface les widgets contenu dans le layout """
        for i in range(self._layout_v.count()):
            self._layout_v.removeWidget(self._layout_v.itemAt(i))
        self._layout_v.addWidget(QtGui.QLabel('Sélectionner les filtres à afficher: '))

    def get_checked_box(self):
        """ Récupère la liste des filtres sélectionnés """
        list_checked_box = []
        for i in range(self._layout_v.count()):
            widget = self._layout_v.itemAt(i).widget()
            try:
                if widget.isChecked():
                    list_checked_box.append(widget.text())
            except Exception as e:
                pass
        return list_checked_box

    def show_hide(self):
        """ Afficher/Cacher le filtre de dessins """
        if self.isVisible():
            self.hide()
        else:
            self.show()
