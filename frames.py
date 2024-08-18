#!/usr/bin/env python
"""
File name: frames.py
Author: Seth Christie
Created: 2024-08-17
Version: 1.0
"""
import json
from pathlib import Path

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGridLayout, QLineEdit, QPushButton, QSpacerItem, QFileDialog, QGroupBox


# ----------------------------------------------------- classes --------------------------------------------------------

class ScheduleFrame(QGroupBox):
    def __init__(self, parent, title="Scheduling Tools"):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.font = QFont('Helvetica', 12)
        self.setTitle(title)
        self.setFont(QFont('Helvetica', 10))

        # url label
        self.url_label = QLabel(parent=self, text="Schedule URL: ")
        self.url_label.setFont(self.font)
        self.layout.addWidget(self.url_label, 0, 0)

        # url input
        self.url_input = QLineEdit(parent=self)
        self.url_input.setFont(self.font)
        self.url_input.setText("https://docs.google.com/spreadsheets/")
        self.url_input.textEdited.connect(self.clear_labels)
        self.layout.addWidget(self.url_input, 0, 1)

        # sheet name label
        self.sheet_label = QLabel(parent=self, text="Sheet Name: ")
        self.sheet_label.setFont(self.font)
        self.layout.addWidget(self.sheet_label, 1, 0)

        # sheet name input
        self.sheet_input = QLineEdit(parent=self)
        self.sheet_input.setFont(self.font)
        self.sheet_input.setText("Sheet1")
        self.sheet_input.textEdited.connect(self.clear_labels)
        self.layout.addWidget(self.sheet_input, 1, 1)

        # add spacer
        self.layout.addItem(QSpacerItem(120, 20), 2, 0)

        # export button
        self.export_button = QPushButton(parent=self, text="Export")
        self.export_button.setFont(self.font)
        self.export_button.setFixedWidth(90)
        self.layout.addWidget(self.export_button, 3, 0)

        # export status label
        self.export_label = QLabel(parent=self, text="")
        self.export_label.setFont(self.font)
        self.layout.addWidget(self.export_label, 3, 1, 1, 2)

        # validate button
        self.validate_button = QPushButton(parent=self, text="Validate")
        self.validate_button.setFont(self.font)
        self.validate_button.setFixedWidth(90)
        self.layout.addWidget(self.validate_button, 4, 0)

        # validate status label
        self.validate_label = QLabel(parent=self, text="")
        self.validate_label.setFont(self.font)
        self.layout.addWidget(self.validate_label, 4, 1, 1, 2)

        # import button
        self.import_button = QPushButton(parent=self, text="Import")
        self.import_button.setFont(self.font)
        self.import_button.setFixedWidth(90)
        self.layout.addWidget(self.import_button, 5, 0)

        # import status label
        self.import_label = QLabel(parent=self, text="")
        self.import_label.setFont(self.font)
        self.layout.addWidget(self.import_label, 5, 1, 1, 2)

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

        # file label
        self.file_label = QLabel(parent=self, text="Select File: ")
        self.file_label.setFont(self.font)
        self.layout.addWidget(self.file_label, 0, 0)

        # file input
        self.file_input = QLineEdit(parent=self)
        self.file_input.setFont(self.font)
        self.file_input.textEdited.connect(self.clear_labels)
        self.layout.addWidget(self.file_input, 0, 1)

        # file browse button
        self.file_button = QPushButton(parent=self, text="Browse")
        self.file_button.setFont(self.font)
        self.file_button.clicked.connect(self.browse_file)
        self.file_button.clicked.connect(self.clear_labels)
        self.layout.addWidget(self.file_button, 0, 2)

        # add spacer
        self.layout.addItem(QSpacerItem(120, 20), 1, 0)

        # create button
        self.create_button = QPushButton(parent=self, text="Create")
        self.create_button.setFont(self.font)
        self.create_button.setFixedWidth(90)
        self.create_button.clicked.connect(self.create_schedule)
        self.layout.addWidget(self.create_button, 2, 0)

        # create status label
        self.create_label = QLabel(parent=self, text="")
        self.create_label.setFont(self.font)
        self.layout.addWidget(self.create_label, 2, 1, 1, 2)

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)"
        )
        if filename:
            self.file_input.setText(filename)
            self.create_label.setText("")

    def create_schedule(self):
        filename = self.file_input.text()
        self.create_label.setStyleSheet("color: rgb(179, 235, 242);")
        self.create_label.setText("Creating Schedule...")

        if filename == "":
            self.create_label.setStyleSheet("color: rgb(255, 105, 97);")
            self.create_label.setText("Please select a file.")
            return

        if not Path(filename).is_file():
            self.create_label.setStyleSheet("color: rgb(255, 105, 97);")
            displayed_name = filename
            if len(filename) > 32:
                displayed_name = displayed_name[:32] + "..."
            self.create_label.setText("File " + displayed_name + " was not found.")
            return

        with open("D:/PyCharm/SchedulerTool/data/degree-requirements.json", 'r') as degree_reqs:
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
