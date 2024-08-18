#!/usr/bin/env python
"""
File name: frames.py
Author: Seth Christie
Created: 2024-08-17
Version: 1.0
"""
import json
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGridLayout, QLineEdit, QPushButton, QSpacerItem, QFileDialog, QGroupBox, \
    QScrollArea


# ----------------------------------------------------- classes --------------------------------------------------------

class ScheduleFrame(QGroupBox):
    def __init__(self, parent, title="Scheduling Tools"):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.font = QFont('Helvetica', 12)
        self.setTitle(title)
        self.setFont(QFont('Helvetica', 10))

        row = 0

        # url label
        self.url_label = QLabel(parent=self, text="Schedule URL: ")
        self.url_label.setFont(self.font)
        self.layout.addWidget(self.url_label, row, 0)

        # url input
        self.url_input = QLineEdit(parent=self)
        self.url_input.setFont(self.font)
        self.url_input.setText("https://docs.google.com/spreadsheets/")
        self.url_input.textEdited.connect(self.clear_labels)
        self.layout.addWidget(self.url_input, row, 1)
        row += 1

        # sheet name label
        self.sheet_label = QLabel(parent=self, text="Sheet Name: ")
        self.sheet_label.setFont(self.font)
        self.layout.addWidget(self.sheet_label, row, 0)

        # sheet name input
        self.sheet_input = QLineEdit(parent=self)
        self.sheet_input.setFont(self.font)
        self.sheet_input.setText("Sheet1")
        self.sheet_input.textEdited.connect(self.clear_labels)
        self.layout.addWidget(self.sheet_input, row, 1)
        row += 1

        # add spacer
        self.layout.addItem(QSpacerItem(120, 20), row, 0)
        row += 1

        # export button
        self.export_button = QPushButton(parent=self, text="Export")
        self.export_button.setFont(self.font)
        self.export_button.setFixedWidth(90)
        self.layout.addWidget(self.export_button, row, 0)

        # export status label
        self.export_label = QLabel(parent=self, text="")
        self.export_label.setFont(self.font)
        self.layout.addWidget(self.export_label, row, 1, 1, 2)
        row += 1

        # validate button
        self.validate_button = QPushButton(parent=self, text="Validate")
        self.validate_button.setFont(self.font)
        self.validate_button.setFixedWidth(90)
        self.layout.addWidget(self.validate_button, row, 0)

        # validate status label
        self.validate_label = QLabel(parent=self, text="")
        self.validate_label.setFont(self.font)
        self.layout.addWidget(self.validate_label, row, 1, 1, 2)
        row += 1

        # import button
        self.import_button = QPushButton(parent=self, text="Import")
        self.import_button.setFont(self.font)
        self.import_button.setFixedWidth(90)
        self.layout.addWidget(self.import_button, row, 0)

        # import status label
        self.import_label = QLabel(parent=self, text="")
        self.import_label.setFont(self.font)
        self.layout.addWidget(self.import_label, row, 1, 1, 2)
        row += 1

    def clear_labels(self):
        self.export_label.setText("")
        self.validate_label.setText("")


class BuilderFrame(QGroupBox):
    def __init__(self, parent, title="Schedule Builder"):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.font = QFont('Helvetica', 12)
        self.setTitle(title)
        self.setFont(QFont('Helvetica', 10))

        row = 0

        # name label
        self.name_label = QLabel(parent=self, text="Name: ")
        self.name_label.setFont(self.font)
        self.layout.addWidget(self.name_label, row, 0)

        # name input
        self.name_input = QLineEdit(parent=self)
        self.name_input.setFont(self.font)
        self.name_input.textEdited.connect(self.clear_labels)
        self.name_input.setText("Student")
        self.layout.addWidget(self.name_input, row, 1)
        row += 1

        # majors label
        self.majors_label = QLabel(parent=self, text="Majors: ")
        self.majors_label.setFont(self.font)
        self.layout.addWidget(self.majors_label, row, 0)

        # majors input
        self.majors_input = QLineEdit(parent=self)
        self.majors_input.setFont(self.font)
        self.majors_input.textEdited.connect(self.clear_labels)
        self.majors_input.setText("ME")
        self.layout.addWidget(self.majors_input, row, 1)
        row += 1

        # courses label
        self.courses_label = QLabel(parent=self, text="Courses:")
        self.courses_label.setFont(self.font)
        self.layout.addWidget(self.courses_label, row, 0)

        # courses input
        self.courses_input = QLineEdit(parent=self)
        self.courses_input.setFont(self.font)
        self.courses_input.textEdited.connect(self.clear_labels)
        self.courses_input.setText("")
        self.layout.addWidget(self.courses_input, row, 1)
        row += 1

        # standing label
        self.standing_label = QLabel(parent=self, text="Standing: ")
        self.standing_label.setFont(self.font)
        self.layout.addWidget(self.standing_label, row, 0)

        # standing input
        self.standing_input = QLineEdit(parent=self)
        self.standing_input.setFont(self.font)
        self.standing_input.textEdited.connect(self.clear_labels)
        self.standing_input.setText("Freshman I")
        self.layout.addWidget(self.standing_input, row, 1)
        row += 1

        # add spacer
        self.layout.addItem(QSpacerItem(120, 20), row, 0)
        row += 1

        # create button
        self.create_button = QPushButton(parent=self, text="Create")
        self.create_button.setFont(self.font)
        self.create_button.setFixedWidth(90)
        self.create_button.clicked.connect(self.create_schedule)
        self.layout.addWidget(self.create_button, row, 0)

        # create status label
        self.create_label = QLabel(parent=self, text="")
        self.create_label.setFont(self.font)
        self.layout.addWidget(self.create_label, row, 1, 1, 2)
        row += 1

    def create_schedule(self):
        name = self.name_input.text()
        self.create_label.setStyleSheet("color: rgb(179, 235, 242);")
        self.create_label.setText("Creating Schedule...")

        if name == "":
            self.create_label.setStyleSheet("color: rgb(255, 105, 97);")
            self.create_label.setText("Please provide a name.")
            return

        with open("data/degree-requirements.json", 'r') as degree_reqs:
            degree_reqs = json.load(degree_reqs)
        print(degree_reqs)

        # TODO create schedule functionality

        self.create_label.setStyleSheet("color: rgb(119, 221, 119);")
        self.create_label.setText("Schedule created!")

    def clear_labels(self):
        self.create_label.setText("")


class CourseFrame(QGroupBox):
    def __init__(self, parent, title="Course Tools"):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.font = QFont('Helvetica', 12)
        self.setTitle(title)
        self.setFont(QFont('Helvetica', 10))
