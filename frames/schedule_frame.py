#!/usr/bin/env python
"""
File name: schedule_frame.py
Author: Seth Christie
Created: 2024-08-19
Version: 1.0
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem

import utils
from abstract_frame import AbstractFrame


# ----------------------------------------------------- classes --------------------------------------------------------

class ScheduleFrame(AbstractFrame):
    def __init__(self, parent, title="Scheduling Tools"):
        super().__init__(parent, title)
        row = 0

        # url label
        self.url_label = QLabel(parent=self, text="Schedule URL: ")
        self.url_label.setFont(self.font)
        self.layout.addWidget(self.url_label, row, 0)

        # url input
        self.url_input = QLineEdit(parent=self)
        self.url_input.setFont(self.font)
        self.url_input.setText("https://docs.google.com/spreadsheets/")
        self.url_input.textEdited.connect(self.clear_status)
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
        self.sheet_input.textEdited.connect(self.clear_status)
        self.layout.addWidget(self.sheet_input, row, 1)
        row += 1

        # add spacer
        self.layout.addItem(QSpacerItem(120, 20), row, 0)
        row += 1

        self.button_layout = QHBoxLayout()  # create new layout for buttons

        # export button
        self.export_button = QPushButton(parent=self, text="Export")
        self.export_button.setFont(self.font)
        self.export_button.setFixedWidth(90)
        self.export_button.clicked.connect(self.export)
        self.button_layout.addWidget(self.export_button)

        # validate button
        self.validate_button = QPushButton(parent=self, text="Validate")
        self.validate_button.setFont(self.font)
        self.validate_button.setFixedWidth(90)
        self.button_layout.addWidget(self.validate_button)

        # import button
        self.import_button = QPushButton(parent=self, text="Import")
        self.import_button.setFont(self.font)
        self.import_button.setFixedWidth(90)
        self.button_layout.addWidget(self.import_button)
        row += 1

        self.layout.addLayout(self.button_layout, row, 0, 1, 2,
                              alignment=Qt.AlignmentFlag.AlignLeft)  # add button layout to layout
        row += 1

        # status label
        self.status_label = QLabel(parent=self, text="")
        self.status_label.setFont(self.font)
        self.layout.addWidget(self.status_label, row, 0, 1, 2)

    def clear_status(self):
        """Clears the status label"""
        self.status_label.setText("")

    def export(self):
        schedule = utils.schedule_request(self.url_input.text(), self.sheet_input.text())

        if schedule == -1:
            self.status_label.setStyleSheet("color: rgb(255, 105, 97);")
            self.status_label.setText("Please provide a name.")
            return

        utils.save_schedule_to_file(schedule)
        self.status_label.setStyleSheet("color: rgb(119, 221, 119);")
        self.status_label.setText(f"Saved Schedule to exports/{schedule["Name"]}.json")