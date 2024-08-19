#!/usr/bin/env python
"""
File name: builder_frame.py
Author: Seth Christie
Created: 2024-08-19
Version: 1.0
"""
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGroupBox, QGridLayout


class AbstractFrame(QGroupBox):
    def __init__(self, parent, title):
        super().__init__()
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.font = QFont('Helvetica', 12)
        self.setTitle(title)
        self.setFont(QFont('Helvetica', 10))
