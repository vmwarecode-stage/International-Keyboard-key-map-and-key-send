# -*- coding: utf-8 -*-
# send key in Mac OS
# Require virtkey
#__author__ = 'Sophia'

import subprocess
import time


class MacKeyboard:
    """Simulate Mac Keyboard"""

    def send_key_code(self, key_code, combo_key=''):
        """
        Execute the command to input key or combo key pressing in an application
        key_code: the key_code of the key
        combo_key: the combo key(s) want to be pressed together with the key_code, following the format "command down" or "{command down, option down}"
        """
        if key_code != "":
            as_key_code = self._asquote(str(key_code))
            as_comboKey = combo_key

            if as_comboKey != "":
                s = '''
                    tell application "System Events" to key code {0} using {1}
                    '''.format(as_key_code, as_comboKey)
            else:
                s = '''
                    tell application "System Events" to key code {0}
                    '''.format(as_key_code)
            r = self._asrun(s)
            time.sleep(0.05)
            return r
        else:
            return ""

    # def get_key_state(self, script_name, modifier_key):
    #         #        as_script_name = self.asquote(str(script_name))
    #
    #         s = '''
    #             do shell script "{0} {1}"
    #             '''.format(script_name, modifier_key)
    #         print s
    #         r = self.asrun(s)
    #         print r
    #         return r

    def _asrun(self, ascript):
        """Run the given AppleScript and return the standard output and error."""

        osa = subprocess.Popen(['osascript', '-'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
        r = osa.communicate(ascript)[0]
        r = r.split('\n')[0]
        if r in ['1','true']:
            return True
        elif r in ['0','false']:
            return False
        else:
            return r

    def _asquote(self, astr):
        """Return the AppleScript equivalent of the given string."""

        astr = astr.replace('"', r'\"')
        return '"{}"'.format(astr)
