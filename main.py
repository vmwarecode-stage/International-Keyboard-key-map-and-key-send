# -*- coding: utf-8 -*-
# keyboard_scanner.py
# Added on 201401211 - kEVIN

import sys
import time

from keyboard.keyboard_linux import  *
from keyboard.keyboard_windows import  *
from keyboard.keyboard_mac import  *
from keymap.keymap import *


reload(sys)
sys.setdefaultencoding('utf-8')

HELP_INFO = '''Usage (version: 0.1):
-----------------
-KeyCode <language>
    Get key code:

    Languages: en-us, de-de, zh-cn, zh-tw, ja-jp, ko-kr, fr-fr

    Example:
        -keycode zh-cn
-----------------
-SendKeyCode <Key Code>
    Send key code to current active dialog in Windows,
    Mac and Linux OS:

    Example:
        -SendKeyCode "65 16+65"
            Send a and shift+a in Windows OS
-----------------
-SendScanCode <Scan Code>
    Send Scan code to current active dialog in Windows OS:

    Example:
        -SendScanCode "30 42+30"
            Send a and shift+a in Windows OS
-----------------
-SendKey <language> <Key Name> [EndKey=<key name>]
    Send key to current active dialog:

    Languages: en-us, de-de, zh-cn, zh-tw, ja-jp, ko-kr, fr-fr
    Key Name: Must be same with displayed name by command -KeyCode;
              combination keys joinwith + , multiple keys join with space.
              such as a, shift+a, "a b c shift+a"
    EndKey: Send keys after each key send, It's designed for eastern
            Asian IME, and nornally it's enter, or space or "space enter"

    Example:
        -Sendkey zh-cn "a shift+a" endkey=enter
        -Sendkey de-de "a shift+a"
-----------------
-SendKey <language> <Key Category> [LockKey=<lock keys>]
         [ModifierKey=<Modifier keyof combination key>] [EndKey=<key name>]
    Send keys by category to current active dialog:

    Languages: en-us, de-de, zh-cn, zh-tw, ja-jp, ko-kr, fr-fr
    Key Category*: Supported key categories: CharacterKey, Numericpad,
    LockKey: Supported lock Keys: numlock or capslock
    ModifierKey: Supported modifier keys: shift, altgr(Windows & Linux),
                 option(Mac),shift+option(Mac)
    EndKey: Send keys after each key send, It's designed for eastern
            Asian IME, and normally it's enter, or space or "space enter"

    Example:
        -TestKey zh-cn Numericpad lockkey=numlock
            (Send keys in numeric pad with Numlock on)
        -testkey zh-cn CharacterKey lockkey=Capslock ModifierKey=shift endkey=enter
            (send keys in main pad with shift and Capslock on)

    * Please refer to https://en.wikipedia.org/wiki/Keyboard_layout for key category definition
-----------------'''

SUPPORT_LANGUAGE_LIST = ['en-us', 'de-de', 'zh-cn', 'zh-tw',
                         'ja-jp', 'ko-kr', 'fr-fr']
OS_NAME = sys.platform



def send_key_code(key_code):
    """
    Set key code
    :param key_code: (str) key code
    :return:
    """
    message_before_input()
    print ('Send key code: %s' % (key_code))
    key_code_list = key_code.split(" ")
    for k in key_code_list:
        single_key_code = []
        keys_convert_plus = k.replace("+", "[+]")  # such as covert 'a+b++' to 'a[+]b[+][+]'
        keys_convert_plus = keys_convert_plus.replace("[+][+]", "[+]+")  # such as covert 'a[+]b[+][+]' to ''a[+]b[+]+''
        single_key_code = keys_convert_plus.split("[+]")  # split keys by [+]

        if len(single_key_code) > 0:
            # for mac os
            if OS_NAME == 'darwin':
                if len(single_key_code) == 2:
                    MacKeyboard().send_key_code(single_key_code[1], combo_key=single_key_code[0])
                elif len(single_key_code) == 1:
                    MacKeyboard().send_key_code(single_key_code[0])
            elif OS_NAME.startswith('linux'):
                LinuxKeyboard().send_key_code(single_key_code)
            elif OS_NAME == 'win32':
                WindowsKeyboard().send_key_code(single_key_code)
            else:
                print ("Curent OS doesn't support: %s" % OS_NAME)
                exit(-1)

