#!/usr/bin/env python
"""
File name: main.py
Author: Seth Christie
Created: 2024-08-17
Version: 1.0
"""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSpacerItem
from PyQt6.QtGui import QFont
import qdarktheme

from frames import schedule_frame
from frames import builder_frame
from frames import course_frame


# ----------------------------------------------------- classes --------------------------------------------------------

class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.create_window()
        self.layout = QVBoxLayout()

        # create title widget
        self.title_font = QFont('Helvetica', 24)
        self.title_font.setBold(True)

        self.title_label = QLabel(parent=self, text="Scheduler Tool")
        self.title_label.setFont(QFont('Helvetica', 24))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # add frames to layout
        self.schedule_frame = schedule_frame.ScheduleFrame(self)
        self.layout.addWidget(self.schedule_frame)
        self.layout.addItem(QSpacerItem(0, 20))

        self.degreeworks_frame = builder_frame.BuilderFrame(self)
        self.layout.addWidget(self.degreeworks_frame)
        self.layout.addItem(QSpacerItem(0, 20))

        self.course_frame = course_frame.CourseFrame(self)
        self.layout.addWidget(self.course_frame)
        self.layout.addItem(QSpacerItem(0, 20))

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)  # set alignment of layout
        self.setLayout(self.layout)  # set layout of widget

    def create_window(self):
        """Creates the main window."""
        self.resize(600, 800)
        self.setFixedSize(600, 800)
        self.setWindowTitle("Scheduler Tool")

        self.setPalette(qdarktheme.load_palette('dark'))
        self.setStyleSheet(qdarktheme.load_stylesheet())

    def center(self):
        """Centers the window on the screen."""
        qt = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qt.moveCenter(cp)
        self.move(qt.topLeft())


# ---------------------------------------------------- functions -------------------------------------------------------

def main():
    app = QApplication(sys.argv)  # create application
    ex = Application()
    ex.show()  # show window
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
