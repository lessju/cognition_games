# -*- coding: utf-8 -*-

# PyQt Stuff
import re

import PyQt4.QtCore as core
import PyQt4.QtGui as gui
import PyQt4.uic as uic

# Python packages
import random
import codecs
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

        self._main_widget.sally_ann_select_button.setIcon(gui.QIcon('images/sally_anne_game.jpg'))
        self._main_widget.sally_ann_select_button.setIconSize(self._main_widget.sally_ann_select_button.size())

        # Set pixmaps to language selection buttons
        self._main_widget.stroop_english_button.setIcon(gui.QIcon('images/english_flag.png'))
        self._main_widget.stroop_english_button.setIconSize(core.QSize(50, 50))
        self._main_widget.stroop_maltese_button.setIcon(gui.QIcon('images/maltese_flag.jpg'))
        self._main_widget.stroop_maltese_button.setIconSize(core.QSize(50, 50))
        self._main_widget.sally_anne_english_button.setIcon(gui.QIcon('images/english_flag.png'))
        self._main_widget.sally_anne_english_button.setIconSize(core.QSize(50, 50))
        self._main_widget.sally_anne_maltese_button.setIcon(gui.QIcon('images/maltese_flag.jpg'))
        self._main_widget.sally_anne_maltese_button.setIconSize(core.QSize(50, 50))

        #  Connect signals (Stroop)
        core.QObject.connect(self._main_widget.stroop_select_button, core.SIGNAL('clicked()'), self.select_stroop)
        core.QObject.connect(self._main_widget.stroop_change_game_button, core.SIGNAL("clicked()"), self.reset_game)
        core.QObject.connect(self._main_widget.start_stroop_button, core.SIGNAL('clicked()'), self.start_stroop_game)
        core.QObject.connect(self._main_widget.ready_stroop_game_button, core.SIGNAL('clicked()'),  #
                             self.start_stroop_game)
        core.QObject.connect(self._main_widget.stroop_play_again_button, core.SIGNAL('clicked()'), self.select_stroop)
        core.QObject.connect(self._main_widget.stroop_english_button, core.SIGNAL('clicked()'), self.set_stroop_english)
        core.QObject.connect(self._main_widget.stroop_maltese_button, core.SIGNAL('clicked()'), self.set_stroop_maltese)

        # Connect signals (Sally Anne)
        core.QObject.connect(self._main_widget.sally_ann_select_button, core.SIGNAL('clicked()'),
                             self.select_sally_anne)
        core.QObject.connect(self._main_widget.sally_anne_change_game_button, core.SIGNAL("clicked()"), self.reset_game)
        core.QObject.connect(self._main_widget.start_sally_anne_button, core.SIGNAL('clicked()'),
                             self.start_sally_anne_game)
        core.QObject.connect(self._main_widget.sally_anne_english_button, core.SIGNAL('clicked()'),
                             self.set_sally_anne_english)
        core.QObject.connect(self._main_widget.sally_anne_maltese_button, core.SIGNAL('clicked()'),
                             self.set_sally_anne_maltese)
        core.QObject.connect(self._main_widget.sally_anne_next_button, core.SIGNAL('clicked()'),
                             self.sally_anne_move_slide)
        core.QObject.connect(self._main_widget.sally_anne_answer_1_button, core.SIGNAL('clicked()'),
                             self.sally_anne_answer_1_pressed)
        core.QObject.connect(self._main_widget.sally_anne_answer_2_button, core.SIGNAL('clicked()'),
                             self.sally_anne_answer_2_pressed)
        core.QObject.connect(self._main_widget.sally_anne_play_again_button, core.SIGNAL('clicked()'),
                             self.sally_anne_final_page)

        # Set current stacked widgets index
        self._main_widget.main_stacked_widget.setCurrentIndex(0)
        self._main_widget.stroop_stacked_widget.setCurrentIndex(0)

        # Show main window
        self.showMaximized()

        # Populate Stroop game label list
        self._stroop_color_text_english = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK', 'PINK', 'ORANGE', 'PURPLE']
        self._stroop_color_text_maltese = [u'AĦMAR', u'BLU', u'AĦDAR', u'ISFAR', u'ISWED', u'ROŻA', u'ORANĠJO',
                                           u'VJOLA']
        self._stroop_color_value = [(255, 0, 0), (0, 0, 255), (0, 255, 0),
                                    (255, 255, 50), (0, 0, 0), (255, 51, 153),
                                    (255, 161, 0), (153, 0, 153)]

        self._stroop_label_list = []
        for i in range(1, 26):
            self._stroop_label_list.append(getattr(self._main_widget, "stroop_text_%d" % i))
        self._stroop_index = 0

        # Populate sally anne image dimensions from file
        self._sally_anne_image_dimensions = {}
        with open("images/sally_anne_image_dimensions.csv", "r") as f:
            for item in f.read().splitlines():
                vals = [int(x) for x in item.split(',')]
                self._sally_anne_image_dimensions[vals[0]] = (vals[1], vals[2])

        # Parse sally anne text files
        def process_text_file(filepath):
            result = {}
            with codecs.open(filepath, 'r', 'utf-8') as f:
                text = f.read().replace('\r', '')
                # Find all positions of '['
                pos = [pos for pos, char in enumerate(text) if char == '[']

                # Generate text dictionary
                for i, item in enumerate(pos):
                    if i == len(pos) - 1:
                        substring = text[item:]
                    else:
                        substring = text[item:pos[i + 1]]

                    # Get key and value pair from substringre
                    key = re.search('\[.*\]', substring).group()
                    value = substring[len(key) + 1:-2]
                    result[key[1:-1]] = value
            return result

        self._sally_anne_english_text = process_text_file("text/sally_anne_english.txt")
        self._sally_anne_maltese_text = process_text_file("text/sally_anne_maltese.txt")
        self._stroop_english_text = process_text_file("text/stroop_english.txt")
        self._stroop_maltese_text = process_text_file("text/stroop_maltese.txt")

        # Define require variables
        self._sally_anne_answer = 1
        self._sally_anne_page_index = 0
        self._start_time = None
        self._maltese = False

    def reset_game(self):
        self._main_widget.main_stacked_widget.setCurrentIndex(0)

    # ------------------------------------------ Stroop functions ----------------------------------------
    def set_stroop_english(self):
        self._maltese = False
        self.stroop_populate_ui()

    def set_stroop_maltese(self):
        self._maltese = True
        self.stroop_populate_ui()

    def stroop_populate_ui(self):
        """ Populate Stroop Game UI in either maltese or english """

        if self._maltese:
            self._main_widget.stroop_instructions_label.setText(self._stroop_maltese_text['instructions'])
            self._main_widget.start_stroop_button.setText("Ibda")
            self._main_widget.stroop_play_again_button.setText(u"Erga Ilgħab")
            self._main_widget.ready_stroop_game_button.setText("Lest")
            self._main_widget.stroop_explanation_label.setText(self._stroop_maltese_text['explanation'])
            self._main_widget.stroop_change_game_button.setText(u"Biddel il-Logħoba")
        else:
            self._main_widget.stroop_instructions_label.setText(self._stroop_english_text['instructions'])
            self._main_widget.start_stroop_button.setText("Start")
            self._main_widget.stroop_play_again_button.setText("Play Again")
            self._main_widget.ready_stroop_game_button.setText("Ready")
            self._main_widget.stroop_explanation_label.setText(self._stroop_english_text['explanation'])
            self._main_widget.stroop_change_game_button.setText("Change game")

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

    def start_stroop_game(self):
        """ Start Stroop Game """

        if 0 < self._stroop_index < 3:
            self.ready_stroop_game()

        # Create randmoised text
        for label in self._stroop_label_list:
            # Generate random indices
            text = random.randint(0, 7)
            color = text
            if self._stroop_index != 0:
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

        self._stroop_index += 1

        if self._stroop_index == 3:
            self._stroop_index = 0
            self._main_widget.stroop_stacked_widget.setCurrentIndex(2)

    def ready_stroop_game(self):
        """ Ready from stroop game """

        # Calculate time elapsed and show dialog box
        duration = time.time() - self._start_time
        msg = gui.QMessageBox()
        msg.setIcon(gui.QMessageBox.Information)
        msg.setText("Time taken: %.1f seconds" % duration)
        msg.setWindowTitle("Stroop Game")
        msg.setStandardButtons(gui.QMessageBox.Ok)
        msg.exec_()

    # ------------------------------------------ Sally Anne functions -------------------------------------
    def set_sally_anne_english(self):
        self._maltese = False
        self.sally_anne_populate_ui()

    def set_sally_anne_maltese(self):
        self._maltese = True
        self.sally_anne_populate_ui()

    def sally_anne_populate_ui(self):
        """ Populate Sally Anne Game UI in either maltese or english """

        if self._maltese:
            self._main_widget.sally_anne_instructions_label.setText(
                unicode(self._sally_anne_maltese_text["instructions"]))
            self._main_widget.sally_anne_explanation_label.setText(
                unicode(self._sally_anne_maltese_text["story"]))
            self._main_widget.start_sally_anne_button.setText(unicode("Ibda"))
            self._main_widget.sally_anne_next_button.setText(unicode("Li jmiss"))
            self._main_widget.sally_anne_play_again_button.setText(unicode("Li jmiss"))
        else:
            self._main_widget.sally_anne_instructions_label.setText(self._sally_anne_english_text["instructions"])
            self._main_widget.sally_anne_explanation_label.setText(
                unicode(self._sally_anne_english_text["story"]))
            self._main_widget.start_sally_anne_button.setText("Start")
            self._main_widget.sally_anne_next_button.setText("Next")
            self._main_widget.sally_anne_play_again_button.setText(unicode("Next"))

        self._main_widget.sally_anne_english_button.setVisible(False)
        self._main_widget.sally_anne_maltese_button.setVisible(False)
        self._main_widget.sally_anne_instructions_label.setVisible(True)
        self._main_widget.start_sally_anne_button.setVisible(True)
        self._sally_anne_page_index = 0

    def select_sally_anne(self):
        """ Switch to Sally Anne screen """
        self._main_widget.main_stacked_widget.setCurrentIndex(3)
        self._main_widget.sally_anne_stacked_widget.setCurrentIndex(0)
        self._main_widget.sally_anne_instructions_label.setVisible(False)
        self._main_widget.sally_anne_english_button.setVisible(True)
        self._main_widget.sally_anne_maltese_button.setVisible(True)
        self._main_widget.start_sally_anne_button.setVisible(False)
        self._sally_anne_page_index = 0

    def start_sally_anne_game(self):
        """ Start Sally Anne game """
        if self._sally_anne_page_index == 1:
            return self.sally_anne_move_slide()

        if self._maltese:
            self._main_widget.sally_anne_instructions_label.setText(
                unicode(self._sally_anne_maltese_text["sally_anne_0"]))
            self._main_widget.start_sally_anne_button.setText(unicode("Li jmiss"))
        else:
            self._main_widget.sally_anne_instructions_label.setText(self._sally_anne_english_text["sally_anne_0"])
            self._main_widget.start_sally_anne_button.setText("Next")

        self._sally_anne_page_index += 1

    def sally_anne_move_slide(self):
        """ Move Sally Anne image index """
        if self._sally_anne_page_index == 1:
            self._main_widget.sally_anne_stacked_widget.setCurrentIndex(1)

        # Load next image
        if self._sally_anne_page_index < 9:
            x, y = self._sally_anne_image_dimensions[self._sally_anne_page_index]
            if self._maltese:
                pixmap = gui.QPixmap('images/sally_anne_maltese/sally_anne_%d.jpg' %
                                     self._sally_anne_page_index)
                pixmap = pixmap.scaled(x, y, core.Qt.KeepAspectRatio)
                self._main_widget.sally_anne_image_placeholder.setPixmap(pixmap)
                self._main_widget.sally_anne_image_caption.setText(
                    self._sally_anne_maltese_text[unicode("sally_anne_%d" % self._sally_anne_page_index)])
            else:
                pixmap = gui.QPixmap('images/sally_anne_english/sally_anne_%d.jpg' %
                                     self._sally_anne_page_index)
                pixmap = pixmap.scaled(x, y, core.Qt.KeepAspectRatio)
                self._main_widget.sally_anne_image_placeholder.setPixmap(pixmap)
                self._main_widget.sally_anne_image_caption.setText(
                    self._sally_anne_english_text["sally_anne_%d" % self._sally_anne_page_index])
        else:
            self.sally_anne_question_page()

        self._sally_anne_page_index += 1

    def sally_anne_question_page(self):
        """ Sally Anne question page """
        self._main_widget.sally_anne_stacked_widget.setCurrentIndex(2)
        if self._maltese:
            self._main_widget.sally_anne_question.setText(unicode(self._sally_anne_maltese_text['question']))
        else:
            self._main_widget.sally_anne_question.setText(self._sally_anne_english_text['question'])

        # Set pixmaps for Sally Anne answer buttons
        language = 'maltese' if self._maltese else 'english'
        self._main_widget.sally_anne_answer_1_button.setIcon(gui.QIcon('images/sally_anne_%s/basket.jpg' % language))
        self._main_widget.sally_anne_answer_1_button.setIconSize(self._main_widget.sally_anne_answer_1_button.size())
        self._main_widget.sally_anne_answer_1_button.setText("")

        self._main_widget.sally_anne_answer_2_button.setIcon(gui.QIcon('images/sally_anne_%s/box.jpg' % language))
        self._main_widget.sally_anne_answer_2_button.setIconSize(self._main_widget.sally_anne_answer_2_button.size())
        self._main_widget.sally_anne_answer_2_button.setText("")

    def sally_anne_answer_1_pressed(self):
        """ Answer 1 was pressed """
        self._sally_anne_answer = 1
        self.sally_anne_evaluate_answer()

    def sally_anne_answer_2_pressed(self):
        """ Answer 1 was pressed """
        self._sally_anne_answer = 2
        self.sally_anne_evaluate_answer()

    def sally_anne_evaluate_answer(self):
        """ Evaluate answer for Sally Anne game """
        if self._sally_anne_answer == 1:
            report = "Correct answer"
        else:
            report = "Incorrent answer"

        msg = gui.QMessageBox()
        msg.setIcon(gui.QMessageBox.Information)
        msg.setText(report)
        msg.setWindowTitle("Sally Anne Game")
        msg.setStandardButtons(gui.QMessageBox.Ok)
        msg.exec_()

        # Switch to next page
        self._sally_anne_page_index = 0
        self._main_widget.sally_anne_stacked_widget.setCurrentIndex(3)
        self._main_widget.sally_anne_change_game_button.setVisible(False)

    def sally_anne_final_page(self):
        """ Final page of sally anne game """
        self._main_widget.sally_anne_change_game_button.setVisible(True)
        if self._sally_anne_page_index == 0:
            if self._maltese:
                self._main_widget.sally_anne_play_again_button.setText(u"Erga Ilgħab")
                self._main_widget.sally_anne_change_game_button.setText(u"Biddel il-Logħoba")
                self._main_widget.sally_anne_explanation_label.setText(
                    unicode(self._sally_anne_maltese_text["explanation"]))
            else:
                self._main_widget.sally_anne_play_again_button.setText("Play Again")
                self._main_widget.sally_anne_explanation_label.setText(
                    unicode(self._sally_anne_english_text["explanation"]))
                self._main_widget.sally_anne_change_game_button.setText("Change Game")
            self._sally_anne_page_index = 1
        else:
            self._main_widget.sally_anne_stacked_widget.setCurrentIndex(0)
            self._main_widget.sally_anne_english_button.setVisible(True)
            self._main_widget.sally_anne_maltese_button.setVisible(True)
            self._main_widget.sally_anne_instructions_label.setVisible(False)
            self._main_widget.start_sally_anne_button.setVisible(False)
            self._sally_anne_page_index = 0


# Application entry point
if __name__ == "__main__":
    app = gui.QApplication(sys.argv)
    app.setApplicationName("Cognition Games")
    app.setWindowIcon(gui.QIcon('cognition_games.jpg'))
    plotter = CognitionGames("cognition_games.ui")
    sys.exit(app.exec_())