def send_scan_code(scan_code):
    """
    Send scan code
    :param key_code: (str) key code
    :return:
    """
    message_before_input()

    print ('Send scan code: %s' % (scan_code))
    scan_code_list = scan_code.split(" ")
    for s in scan_code_list:
        keys_convert_plus = s.replace("+", "[+]")  # such as covert 'a+b++' to 'a[+]b[+][+]'
        keys_convert_plus = keys_convert_plus.replace("[+][+]", "[+]+")  # such as covert 'a[+]b[+][+]' to ''a[+]b[+]+''
        single_scan_code = keys_convert_plus.split("[+]")  # split keys by [+]

        if len(single_scan_code) > 0:
            # for mac os
            if OS_NAME == 'win32':
                WindowsKeyboard().send_scan_code(single_scan_code)
            else:
                print ("Curent OS doesn't support Send scan code: %s" % OS_NAME)
                exit(-1)


def get_key_list(keys, key_dictionary):
    """
    Get key code list by key name
    :param keys: (str) Key name
    :param key_dictionary: (dict) all key list
    :return:
    """

    keys_convert_plus = keys.replace("+", "[+]")  # such as covert 'a+b++' to 'a[+]b[+][+]'
    keys_convert_plus = keys_convert_plus.replace("[+][+]", "[+]+")  # such as covert 'a[+]b[+][+]' to ''a[+]b[+]+''
    keys_names = keys_convert_plus.split("[+]")  # split keys by [+]

    key_code_list = []
    try:
        #for mac os
        if OS_NAME == 'darwin':
            # need combine combo key to a string like "command down" or "{command down, option down}"
            combo_keys = ''
            for i in range(0,len(keys_names)-1,1):
                if combo_keys == '':
                    combo_keys = keys_names[i] + ' down'
                else:
                    combo_keys += ','+keys_names[i]+' down'

            if ',' in combo_keys:
                combo_keys = '{%s}'%combo_keys
            key_code_list.append(combo_keys)

            # covert key name to key code for normal key
            normal_ken_name = keys_names[len(keys_names)-1]
            key_code = key_dictionary[normal_ken_name]['mac_keycode']
            if key_code == ''or key_code.lower() == 'na':
                print ("Key code of key [%s] in [%s] OS is null: %s" % (normal_ken_name, OS_NAME))
                exit(-1)
            else:
                key_code_list.append(key_code)  # covert key name to key code

        else: #for windows and linux os
            for key in keys_names:
                key_code = ''
                if OS_NAME.startswith('linux'):
                    key_code = key_dictionary[key]['linux_keycode']
                elif OS_NAME == 'win32':
                    key_code = key_dictionary[key]['windows_scancode'] #get windows scan code firstly
                else:
                    print ("Curent OS doesn't support: %s" % OS_NAME)
                    exit(-1)
                if key_code == '':
                    print ("Key code of key [%s] in [%s] OS is null: %s" % (key,OS_NAME))
                    exit(-1)
                else:
                    key_code_list.append(key_code)  # covert key name to key code

        return key_code_list
    except:
        raise


def get_key_list_by_category(key_dictionary_type, key_dictionary_all, prefix_key=''):
    """
    Get key code list by catefory
    :param key_dictionary_type: (dict) key list by category
    :param key_dictionary_all: (dict) all key list
    :param prefix_key:
    :return:
    """

    key_list = []
    key_code_list = []
    key_name_list = []
    try:
        key_code_name = ""
        if OS_NAME == 'darwin':
            key_code_name = 'mac_keycode'
        elif OS_NAME.startswith('linux'):
            key_code_name = 'linux_keycode'
        elif OS_NAME == 'win32':
            key_code_name = 'windows_scancode'
        else:
            print ("Curent OS doesn't support: %s" % OS_NAME)
            exit(-1)

        for key in sorted(key_dictionary_type):
            key_code = key_dictionary_type[key][key_code_name]
            if key_code != '' and key_code.lower() != 'na':
                if prefix_key != '':
                    combo_key = get_key_list(prefix_key + "+" + key, key_dictionary_all)
                    key_code_list.append(combo_key)
                else:
                    key_code_list.append([key_code])
                key_name_list.append(key)

        key_list.append(key_name_list)
        key_list.append(key_code_list)
        return key_list
    except:
        raise


