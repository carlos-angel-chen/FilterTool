from PyQt5.QtWidgets import QWidget
from Frontend.src.ui.Stage_Widget import Ui_Form

class StageWidget (QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setupUi(self)

