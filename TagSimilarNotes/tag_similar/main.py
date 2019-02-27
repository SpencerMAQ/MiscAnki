# -*- coding: utf-8 -*-

# This file is part of the 'Tag Similar Notes' add-on for Anki
# Copyright: SpencerMAQ (Michael Spencer Quinto) <spencer.michael.q@gmail.com> 2019
# License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html

from aqt.qt import *
from aqt import mw
from aqt.utils import showInfo
from aqt.addons import AddonManager

import difflib
import os
import sys
import json
import logging

from .utils import setup_logger
from .utils import calculate_time
from .utils import open_log_file
from .utils import trace_calls

if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
    from functools import lru_cache

try:
    from PyQt4 import QtCore
    _from_utf8 = QtCore.QString.fromUtf8
except (AttributeError, ImportError):
    def _from_utf8(s):
        return s

__version__ = '0.0'
# Feb 27 2019

# HOTKEY              = 'Shift+P'
TAG_TO_ADD          = 'Rescheduled_by_Push_Existing_Vocab'

# ===================== DO NOT EDIT BEYOND THIS LINE ===================== #
UNMATCHED_FORMAT = logging.Formatter('%(message)s')

addon_mgr_instance = AddonManager(mw)
ADD_ON_PATH = addon_mgr_instance.addonsFolder()
PUSH_EXISTING_PATH = ADD_ON_PATH + r'\push_existing'

if not os.path.exists(PUSH_EXISTING_PATH):
    os.makedirs(PUSH_EXISTING_PATH)

NEW_PATH = os.path.join(ADD_ON_PATH, 'push_existing')

CONFIG_PATH = os.path.join(NEW_PATH, 'push_existing_config.json')  # doesn't work on json?? but works for log
LOG_PATH = os.path.join(NEW_PATH, 'push_existing.log')
UNMATCHED_LOG_PATH = os.path.join(NEW_PATH, 'unmatched_vocab.log')

main_logger = setup_logger('main_logger', LOG_PATH)
unmatched_logger = setup_logger('unmatched_logger', UNMATCHED_LOG_PATH, _format=UNMATCHED_FORMAT)

del addon_mgr_instance

# ===================== TEMPORARY STUFF ===================== #
if False:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from anki.storage import Collection

    class Temporary:
        def __init__(self):
            self.col = Collection('', log=True)

    mw = Temporary()

# ===================== TEMPORARY STUFF ===================== #

class PushCards(QDialog):
    def __init__(self, parent):
        self._init_buttons()
        self._init_json()
        self._init_signals()
        self._init_ui()

    @trace_calls
    def _init_json(self):
        pass

    @trace_calls
    def _init_buttons(self):
        """QtGui/QtWidget elements"""
        pass

    @trace_calls
    def _init_signals(self):
        pass

    @trace_calls
    def _init_ui(self):
        """Initialize Layout"""
        pass

    @trace_calls
    def tag_similar_cards(self):
        pass

    @trace_calls
    def closeEvent(self, QCloseEvent):
        """Creates a JSON file if it doesn't exist
        Otherwise, saves the QComboBox and QRadioButton settings
        Due to difficulties in lookup when dealing with delimiters such as \n or \t
        the __delimiter stored inside the JSON file is based
        on a reverse lookup an a global dictionary DELIMITER_DICT
        On initialization, __init_json looks for the actual delimiter based on the key
        which was based on reverse lookup
        Skips the Yes/No Prompt if the settings are the same as the JSON file
        Args:
            QCloseEvent:        I have no idea what this is
        """
        # https://stackoverflow.com/questions/2568673/inverse-dictionary-lookup-in-python
        __delimiter = next(key for key, value in DELIMITER_DICT.items() if value == self.delimiter) \
            if self.delimiter else ''

        # TODO: Edit conf, is this even needed?
        conf = {'default_model':            self.selected_model,
                'default_field_to_match':   self.field_to_match,
                'default_num_of_cards':     self.number_of_cards_to_resched_per_note,
                'default_delimiter':        __delimiter,
                'enable_add_tag':           self.enable_add_note_tag,
                'default_encoding':         self.encoding,
                'preferred_csv_loc':        self.preferred_csv_directory
                }

        '''Skip prompt if the settings are the same, but check first if it exists to avoid IOError'''
        if os.path.isfile(NEW_PATH + r'\push_existing.json'):
            with open(NEW_PATH + r'\push_existing.json', mode='r') as __hf:
                __fnoc = json.load(__hf)
                if all([__fnoc[key] == conf[key] for key, value in conf.items()]):
                    return

        # https://stackoverflow.com/questions/14834494/pyqt-clicking-x-doesnt-trigger-closeevent
        reply = QMessageBox.question(self, 'Save Settings',
                                     'Would you like to save your config settings?\n'
                                     'Click \'No\' to retain your previous settings',
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            with open(NEW_PATH + r'\push_existing.json', mode='w') as fh:
                json.dump(conf,
                          fh,
                          indent=4,
                          separators=(',', ': ')
                          )



def init_window():
    mw.push_cards = PushCards(mw)

run_action = QAction('Push Existing Vocabulary', mw)
run_action.setShortcut(QKeySequence(HOTKEY))
run_action.triggered.connect(init_window)

mw.form.menuTools.addAction(run_action)