def send_key(language, key_name, end_key=''):
    """
    Send key
    :param language: (str)
    :param key_name: (str)
    :param end_key: str)
    :return:
    """

    try:
        message_before_input()

        print ("+" + "-" * 74 + "+")
        print ('Send key(s): %s' % key_name)
        keymap = KeyMap()
        key_dictionary_all = keymap.get_all_keys(language)

        end_key_code = get_end_key_list(end_key, key_dictionary_all) #get end key code

        key_list = key_name.split(' ') #split key name
        for k in key_list:
            key_code_list = get_key_list(k, key_dictionary_all) #get key code for each key
            send_key_code_list(key_code_list, end_key_code)
    except:
        raise


def send_key_code_list(key_code_list, end_key_list=[]):
    """
    Send key code list
    :param key_code_list: (list) Key code list
    :param enter_key_code: (list) enter key code list
    :return:
    """
    try:
            # os_name = sys.platform
            if len(key_code_list) > 0:
                #for mac os
                if OS_NAME == 'darwin':
                    if len(key_code_list) == 2:
                        MacKeyboard().send_key_code(key_code_list[1], combo_key=key_code_list[0])
                    elif len(key_code_list) == 1:
                        MacKeyboard().send_key_code(key_code_list[0])
                elif OS_NAME.startswith('linux'):
                    LinuxKeyboard().send_key_code(key_code_list)
                elif OS_NAME == 'win32':
                    WindowsKeyboard().send_scan_code(key_code_list)
                else:
                    print ("Curent OS doesn't support: %s" % OS_NAME)
                    exit(-1)

            if len(end_key_list) > 0 :
                for k in end_key_list:
                    if OS_NAME == 'darwin':
                        if len(k) == 2:
                            MacKeyboard().send_key_code(k[1], combo_key=k[0])
                        elif len(k) == 1:
                            MacKeyboard().send_key_code(k[0])
                    elif OS_NAME.startswith('linux'):
                        LinuxKeyboard().send_key_code(k)
                    elif OS_NAME == 'win32':
                        WindowsKeyboard().send_scan_code(k)
    except:
        raise


def test_key(language, category, end_key='', lock_key='', modifier_key=''):
    """
    Send non-function key by category
    :param language: str,
    :param category: (str) characterkey, numericpad
    :param end_key: enter, space
    :param lock_key:
    :param modifier_key:
    :return:
    """

    try:
        message_before_input()

        keymap = KeyMap()
        key_dictionary_all = keymap.get_all_keys(language)

        # turn on lock key key, numlock, caps lock,
        if lock_key != '':
            toggle_lock_key(lock_key,key_dictionary_all,lock_key_on=True)
            if OS_NAME == 'win32':
                if category.startswith('character'):
                    toggle_lock_key('capslock',key_dictionary_all,lock_key_on=False) #turn off capslock if test character keys without lockkey
                elif category.startswith('numeric'):
                    toggle_lock_key('numlock',key_dictionary_all,lock_key_on=False) #turn off numlock if test numeric keys without lockkey

        # send keys in main pad
        key_list_main = keymap.get_all_keys(language, type=category)
        keys_list = get_key_list_by_category(key_list_main, key_dictionary_all, modifier_key)
        print ('+' + '-' * 74 + "+")
        if lock_key != '':
            print ('Send keys with Setup key [%s]' % lock_key)

        if modifier_key!= '':
            print ('Send keys with %s in %s pad: %s' % (modifier_key, category, keys_list[0]))
        else:
            print ('Send keys in %s pad: %s' % (category, keys_list[0]))

        end_key_code = get_end_key_list(end_key, key_dictionary_all) #get end key code
        for key_code in keys_list[1]:
            send_key_code_list( key_code,end_key_code)

        # turn off lock key, numlock, caps lock,
        toggle_lock_key(lock_key,key_dictionary_all,lock_key_on=False)

    except:
        raise

