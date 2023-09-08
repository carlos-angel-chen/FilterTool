import numpy as np
from PyQt5.QtWidgets import QWidget
from Frontend.src.ui.tp4 import Ui_Form
from Frontend.src.tp4_stages import Stages
from back.backend import FilterSpace, FilterType, ApproxType, plot_template

class MainWindowQ (QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)

        self.setupUi(self)
        self.error = 0
        self.cant_curvas = 0
        self.fs = FilterSpace()

        self.Qmax = 0
        self.Nmaxmin = 0
        self.denom = 0

        self.Qmax_valor = 0
        self.denom_valor = 0

        #HIDESSSS
        self.label_19.hide()
        self.label_20.hide()
        self.label_21.hide()
        self.label_22.hide()
        self.label_24.hide()
        self.label_25.hide()

        self.fa_mas_valor.hide()
        self.fa_menos_valor.hide()
        self.fp_mas_valor.hide()
        self.fp_menos_valor.hide()
        self.GD_value.hide()
        self.tolerance_value.hide()

        self.Denom_slider.hide()
        self.Denom_box.hide()
        self.Q_slider.hide()
        self.Q_box.hide()

        self.label_23.hide()
        self.N_max_slider.hide()
        self.N_max_box.hide()
        self.label_9.setText("N")
        self.label_3.hide()

        self.aproximation_select_2.hide()


        #BOXESSSSSSS
        self.filter_select.currentIndexChanged.connect(self.filter_change)
        self.aproximation_select.currentIndexChanged.connect(self.aproximation_change)
        self.Curve_List_Select.currentIndexChanged.connect(self.curve_change)
        self.type_graph_select.currentIndexChanged.connect(self.type_graph_change)


        #CHECK BOXESSSSS
        self.N_check.stateChanged.connect(self.N_check_state)
        self.Q_check.stateChanged.connect(self.Q_check_state)
        self.Denom_check.stateChanged.connect(self.Denom_check_state)
        self.Template_checkbox.stateChanged.connect(self.Template_check_state)


        #BUTTONSSSS
        self.add_curve_button.clicked.connect(self.create_curve)
        self.remove_curve_button.clicked.connect(self.remove_curve)

        self.Design_Stages_button.clicked.connect(self.Design_Stages)


        #GRAPHHHHHH
        #crear el box para la toolbar
        self.MplWidget.show_toolbar(self.Toolbar1)




    # FUNCIONESSSS

    def filter_change(self, value):
        if value == 0 or value == 1:
            self.label_19.hide()
            self.label_20.hide()
            self.label_21.hide()
            self.label_22.hide()
            self.label_24.hide()
            self.label_25.hide()
            self.fa_mas_valor.hide()
            self.fa_menos_valor.hide()
            self.fp_mas_valor.hide()
            self.fp_menos_valor.hide()
            self.GD_value.hide()
            self.tolerance_value.hide()
            self.aproximation_select_2.hide()
            self.label_15.show()
            self.label_16.show()
            self.Aa_Valor.show()
            self.Ap_valor.show()
            self.label_17.show()
            self.label_18.show()
            self.fp_valor.show()
            self.fa_valor.show()
            self.aproximation_select.show()


        elif value == 2 or value == 3:
            self.label_17.hide()
            self.label_18.hide()
            self.fa_valor.hide()
            self.fp_valor.hide()
            self.label_24.hide()
            self.label_25.hide()
            self.GD_value.hide()
            self.tolerance_value.hide()
            self.aproximation_select_2.hide()
            self.label_15.show()
            self.label_16.show()
            self.label_19.show()
            self.label_20.show()
            self.label_21.show()
            self.label_22.show()
            self.Aa_Valor.show()
            self.Ap_valor.show()
            self.fa_mas_valor.show()
            self.fa_menos_valor.show()
            self.fp_mas_valor.show()
            self.fp_menos_valor.show()
            self.aproximation_select.show()


        elif value == 4:
            self.label_15.hide()
            self.label_16.hide()
            self.label_17.hide()
            self.fa_valor.hide()
            self.label_19.hide()
            self.label_20.hide()
            self.label_21.hide()
            self.label_22.hide()
            self.Aa_Valor.hide()
            self.Ap_valor.hide()
            self.fa_mas_valor.hide()
            self.fa_menos_valor.hide()
            self.fp_mas_valor.hide()
            self.fp_menos_valor.hide()
            self.aproximation_select.hide()
            self.label_18.show()
            self.label_24.show()
            self.label_25.show()
            self.fp_valor.show()
            self.GD_value.show()
            self.tolerance_value.show()
            self.aproximation_select_2.show()


    def aproximation_change(self, value):
        if value == 2:
            self.label_14.hide()
            self.Denom_check.hide()
            self.Denom_slider.hide()
            self.Denom_box.hide()
        else:
            self.label_14.show()
            self.Denom_check.show()

    def type_graph_change(self):
        self.MplWidget.canvas.ax.clear()
        if len(self.fs.filters) != 0:
            if self.type_graph_select.currentIndex() == 0:
                self.fs.plot_mod(self.MplWidget.canvas.ax, A=False)

            elif self.type_graph_select.currentIndex() == 1:
                self.fs.plot_ph(self.MplWidget.canvas.ax)

            elif self.type_graph_select.currentIndex() == 2:
                self.fs.plot_mod(self.MplWidget.canvas.ax, A=True)

            elif self.type_graph_select.currentIndex() == 3:
                self.fs.plot_gd(self.MplWidget.canvas.ax)

            elif self.type_graph_select.currentIndex() == 4:
                self.fs.plot_zp(self.MplWidget.canvas.ax)
        self.MplWidget.canvas.draw()


    def N_check_state (self, value):
        if value == 0:
            self.label_23.hide()
            self.N_max_slider.hide()
            self.N_max_box.hide()
            self.label_9.setText("N")
            self.Nmaxmin = 0
        else:
            self.label_23.show()
            self.N_min_slider_2.show()
            self.N_min_box_2.show()
            self.N_max_slider.show()
            self.N_max_box.show()
            self.label_9.setText("Nmin")
            self.Nmaxmin = 1

    def Q_check_state (self, value):
        if value == 0:
            self.Q_slider.hide()
            self.Q_box.hide()
            self.Qmax = 0
        else:
            self.Q_slider.show()
            self.Q_box.show()
            self.Qmax = 1

    def Denom_check_state (self, value):
        if value == 0:
            self.Denom_slider.hide()
            self.Denom_box.hide()
            self.denom = 0
        else:
            self.Denom_slider.show()
            self.Denom_box.show()
            self.denom = 1

    def Template_check_state(self, value):
        if len(self.fs.filters) != 0:
            if value == 0:
                self.type_graph_change()
            else:
                if self.type_graph_select.currentIndex() == 0:
                    plot_template(self.MplWidget.canvas.ax, self.fs.filters[self.Curve_List_Select.currentIndex()].type,
                                  self.fs.filters[self.Curve_List_Select.currentIndex()].data, A=False)
                elif self.type_graph_select.currentIndex() == 2:
                    plot_template(self.MplWidget.canvas.ax, self.fs.filters[self.Curve_List_Select.currentIndex()].type,
                                  self.fs.filters[self.Curve_List_Select.currentIndex()].data, A=True)
                self.MplWidget.canvas.draw()


    def create_curve(self):
        if self.Qmax == 0:
            self.Qmax_valor = None
            self.Qmax_text = "Auto."
        else:
            self.Qmax_valor = self.Q_box.value()
            self.Qmax_text = str(self.Q_box.value())
        if self.denom == 0:
            self.denom_valor = 0
            self.denom_text = "Auto."
        else:
            self.denom_valor = self.Denom_box.value()
            self.denom_text = str(self.Denom_box.value())

        if self.filter_select.currentIndex() == 0 or self.filter_select.currentIndex() == 1:
            if self.Nmaxmin == 0:
                if (self.fs.addFilter(self.filter_select.currentIndex(), self.aproximation_select.currentIndex(), (self.fp_valor.value()) * 2 * np.pi, (self.fa_valor.value()) * 2 * np.pi, self.Ap_valor.value(), self.Aa_Valor.value(), self.denom_valor, self.Gain_valor.value(),self.N_min_box_2.value(), None, None, None, self.Qmax_valor, None, None, None) == ""):
                    self.error = 0
                else:
                    self.error = 1
            elif self.Nmaxmin == 1:
                if (self.fs.addFilter(self.filter_select.currentIndex(), self.aproximation_select.currentIndex(),
                                      (self.fp_valor.value()) * 2 * np.pi, (self.fa_valor.value()) * 2 * np.pi, self.Ap_valor.value(), self.Aa_Valor.value(), self.denom_valor, self.Gain_valor.value(),
                                      None, None, self.N_min_box_2.value(), self.N_max_box.value(), self.Qmax_valor, None,
                                      None, None) == ""):
                    self.error = 0
                else:
                    self.error = 1



        if self.filter_select.currentIndex() == 2 or self.filter_select.currentIndex() == 3:
            self.fa_masmenos = [(self.fa_menos_valor.value()) * 2 * np.pi , (self.fa_mas_valor.value()) * 2 * np.pi]
            self.fp_masmenos = [(self.fp_menos_valor.value()) * 2 * np.pi, (self.fp_mas_valor.value()) * 2 * np.pi]
            if self.Nmaxmin == 0:
                if (self.fs.addFilter(self.filter_select.currentIndex(), self.aproximation_select.currentIndex(), self.fp_masmenos, self.fa_masmenos, self.Ap_valor.value(), self.Aa_Valor.value(), self.denom_valor, self.Gain_valor.value(), self.N_min_box_2.value(), None, None, None, self.Qmax_valor, None, None, None) == ""):
                    self.error = 0
                else:
                    self.error = 1
            elif self.Nmaxmin == 1:
                if (self.fs.addFilter(self.filter_select.currentIndex(), self.aproximation_select.currentIndex(),
                                      self.fp_masmenos, self.fa_masmenos, self.Ap_valor.value(), self.Aa_Valor.value(), self.denom_valor, self.Gain_valor.value(),
                                      None, None, self.N_min_box_2.value(), self.N_max_box.value(), self.Qmax_valor, None,
                                      None, None) == ""):
                    self.error = 0
                else:
                    self.error = 1


        elif self.filter_select.currentIndex() == 4:
            if self.aproximation_select_2.currentIndex() == 0:
                self.var = 5
            else:
                self.var = 6
            if self.Nmaxmin == 0:
                if (self.fs.addFilter(self.filter_select.currentIndex(), self.var, (self.fp_valor.value()) * 2 * np.pi, None, None, None, self.denom_valor, self.Gain_valor.value(), self.N_min_box_2.value(), None, None, None, self.Qmax_valor, None, self.GD_value.value(), self.tolerance_value.value()) == ""):
                    self.error = 0
                else:
                    self.error = 1
            elif self.Nmaxmin == 1:
                if (self.fs.addFilter(self.filter_select.currentIndex(), self.var,
                                      (self.fp_valor.value()) * 2 * np.pi, None, None, None, self.denom_valor, self.Gain_valor.value(),
                                      None, None, self.N_min_box_2.value(), self.N_max_box.value(), self.Qmax_valor, None,
                                      self.GD_value.value(), self.tolerance_value.value()) == ""):
                    self.error = 0
                else:
                    self.error = 1

        if self.error == 0:
            self.label_3.hide()
            self.Curve_List_Select.addItems((self.fs.filters[self.cant_curvas].name).split('\n'))
            self.cant_curvas = self.cant_curvas + 1
            self.label_3.hide()
            self.type_graph_change()
        else:
            self.label_3.show()
            self.error = 0

    def remove_curve(self):
        if self.cant_curvas > 0:
            self.fs.delFilter(self.fs.filters[self.Curve_List_Select.currentIndex()])
            self.Curve_List_Select.removeItem(self.Curve_List_Select.currentIndex())
            self.cant_curvas = self.cant_curvas - 1
            self.type_graph_change()


    def curve_change (self):
        self.type_graph_change()

    def Design_Stages (self):
        print("second")
        if self.cant_curvas > 0:
            self.stages = Stages(self.fs.filters[self.Curve_List_Select.currentIndex()])








