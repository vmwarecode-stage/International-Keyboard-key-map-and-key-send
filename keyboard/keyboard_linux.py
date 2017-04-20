# -*- coding: utf-8 -*-
# send key in Linux OS
# Require virtkey
#__author__ = 'EllenZhang'

import sys
import time


try:
    import virtkey
except:
    if sys.platform.startswith('linus'):
        raise


class LinuxKeyboard:
    """Simulate Linux Keyboard"""

    def _key_up(self, key_code):
        """
        Release key
        :param key_code: (string) key code
        :return:
        """
        virtkey.virtkey().release_keycode(int(key_code))

    def _key_down (self, key_code):
        """
        Press key down
        :param key_code: (string) key code
        :return:
        """
        virtkey.virtkey().press_keycode(int(key_code))

    def send_key_code(self, key_code_list):
        """
        press keys
        :param key_code_list: (List) list of key code
        :return:
        """
        for i in key_code_list: #key up
            if len(str(i)) > 0:
                self._key_down(i)
        for i in range(len(key_code_list)-1, -1, -1): #key down
            if len(str(key_code_list[i])) > 0:
                self._key_up(key_code_list[i])

        time.sleep(0.05)

    # def get_key_state_scan_code(self, key_code):
    #     key_state =  virtkey.virtkey().GetKeyState(key_code)
    #     return key_state