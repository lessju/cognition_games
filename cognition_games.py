# PyQt Stuff
import PyQt4.QtCore as core
import PyQt4.QtGui as gui
import PyQt4.uic as uic

# Python packages
import random
import sys 

# ------------------------- MAIN WINDOW --------------------------------
import time


class CognitionGames(gui.QMainWindow):
    """ Class encapsulating UI functionality"""

    def __init__(self, uiFile):
        """ Initialise main window """
        super(CognitionGames, self).__init__()
        # Load window file
        self._main_widget = uic.loadUi(uiFile)
        self.setCentralWidget(self._main_widget)
        self.setWindowTitle("Cognition Game")

        # Set pixmaps to game selection screen buttons
        self._main_widget.stroop_select_button.setIcon(gui.QIcon('images/stroop_game.jpg'))
        self._main_widget.stroop_select_button.setIconSize(self._main_widget.stroop_select_button.size())

        self._main_widget.wug_select_button.setIcon(gui.QIcon('images/wug_game.jpg'))
        self._main_widget.wug_select_button.setIconSize(self._main_widget.wug_select_button.size())

        self._main_widget.sally_ann_select_button.setIcon(gui.QIcon('images/sally_anne_game.jpg'))
        self._main_widget.sally_ann_select_button.setIconSize(self._main_widget.sally_ann_select_button.size())

        # Populate Stroop game label list
        self._stroop_color_text = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK', 'PINK', 'ORANGE', 'PURPLE']
        self._stroop_color_value = [(255, 0, 0), (0, 0, 255), (0, 255, 0),
                                    (255, 255, 50), (0, 0, 0), (255, 51, 153),
                                    (255, 161, 0), (153, 0, 153)]

        self._stroop_label_list = []
        for i in range(1, 26):
            self._stroop_label_list.append(getattr(self._main_widget, "stroop_text_%d" % i))

        # Connect game selection button
        core.QObject.connect(self._main_widget.stroop_select_button, core.SIGNAL('clicked()'), self.select_stroop)
        core.QObject.connect(self._main_widget.wug_select_button, core.SIGNAL('clicked()'), self.select_wug)
        core.QObject.connect(self._main_widget.sally_ann_select_button, core.SIGNAL('clicked()'), self.select_sally_anne)
        core.QObject.connect(self._main_widget.start_stroop_button, core.SIGNAL('clicked()'), self.start_stroop_game)
        core.QObject.connect(self._main_widget.ready_stroop_game_button, core.SIGNAL('clicked()'), self.ready_stroop_game)
        core.QObject.connect(self._main_widget.stroop_play_again_button, core.SIGNAL('clicked()'), self.select_stroop)

        # Set current stacked widgets index
        self._main_widget.main_stacked_widget.setCurrentIndex(0)
        self._main_widget.stroop_stacked_widget.setCurrentIndex(0)

        # Show main window
        self.showMaximized()

        # Define require variables
        self._start_time = None

    def select_stroop(self):
        """ Switch to Stroop game screen """
        self._main_widget.main_stacked_widget.setCurrentIndex(1)
        self._main_widget.stroop_stacked_widget.setCurrentIndex(0)

    def select_wug(self):
        """ Switch to Wug game screen """
        self._main_widget.main_stacked_widget.setCurrentIndex(2)

    def select_sally_anne(self):
        """ Switch to Sally Anne screen """
        self._main_widget.main_stacked_widget.setCurrentIndex(3)

    def start_stroop_game(self):
        """ Start Stroop Game """

        # Create randmoised text
        for label in self._stroop_label_list:
            # Generate random indices
            text = random.randint(0, 7)
            color = text
            while color == text:
                color = random.randint(0, 7)

            label.setText('%s' % self._stroop_color_text[text])
            label.setStyleSheet("QLabel {color :  rgba(%d, %d, %d, 255); }" % self._stroop_color_value[color])

        # Start timer
        self._start_time = time.time()

        # Change to game page
        if self._main_widget.main_stacked_widget.currentIndex() == 1:
            self._main_widget.stroop_stacked_widget.setCurrentIndex(1)

    def ready_stroop_game(self):
        """ Ready from stroop game """

        # Calculate time elapsed and show dialog box
        duration =  time.time() - self._start_time
        msg = gui.QMessageBox()
        msg.setIcon(gui.QMessageBox.Information)
        msg.setText("Time taken: %.1f seconds" % duration)
        msg.setWindowTitle("Stroop Game")
        msg.setStandardButtons(gui.QMessageBox.Ok)
        msg.exec_()

        # Switch to explanation page
        self._main_widget.stroop_stacked_widget.setCurrentIndex(2)

# Application entry point
if __name__ == "__main__":
    app = gui.QApplication(sys.argv)
    app.setApplicationName("Cognition Games")
    plotter = CognitionGames("cognition_games.ui")
    sys.exit(app.exec_())
