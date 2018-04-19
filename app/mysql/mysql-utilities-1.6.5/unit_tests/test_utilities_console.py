#
# Copyright (c) 2013, 2016, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#

import os
import sys
import unittest

from mysql.utilities.common.console import _WIN_COMMAND_KEY
from mysql.utilities.command.utilitiesconsole import UtilitiesConsole


_BASE_DIR, _ = os.path.split(os.path.abspath(os.path.dirname(__file__)))
_UTIL_DIR = os.path.join(_BASE_DIR, "scripts")

class TestUtilitiesConsole(unittest.TestCase):
    """Test Case class for the Utilities Console"""

    def setUp(self):
        options = {
            'verbosity': False,
            'quiet': False,
            'width': 80,
            'utildir': _UTIL_DIR,
            'variables': [],
            'prompt': '>',
            'welcome': "",
            'goodbye': "",
            'commands': [],
            'custom': True,
            'hide_util': False,
            'add_util': []
        }
        self.util_con = UtilitiesConsole(options)

    def test_strange_keyboard_input(self):
        test_cases = {'R': "INSERT_KEY", 'I': 'PAGE_UP_KEY',
                      'Q': 'PAGE_DOWN_KEY'}

        for key in test_cases:
            self.assertEqual(_WIN_COMMAND_KEY.get(key), None)

    def test_backspace_beginning(self):
        """Test console response to BACKSPACE KEY when the cursor
        is at the beginning of the line.
        """

        test_cases = ['BACKSPACE_POSIX', 'BACKSPACE_WIN']
        self.util_con.cmd_line.command = "12345"
        self.util_con.cmd_line.length = 5
        self.util_con.cmd_line.position = 0
        for key in test_cases:
            self.util_con._process_command_keys(key)
            self.assertEqual("12345", self.util_con.cmd_line.command)

    def test_backspace_middle(self):
        """Test console response to BACKSPACE KEY when the cursor
        is in the middle of the line.
        """

        self.util_con.cmd_line.command = "12345"
        self.util_con.cmd_line.length = 5
        self.util_con.cmd_line.position = 3
        self.util_con._process_command_keys('BACKSPACE_POSIX')
        self.assertEqual("1245", self.util_con.cmd_line.command)
        self.util_con._process_command_keys('BACKSPACE_WIN')
        self.assertEqual("145", self.util_con.cmd_line.command)

    def test_backspace_end(self):
        """Test console response to BACKSPACE KEY when the cursor
        is in the end of the line.
        """

        self.util_con.cmd_line.command = "12345"
        self.util_con.cmd_line.length = 5
        self.util_con.cmd_line.position = 5
        self.util_con._process_command_keys('BACKSPACE_POSIX')
        self.assertEqual("1234", self.util_con.cmd_line.command)
        self.util_con._process_command_keys('BACKSPACE_WIN')
        self.assertEqual("123", self.util_con.cmd_line.command)

    def test_arrow_delete(self):
        """Test console response to using arrow keys and the
        DELETE KEY when the cursor is in the end of the line.
        """

        self.util_con.cmd_line.command = "12345-123"
        self.util_con.cmd_line.length = 9
        self.util_con.cmd_line.position = 9
        for i in range(0, 5):
            self.util_con._process_command_keys('ARROW_LT')
        self.assertEqual("12345-123", self.util_con.cmd_line.command)
        self.util_con._process_command_keys('ARROW_RT')
        self.assertEqual("12345-123", self.util_con.cmd_line.command)
        self.util_con._process_command_keys('DELETE_POSIX')
        self.assertEqual("12345123", self.util_con.cmd_line.command)
        self.assertEqual(5, self.util_con.cmd_line.position)
        self.assertEqual(8, self.util_con.cmd_line.length)
        self.util_con._process_command_keys('DELETE_POSIX')
        self.assertEqual("1234523", self.util_con.cmd_line.command)
        self.assertEqual(5, self.util_con.cmd_line.position)
        self.assertEqual(7, self.util_con.cmd_line.length)

    def test_home_key(self):
        """Test console response to HOME KEY.
        """
        self.util_con.cmd_line.command = "12345"
        self.util_con.cmd_line.length = 5
        for position in [0, 2, 5]:
            self.util_con.cmd_line.position = position
            self.util_con._process_command_keys('HOME')
            self.assertEqual("12345", self.util_con.cmd_line.command)
            self.assertEqual(5, self.util_con.cmd_line.length)
            self.assertEqual(0, self.util_con.cmd_line.position)

    def test_end_key(self):
        """Test console response to END KEY.
        """
        self.util_con.cmd_line.command = "12345"
        self.util_con.cmd_line.length = 5
        for position in [0, 2, 5]:
            self.util_con.cmd_line.position = position
            self.util_con._process_command_keys('END')
            self.assertEqual("12345", self.util_con.cmd_line.command)
            self.assertEqual(5, self.util_con.cmd_line.length)
            self.assertEqual(5, self.util_con.cmd_line.position)

    def test_quit_tab(self):
        """Test console response to Q+tab (should be 'quit').

        NOTICE: This test is designed to be executed from the base of the
        source tree. If you want to run it from elsewhere, you will need
        to change the 'utildir' variable below.

        """
        options = {
            'verbosity': False,
            'quiet': False,
            'width': 80,
            'utildir': "./scripts",
            'variables': [],
            'prompt': '>',
            'welcome': "",
            'goodbye': "",
            'commands': [],
            'custom': True,
            'hide_util': False,
            'add_util': []
        }
        util_con = UtilitiesConsole(options)
        stdout_backup = sys.stdout
        try:
            sys.stdout = open(os.devnull, 'w')
            test_cases = ["q", "Q"]
            for key in test_cases:
                util_con.cmd_line.command = ""
                util_con.cmd_line.add(key)
                util_con.do_command_tab("q")
                self.assertEqual(util_con.cmd_line.command, "{0}uit ".format(key))
        finally:
            sys.stdout = stdout_backup

if __name__ == '__main__':
    unittest.main()
