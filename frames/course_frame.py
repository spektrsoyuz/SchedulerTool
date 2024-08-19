#!/usr/bin/env python
"""
File name: course_frame.py
Author: Seth Christie
Created: 2024-08-19
Version: 1.0
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton
from threading import Thread

import utils
from abstract_frame import AbstractFrame
from course_functions import get_course_data


# ---------------------------------------------------- functions -------------------------------------------------------

def start_thread(function):
    thread = Thread(target=function)
    thread.start()


# ----------------------------------------------------- classes --------------------------------------------------------

class CourseFrame(AbstractFrame):
    def __init__(self, parent, title="Course Tools"):
        super().__init__(parent, title)
        row = 0

        # download courses button
        self.download_courses_button = QPushButton(parent=self, text="Download Courses")
        self.download_courses_button.setFont(self.font)
        self.download_courses_button.setFixedWidth(160)
        self.download_courses_button.clicked.connect(self.start_course_download)
        self.layout.addWidget(self.download_courses_button, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        row += 1

        # download majors button
        self.download_majors_button = QPushButton(parent=self, text="Download Majors")
        self.download_majors_button.setFont(self.font)
        self.download_majors_button.setFixedWidth(160)
        self.download_majors_button.clicked.connect(self.download_majors)
        self.layout.addWidget(self.download_majors_button, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        row += 1

        # export me electives button
        self.export_me_electives_button = QPushButton(parent=self, text="Export ME Electives")
        self.export_me_electives_button.setFont(self.font)
        self.export_me_electives_button.setFixedWidth(160)
        self.export_me_electives_button.clicked.connect(self.export_me_electives)
        self.layout.addWidget(self.export_me_electives_button, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        row += 1

        # export cs electives button
        self.export_cs_electives_button = QPushButton(parent=self, text="Export CS Electives")
        self.export_cs_electives_button.setFont(self.font)
        self.export_cs_electives_button.setFixedWidth(160)
        self.export_me_electives_button.clicked.connect(self.export_cs_electives)
        self.layout.addWidget(self.export_cs_electives_button, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        row += 1

    def start_course_download(self):
        download_thread = Thread(target=self.download_courses)
        download_thread.start()

    def download_courses(self):
        """Download courses.json from Kettering Courses A-Z"""
        self.download_courses_button.setEnabled(False)
        course_list = {}
        subjects = ['ACCT', 'BIOL', 'BUSN', 'CE', 'CHME', 'CHEM', 'CILE', 'COMM', 'CS', 'ECON', 'ECE', 'EE', 'ENGR',
                    'EP', 'FINC', 'HIST', 'HUMN', 'IME', 'ISYS', 'LANG', 'LA', 'LIT', 'MATH', 'MECH', 'MEDI', 'MFGO',
                    'MGMT', 'MKRT', 'PHIL', 'PHYS', 'PSYC', 'SSCI', 'SOC']
        for subj in subjects:
            url_undergrad = f'https://catalog.kettering.edu/coursesaz/undergrad/{subj.lower()}'
            url_grad = f'https://catalog.kettering.edu/coursesaz/grad/{subj.lower()}'

            undergrad_list = {}
            grad_list = {}
            try:
                print(f'Requesting {url_undergrad}.')
                undergrad_list = get_course_data(utils.http_request(url_undergrad))
            except TypeError:
                pass

            try:
                print(f'Requesting {url_grad}.')
                grad_list = get_course_data(utils.http_request(url_grad))
            except TypeError:
                pass

            course_list[subj] = {**undergrad_list, **grad_list}

        print('Downloaded course list to courses.json.')
        utils.save_courses_to_file(course_list)
        self.download_courses_button.setEnabled(True)

    def download_majors(self):
        """Download degree-requirements.json and concentrations.json from Kettering Courses A-Z"""
        pass

    def export_me_electives(self):
        """Export ME Electives from courses.json to excel file"""
        pass

    def export_cs_electives(self):
        """Export CS Electives from courses.json to excel file"""
        pass
