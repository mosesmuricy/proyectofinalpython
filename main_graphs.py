# -*- coding: utf-8 -*-
"""
Proyecto Final de Tópicos Especiales I (Python Cientifico)
Alexis Poveda  
Miguel Cámara  8-928-2411
Moisés Souza   E-8-157393
"""

import sys
import matplotlib
import matplotlib.backends.backend_qt4agg as backend_qt4agg
from matplotlib.figure import Figure
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from growth_calculator import GrowthCalculator
from options_menu import OptionsMenu
import resources

APP_NAME = 'Trazador Lotka-Volterra'
AUTHOR = 'Alexis Poveda, Miguel Cámara, Moisés Souza'


class AppForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # Define el título de la pantalla
        self.setWindowTitle(APP_NAME)

        # Agrega el menú de opciones en el dock widget
        self.options_menu = OptionsMenu()
        dock = QtWidgets.QDockWidget('Opciones', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea,
        )
        dock.setWidget(self.options_menu)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        # Conexión de las señales del menú de opciones
        self.options_menu.update_btn.clicked.connect(self.calculate_data)
       
        self.options_menu.clear_graph_btn.clicked.connect(self.clear_graph)

        self.options_menu.legend_cb.stateChanged.connect(self.redraw_graph)

        self.options_menu.grid_cb.stateChanged.connect(self.redraw_graph)

        self.options_menu.legend_loc_cb.currentIndexChanged.connect(self.redraw_graph)

        # Creación del grafo de trama
        fig = Figure((7.0, 3.0), dpi=100)
        self.canvas = backend_qt4agg.FigureCanvasQTAgg(fig)
        self.canvas.setParent(self)
        self.axes = fig.add_subplot(111)
        backend_qt4agg.NavigationToolbar2QT(self.canvas, self.canvas)

        # Inicialización del grafo
        self.clear_graph()

        # Establece al grafo como el widget principal en la pantalla
        self.setCentralWidget(self.canvas)

        # Creación de la barra de menú de acciones
        file_exit_action = QtWidgets.QAction('S&alir', self)
        file_exit_action.setToolTip('Salir')
        file_exit_action.setIcon(QtGui.QIcon(':/resources/door_open.png'))
       ## self.connect(file_exit_action,QtCore.SIGNAL('triggered()'),self.close)

        about_action = QtWidgets.QAction('&Acerca de', self)
        about_action.setToolTip('Acerca de')
        about_action.setIcon(QtGui.QIcon(':/resources/icon_info.gif'))
       ## self.connect(about_action,QtCore.SIGNAL('triggered()'),self.show_about)

        # Creación de la barra de menú
        file_menu = self.menuBar().addMenu('&Archivo')
        file_menu.addAction(file_exit_action)

        help_menu = self.menuBar().addMenu('&Ayuda')
        help_menu.addAction(about_action)

    def calculate_data(self):
        # Creación del objeto GrowthCalculator 
        growth = GrowthCalculator()

        # Actualización de los parámetros que recibe el GrowthCalculator de la opciones de la interfaz
        growth.a = self.options_menu.a_sb.value()
        growth.b = self.options_menu.b_sb.value()
        growth.c = self.options_menu.c_sb.value()
        growth.d = self.options_menu.d_sb.value()
        growth.predators = self.options_menu.predator_sb.value()
        growth.prey = self.options_menu.prey_sb.value()
        growth.iterations = self.options_menu.iterations_sb.value()
        growth.dt = self.options_menu.timedelta_sb.value()

        # Cálculo de los crecimientos de las poblaciones
        results = growth.calculate()
        self.predator_history.extend(results['predator'])
        self.prey_history.extend(results['prey'])

        # Establece los últimos tamaños de población en la barra de herramientas de opciones
        self.options_menu.predator_sb.setValue(self.predator_history[-1])
        self.options_menu.prey_sb.setValue(self.prey_history[-1])

        # Redibuja el grafo
        self.redraw_graph()

    def clear_graph(self):
        # Limpia las historias de las poblaciones
        self.predator_history = []
        self.prey_history = []

        # Redibuja el grafo
        self.redraw_graph()

    def redraw_graph(self):
        # Limpia el grafo
        self.axes.clear()

        # Creación de las etiquetas del Grafo
        self.axes.set_title('Ciclos de Crecimientos Predador y Presa')
        self.axes.set_xlabel('Iteraciones')
        self.axes.set_ylabel('Tamaño de la Población')

        # Grafica los datos actuales de la población
        if self.predator_history:
            self.axes.plot(self.predator_history, 'r-', label='Predador')
        if self.prey_history:
            self.axes.plot(self.prey_history, 'b-', label='Presa')

        # Creación de leyenda si es necesaria
        if self.options_menu.legend_cb.isChecked():
            if self.predator_history or self.prey_history:
                legend_loc = str(
                    self.options_menu.legend_loc_cb.currentText()
                ).lower()
                legend = matplotlib.font_manager.FontProperties(size=10)
                self.axes.legend(loc=legend_loc, prop=legend)

        # Establece una cuadricula si es necesaria
        self.axes.grid(self.options_menu.grid_cb.isChecked())

        # Dibuja el gráfico
        self.canvas.draw()

    def show_about(self):
        """
        Muestra el cuadro de diálogo "Acerca de".
        """
        message = '''<font size="+2">%s</font>
            <p>Un trazador Lotka-Volterra escrito en Python.
            <p>Escrito por %s,
            <p>Iconos obtenidos de <a href="http://www.famfamfam.com/">famfamfam</a> y
            <a href="http://commons.wikimedia.org/">Wikimedia
            Commons</a>.''' % (APP_NAME, AUTHOR)

        QtWidgets.QMessageBox.about(self, 'Acerca de ' + APP_NAME, message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/resources/icon.svg'))
    form = AppForm()
    form.show()
    app.exec_()
