# -*- coding: utf-8 -*-
# send key in Windows OS
# Require win32api
#__author__ = 'mingl'

import sys
import time
import ctypes

class WindowsKeyboard:
    """Simulate Windows Keyboard"""

    def __init__(self):
        self.user32_dll = ctypes.WinDLL ("User32.dll")

    def _key_up_key_code(self, key_code):
        """
        Relaase key by key code
        :param key_code: (str) key code
        :return:
        """
        self.user32_dll.keybd_event(int(key_code),0x45, 0x1| 0x2, 0)
        # self.user32_dll.keybd_event(int(key_code), 0, 10, 0)

    def _key_down_key_code(self, key_code):
        """
        press down key by key code
        :param key_code: (str) key code
        :return:
        """
        self.user32_dll.keybd_event(int(key_code),0x45, 0x1 , 0);
        # self.user32_dll.keybd_event(int(key_code), 0, 8, 0)

    def _key_up_scan_code(self, scan_code):
        """
        Relaase key by scan code
        :param scan_code: (str) scan code
        :return:
        """
        if scan_code.startswith('-'):
            self.user32_dll.keybd_event(0, int(scan_code[1:]), 11, 0)
        else:
            self.user32_dll.keybd_event(0, int(scan_code), 10, 0)

    def get_key_state(self, scan_code):
        """
        Get lock key status
        :param scanCode: str scan code
        :return:
        """

        vk_code = self.user32_dll.MapVirtualKeyA(int(scan_code), 3)
        key_state = self.user32_dll.GetKeyState(vk_code)

        if key_state == 1:
            return True
        else:
            return False

    def toggle_lock_key(self,lock_key_scan_code_list, lock_key_on=True):
        """
        toggle lock key
        :param lock_key_scan_code_list: list,
        :param lock_key_on: boolean,
        :return:
        """
        if (not self.get_key_state(lock_key_scan_code_list[0]) and lock_key_on) \
                or (self.get_key_state(lock_key_scan_code_list[0]) and not lock_key_on):
            self.send_scan_code(lock_key_scan_code_list) #Press lock key if


    def _key_down_scan_code(self, scan_code):
        """
        Press down key by scan code
        :param scan_code: (str) scan code
        :return:
        """
        if scan_code.startswith('-'):
            self.user32_dll.keybd_event(0, int(scan_code[1:]), 9, 0)
        else:
            self.user32_dll.keybd_event(0, int(scan_code), 8, 0)

    def send_scan_code(self, scan_code_list):
        """
        Press key by scan code list
        :param scan_code_list: scan code list
        :return:
        """

        for scan_code in scan_code_list: #key down
            self._key_down_scan_code(scan_code)

        for i in range(len(scan_code_list)-1, -1, -1): #key up
            self._key_up_scan_code(scan_code_list[i])
        time.sleep(0.05)

    def send_key_code(self, key_code_list):
        """
        Press key by scan code list
        :param scan_code_list: scan code list
        :return:
        """
        for key_code in key_code_list: #key down
            self._key_down_key_code(key_code)

        for i in range(len(key_code_list)-1, -1, -1): #key up
            self._key_up_key_code(key_code_list[i])
        time.sleep(0.05)