def toggle_lock_key(lock_key,key_dictionary_all,lock_key_on=True):
    """
    Toggle lock key
    :param lock_key: str, lock key name
    :param key_dictionary_all: dict,
    :param lock_key_on: Boolean, turn on lock key
    :return:
    """

    if lock_key != '':
        lock_key_code = get_key_list(lock_key, key_dictionary_all)
        if OS_NAME == 'win32':
            WindowsKeyboard().toggle_lock_key(lock_key_code,lock_key_on)  # tourn on number lock
            if lock_key.lower()=='numlock':
                send_key_code_list(["-%s" % lock_key_code[0]])  # send num lock with extension bit for vm
        elif OS_NAME == 'darwin':
            if len(lock_key_code) == 2:
                MacKeyboard().send_key_code(lock_key_code[1], combo_key=lock_key_code[0])
            elif len(lock_key_code) == 1:
                MacKeyboard().send_key_code(lock_key_code[0])
        elif OS_NAME.startswith('linux'):
            LinuxKeyboard().send_key_code(lock_key_code)


def get_end_key_list(end_key, key_dictionary_all):
    """
    Get End Key code list
    :param end_key: str, a a+b, or "a b"
    :param key_dictionary_all:
    :return: [[],[]]
    """

    end_key_code = []
    if end_key != '':
        end_key_list = end_key.split(' ')
        for k in end_key_list:
            k_code_list = get_key_list(k, key_dictionary_all)  # get key code list for single end key
            end_key_code.append(k_code_list)
    return end_key_code


def message_before_input():
    print ("Please move Mouse focus to input application. Key will be sent in 5 seconds...")
    time.sleep(5)


def get_variables_by_name(name):
    """
    Get argument with format key=value
    :param name: key
    :return:
    """
    para_value = ''
    if not name.endswith('='):
        name += '='
    for s in sys.argv:
        if s.lower().startswith(name.lower()):
            para_value = s[s.find('=')+1:].lower().strip()
            break;
    return para_value

if __name__ == '__main__':
    ## for debug only
    # sys.argv = ["","-sendkeycode","20 65 161+65 20"]
    try:
        command = sys.argv[1].lower()
        if command == '-sendkeycode':
            key_code = sys.argv[2]
            send_key_code(key_code) # send keys in num pad

        elif command == '-sendscancode':
            scan_code = sys.argv[2]
            send_scan_code(scan_code) # send keys in num pad
        else:
            language = sys.argv[2].lower()

            if language not in SUPPORT_LANGUAGE_LIST:
                print ("Supported language list is %s" % SUPPORT_LANGUAGE_LIST) #check language is legal
                exit(-1)

            if command == "-keycode":
                if len(sys.argv) > 3:
                    print (HELP_INFO)
                    exit(-1)
                keymap = KeyMap()
                keymap.display_key_info(language)

            elif command=="-sendkey":

                key_category = sys.argv[3].lower()
                if key_category.startswith('character') or key_category.startswith('numeric') \
                        or key_category.startswith('systemkey') or key_category.startswith('editkey') \
                        or key_category.startswith('modifierkey') or key_category.startswith('lockkey') \
                        or key_category.startswith('functionkey') or key_category.startswith('navigationkey'):
                    if len(sys.argv) > 7:
                        print (HELP_INFO)
                        exit(-1)

                    lock_key = get_variables_by_name('LockKey')
                    modifier_key = get_variables_by_name('ModifierKey')
                    end_key = get_variables_by_name('EndKey')
                    test_key(language, key_category, end_key=end_key, lock_key=lock_key,
                             modifier_key=modifier_key)  # send keys in num pad

                else:
                    if len(sys.argv) > 5:
                        print (HELP_INFO)
                        exit(-1)

                    key_name = sys.argv[3].lower()
                    end_key = get_variables_by_name('EndKey')
                    send_key(language, key_name, end_key=end_key)
            else:
                print (HELP_INFO)
    except:
        print (HELP_INFO)
        raise