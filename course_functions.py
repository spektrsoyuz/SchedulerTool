#!/usr/bin/env python
"""
File name: course_functions.py
Author: Seth Christie
Created: 2024-08-19
Version: 1.0
"""
from bs4 import BeautifulSoup

import utils


def get_course_data(http_response):
    """Create a dictionary of multiple courses from a provided http page"""
    courseblocks = BeautifulSoup(http_response.text, 'html.parser').find_all('div', 'courseblock')
    courses = {}

    # iterate over each courseblock
    for courseblock in courseblocks:
        course = get_course(courseblock)
        courses[course.get('id')] = course

    return courses


def get_course(courseblock):
    """Create a dictionary of a single course from a html courseblock"""
    courseblocktitle = courseblock.find('p', 'courseblocktitle').text.split('\xa0')
    courseblockdesc = str(courseblock.find('p', 'courseblockdesc')).split('<br/>')

    coreqs = 'None'
    prereqs = 'None'
    standing = 'None'
    desc = utils.strip_html(courseblockdesc[-3]).replace('\n', ' ')

    for line in desc.split('\n'):
        # check for class standing
        if 'Minimum Class Standing:' in line:
            standing = line.split(':')[1].strip()

        # check for prereqs
        if 'Prerequisites:' in line:
            prereqs = utils.strip_html(line).replace('Prerequisites: ', '')

        # check for coreqs
        if 'Corequisites:' in line:
            coreqs = utils.strip_html(line).replace('Corequisites: ', '')

    # check if course is a special topics course
    if '391' in courseblocktitle[0]:
        desc = 'None'

    return {
        'id': courseblocktitle[0],
        'name': courseblocktitle[2].replace('\n', ''),
        'coreqs': coreqs.replace('\n', ''),
        'prereqs': prereqs.replace('\n', ''),
        'standing': standing,
        'desc': desc.replace('  ', ' '),
        'credits': courseblocktitle[-1].replace(' Credits', '')
    }
