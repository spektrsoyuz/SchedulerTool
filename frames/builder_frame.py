#!/usr/bin/env python
"""
File name: builder_frame.py
Author: Seth Christie
Created: 2024-08-19
Version: 1.0
"""
import json

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QSpacerItem, QComboBox

from abstract_frame import AbstractFrame


# ----------------------------------------------------- classes --------------------------------------------------------

class BuilderFrame(AbstractFrame):
    def __init__(self, parent, title="Schedule Builder"):
        super().__init__(parent, title)
        row = 0

        # fetch degree requirements
        with open("data/degree-requirements.json", 'r') as self.degree_reqs:
            self.degree_reqs = json.load(self.degree_reqs)

        # fetch concentrations
        with open("data/concentrations.json", 'r') as self.concentrations:
            self.concentrations = json.load(self.concentrations)

        # name label
        self.name_label = QLabel(parent=self, text="Name: ")
        self.name_label.setFont(self.font)
        self.layout.addWidget(self.name_label, row, 0)

        # name input
        self.name_input = QLineEdit(parent=self)
        self.name_input.setFont(self.font)
        self.name_input.textEdited.connect(self.clear_status)
        self.name_input.setText("Student")
        self.layout.addWidget(self.name_input, row, 1)
        row += 1

        # majors label
        self.majors_label = QLabel(parent=self, text="Majors: ")
        self.majors_label.setFont(self.font)
        self.layout.addWidget(self.majors_label, row, 0)

        # majors input
        self.majors_options = list(self.degree_reqs.keys())
        self.majors_dropdown = QComboBox(parent=self)
        self.majors_dropdown.setFont(self.font)
        self.majors_dropdown.addItems(self.majors_options)
        self.majors_dropdown.currentIndexChanged.connect(self.update_concentrations)
        self.majors_dropdown.setCurrentIndex(0)
        self.layout.addWidget(self.majors_dropdown, row, 1)
        row += 1

        # concentration label
        self.concentration_label = QLabel(parent=self, text="Concentration: ")
        self.concentration_label.setFont(self.font)
        self.layout.addWidget(self.concentration_label, row, 0)

        # concentration input
        self.concentration_dropdown = QComboBox(parent=self)
        self.concentration_dropdown.setFont(self.font)
        self.concentration_dropdown.setCurrentIndex(0)
        self.layout.addWidget(self.concentration_dropdown, row, 1)

        # set initial concentrations
        initial_major = self.majors_options[0]
        initial_concentrations = self.concentrations.get(initial_major, 0)
        self.concentration_dropdown.addItems(initial_concentrations)
        row += 1

        # courses label
        self.courses_label = QLabel(parent=self, text="Courses:")
        self.courses_label.setFont(self.font)
        self.layout.addWidget(self.courses_label, row, 0)

        # courses input
        self.courses_input = QLineEdit(parent=self)
        self.courses_input.setFont(self.font)
        self.courses_input.textEdited.connect(self.clear_status)
        self.courses_input.setText("")
        self.layout.addWidget(self.courses_input, row, 1)
        row += 1

        # standing label
        self.standing_label = QLabel(parent=self, text="Standing: ")
        self.standing_label.setFont(self.font)
        self.layout.addWidget(self.standing_label, row, 0)

        # standing input
        self.standing_options = ["Freshman I", "Freshman II", "Sophomore I",
                                 "Sophomore II", "Junior I", "Junior II",
                                 "Senior I", "Senior II", "Senior III"]
        self.standing_dropdown = QComboBox(parent=self)
        self.standing_dropdown.setFont(self.font)
        self.standing_dropdown.addItems(self.standing_options)
        self.standing_dropdown.setCurrentIndex(0)
        self.layout.addWidget(self.standing_dropdown, row, 1)
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
        self.status_label = QLabel(parent=self, text="")
        self.status_label.setFont(self.font)
        self.layout.addWidget(self.status_label, row, 1, 1, 2)
        row += 1

    def create_schedule(self):
        """Creates the Schedule based on provided options"""
        name = self.name_input.text()
        self.status_label.setStyleSheet("color: rgb(179, 235, 242);")
        self.status_label.setText("Creating Schedule...")

        if name == "":
            self.status_label.setStyleSheet("color: rgb(255, 105, 97);")
            self.status_label.setText("Please provide a name.")
            return

        # print(self.degree_reqs)
        # print(self.concentrations)

        # TODO create schedule functionality

        self.status_label.setStyleSheet("color: rgb(119, 221, 119);")
        self.status_label.setText("Schedule created")

    def update_concentrations(self):
        """Updates the concentration dropdown based on the selected major."""
        selected_major = self.majors_dropdown.currentText()
        concentrations = self.concentrations.get(selected_major, 0)

        self.concentration_dropdown.clear()
        self.concentration_dropdown.addItems(concentrations)

    def clear_status(self):
        """Clears the status label"""
        self.status_label.setText("")
