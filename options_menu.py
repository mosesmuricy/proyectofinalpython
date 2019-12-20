# -*- coding: utf-8 -*-

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class OptionsMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Creación de las opciones de "Coeficientes Lotka-Volterra"
        self.a_sb = QtWidgets.QDoubleSpinBox()
        self.b_sb = QtWidgets.QDoubleSpinBox()
        self.c_sb = QtWidgets.QDoubleSpinBox()
        self.d_sb = QtWidgets.QDoubleSpinBox()

        for widget in (self.a_sb, self.b_sb, self.c_sb, self.d_sb):
            widget.setRange(0, 10)
            widget.setSingleStep(0.1)

        coeff_grid = QtWidgets.QGridLayout()
        coeff_grid.addWidget(QtWidgets.QLabel('Tasa de Crecimiento (Presa)'), 0, 0)
        coeff_grid.addWidget(self.a_sb, 0, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Tasa de Mortalidad (Presa)'), 1, 0)
        coeff_grid.addWidget(self.b_sb, 1, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Tasa de Mortalidad (Predador)'), 2, 0)
        coeff_grid.addWidget(self.c_sb, 2, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Tasa de Reproducción (Predador)'), 3, 0)
        coeff_grid.addWidget(self.d_sb, 3, 1)

        coeff_gb = QtWidgets.QGroupBox('Coeficientes Lotka-Volterra:')
        coeff_gb.setLayout(coeff_grid)

        # Creación de las opciones "Otros Parámetros"
        self.predator_sb = QtWidgets.QDoubleSpinBox()
        self.predator_sb.setRange(0, 100000)
        self.predator_sb.setSingleStep(1)

        self.prey_sb = QtWidgets.QDoubleSpinBox()
        self.prey_sb.setRange(0, 100000)
        self.prey_sb.setSingleStep(1)

        self.iterations_sb = QtWidgets.QSpinBox()
        self.iterations_sb.setRange(0, 100000)
        self.iterations_sb.setSingleStep(100)

        self.timedelta_sb = QtWidgets.QDoubleSpinBox()
        self.timedelta_sb.setRange(0, 100)
        self.timedelta_sb.setSingleStep(0.05)

        other_grid = QtWidgets.QGridLayout()
        other_grid.addWidget(QtWidgets.QLabel('Población (Predador)'), 0, 0)
        other_grid.addWidget(self.predator_sb, 0, 1)
        other_grid.addWidget(QtWidgets.QLabel('Población (Presa)'), 1, 0)
        other_grid.addWidget(self.prey_sb, 1, 1)
        other_grid.addWidget(QtWidgets.QLabel('Iteraciones'), 2, 0)
        other_grid.addWidget(self.iterations_sb, 2, 1)
        other_grid.addWidget(QtWidgets.QLabel('Delta Tiempo'), 3, 0)
        other_grid.addWidget(self.timedelta_sb, 3, 1)

        other_gb = QtWidgets.QGroupBox('Otros Parámetros:')
        other_gb.setLayout(other_grid)

        # Creación de "Cpciones del Gráfico" 
        self.legend_cb = QtWidgets.QCheckBox('Mostrar Leyenda')
        self.legend_cb.setChecked(True)

        self.legend_cb.stateChanged.connect(self.legend_change)

        self.grid_cb = QtWidgets.QCheckBox('Mostrar Cuadrícula')
        self.grid_cb.setChecked(True)
        self.legend_loc_lbl = QtWidgets.QLabel('Localización de la Leyenda')
        self.legend_loc_cb = QtWidgets.QComboBox()
        self.legend_loc_cb.addItems([x.title() for x in [
            'derecha',
            'centro',
            'abajo a la izquierda',
            'centro a la derecha',
            'abajo a la izquierda',
            'centro a la izquierda',
            'arriba a la derecha',
            'abajo a la derecha',
            'centro superior',
            'centro inferior',
            'mejor',
        ]])
        self.legend_loc_cb.setCurrentIndex(6)

        cb_box = QtWidgets.QHBoxLayout()
        cb_box.addWidget(self.legend_cb)
        cb_box.addWidget(self.grid_cb)

        legend_box = QtWidgets.QHBoxLayout()
        legend_box.addWidget(self.legend_loc_cb)
        legend_box.addStretch()

        graph_box = QtWidgets.QVBoxLayout()
        graph_box.addLayout(cb_box)
        graph_box.addWidget(self.legend_loc_lbl)
        graph_box.addLayout(legend_box)

        graph_gb = QtWidgets.QGroupBox('Opciones del Gráfico:')
        graph_gb.setLayout(graph_box)

        # Creación de los botones actualizar/restablecer
        self.update_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/calculator.png'),
            'Ejecutar Iteraciones',
        )
        self.reset_values_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Restablecer Valores',
        )
        self.clear_graph_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'),
            'Limpiar el Gráfico',
        )
        self.reset_values_btn.clicked.connect(self.reset_values)

        # Creación del diseño principal
        container = QtWidgets.QVBoxLayout()
        container.addWidget(coeff_gb)
        container.addWidget(other_gb)
        container.addWidget(graph_gb)
        container.addWidget(self.update_btn)
        container.addStretch()
        container.addWidget(self.reset_values_btn)
        container.addWidget(self.clear_graph_btn)
        self.setLayout(container)

        # LLenar los widgets con valores
        self.reset_values()

    def reset_values(self):
        """
        Establece los valores predeterminados de los widgets de opciones.
        """
        self.a_sb.setValue(1.0)
        self.b_sb.setValue(0.1)
        self.c_sb.setValue(1.0)
        self.d_sb.setValue(0.075)
        self.predator_sb.setValue(5)
        self.prey_sb.setValue(10)
        self.iterations_sb.setValue(1000)
        self.timedelta_sb.setValue(0.02)

    def legend_change(self):
        self.legend_loc_cb.setEnabled(self.legend_cb.isChecked())
        self.legend_loc_lbl.setEnabled(self.legend_cb.isChecked())
