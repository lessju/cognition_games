# coding=utf-8
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

        # Set pixmaps to language selection buttons
        self._main_widget.stroop_english_button.setIcon(gui.QIcon('images/english_flag.png'))
        self._main_widget.stroop_english_button.setIconSize(core.QSize(50, 50))
        self._main_widget.stroop_maltese_button.setIcon(gui.QIcon('images/maltese_flag.jpg'))
        self._main_widget.stroop_maltese_button.setIconSize(core.QSize(50, 50))

        # Populate Stroop game label list
        self._stroop_color_text_english = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK', 'PINK', 'ORANGE', 'PURPLE']
        self._stroop_color_text_maltese = ['aħmar', 'BLU', 'AHDAR', 'ISFAR', 'ISWED', 'ROSA', 'ORANGJO', 'VJOLA']
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
        core.QObject.connect(self._main_widget.stroop_english_button, core.SIGNAL('clicked()'), self.set_stroop_english)
        core.QObject.connect(self._main_widget.stroop_maltese_button, core.SIGNAL('clicked()'), self.set_stroop_maltese)

        # Set current stacked widgets index
        self._main_widget.main_stacked_widget.setCurrentIndex(0)
        self._main_widget.stroop_stacked_widget.setCurrentIndex(0)

        # Show main window
        self.showMaximized()

        # Define require variables
        self._start_time = None
        self._maltese = False

    def set_stroop_english(self):
        self._maltese = False
        self.stroop_populate_ui()

    def set_stroop_maltese(self):
        self._maltese = True
        self.stroop_populate_ui()

    def stroop_populate_ui(self):
        """ Populate Stroop Game UI in either maltese or english """

        if self._maltese:
            self._main_widget.stroop_instructions_label.setText("Suppost din tkun bil-Malti")
            self._main_widget.start_stroop_button.setText("Ibda")
            self._main_widget.stroop_play_again_button.setText("Erga Ilghab")
            self._main_widget.ready_stroop_game_button.setText("Lest")
        else:
            self._main_widget.stroop_instructions_label.setText("""<html><head/><body><p>
            In this game you will see some words displayed on the screen. The aim of the
            game is to say out loud the color of the words you see. Do not read what the words say. For example, for the
            word, RED, you should say &quot;Blue.&quot;</p><p><br/></p><p>As soon as the words appear on the screen, say the
            list of words as fast as you can. When you have finished, click on the &quot;Finish&quot; button. The time it
            took you to read all of the words will be shown.</p><p><br/></p><p>Press &quot;Start&quot; to start the game
            </p></body></html> """)
            self._main_widget.start_stroop_button.setText("Start")
            self._main_widget.stroop_play_again_button.setText("Play Again")
            self._main_widget.ready_stroop_game_button.setText("Ready")

        self._main_widget.stroop_english_button.setVisible(False)
        self._main_widget.stroop_maltese_button.setVisible(False)
        self._main_widget.stroop_instructions_label.setVisible(True)
        self._main_widget.start_stroop_button.setVisible(True)

    def select_stroop(self):
        """ Switch to Stroop game screen """
        self._main_widget.main_stacked_widget.setCurrentIndex(1)
        self._main_widget.stroop_stacked_widget.setCurrentIndex(0)
        self._main_widget.stroop_instructions_label.setVisible(False)
        self._main_widget.stroop_english_button.setVisible(True)
        self._main_widget.stroop_maltese_button.setVisible(True)
        self._main_widget.start_stroop_button.setVisible(False)


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

            if self._maltese:
                label.setText('%s' % self._stroop_color_text_maltese[text])
            else:
                label.setText('%s' % self._stroop_color_text_english[text])
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
