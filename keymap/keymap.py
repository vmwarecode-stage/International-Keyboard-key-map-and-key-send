# -*- coding: utf-8 -*-
# Get key info from keymap.xml
# Require win32api
__author__ = 'mingl'

import os
import xml.etree.ElementTree as ET

class KeyMap:
    """Get Key info from keymap/keymap.xml"""

    def __init__(self):
        current_path= os.path.dirname(os.path.abspath('__file__'))
        if current_path.endswith('keymap'):
            keymap_file= os.path.join(current_path,'keymap.xml')
        else:
            keymap_file = os.path.join(current_path, 'keymap', 'keymap.xml')
        try:
            self.tree = ET.parse(keymap_file)
            self.root = self.tree.getroot()
        except:
            raise


    def display_key_info(self,language, key_name=''):
        """Get key code by language and key name

        return: dictionary, like {a:{windows_keycode:1,windows_scancode:1,linux_keycode:1, mac_keycode: 1}
        """
        try:
            print ('+' + '-' * 74 + "+")
            print('|{0:11s}|{1:16s}|{2:11s}|{3:10s}|{4:10s}|{5:12s}|'.format('Key Name'.center(11),
                                                                     'Type'.center(16),
                                                                     'WinScanCode'.center(11),
                                                                     'WinKeyCode'.center(10),
                                                                     'MacKeyCode'.center(10),
                                                                     'LinuxKeyCode'.center(12)))
            print ('+' + '-' * 74 + "+")

            xpath = './language[@name="%s"]' % language
            language_node = self.root.find(xpath)  # get language node
            for child in language_node:
                key_attribute_dict = dict.copy(child.attrib)  # get all attributes of key
                # key_attribute_dict.pop('windows_keycode') #remove type
                print('|{0:11s}|{1:16s}|{2:11s}|{3:10s}|{4:10s}|{5:12s}|'.format(key_attribute_dict['name'].center(11),
                                                                     key_attribute_dict['type'].center(16),
                                                                     key_attribute_dict['windows_scancode'].center(11),
                                                                     key_attribute_dict['windows_keycode'].center(10),
                                                                     key_attribute_dict['mac_keycode'].center(10),
                                                                     key_attribute_dict['linux_keycode'].center(12)))

            print ('+' + '-' * 74 + "+")
            print ('Note: Minus scan code means it need "extened bit".')
            print ('Refer to https://en.wikipedia.org/wiki/Keyboard_layout for key type definition.')
        except ET.ParseError as error_parse:
            print ("Parse XML file error:%s" + error_parse)
            raise

    def get_all_keys(self, language, type=''):
        """
        Get key code by language and key name
        :param language:
        :param type: str, mainpad, numpad, function, ''
        :return: return: dictionary, like {a: {windows_keycode:1,windows_scancode:1,linux_keycode:1, mac_keycode: 1},
                ...
                b: {windows_keycode:1,windows_scancode:1,linux_keycode:1, mac_keycode: 1}}
        """

        xpath = './language[@name="%s"]' % language # get all keys

        exp_dict = {}
        try:
            language_node = self.root.find(xpath) #get language node
            for child in language_node:
                append = False
                key_attribute_dict = dict.copy(child.attrib) #get all attributes of key
                if type.lower().startswith('character') and key_attribute_dict['type'] == 'characterkey':  # get main pad key only
                    append = True
                elif type.lower().startswith('numeric') and key_attribute_dict['type'] == 'numericpad': # get num pad keys only
                    append = True
                elif type.lower().startswith('systemkey') and key_attribute_dict['type'] == 'systemkey': # get num pad keys only
                    append = True
                elif type.lower().startswith('editkey') and key_attribute_dict['type'] == 'editkey': # get num pad keys only
                    append = True
                elif type.lower().startswith('modifierkey') and key_attribute_dict['type'] == 'modifierkey': # get num pad keys only
                    append = True
                elif type.lower().startswith('lockkey') and key_attribute_dict['type'] == 'lockkey': # get num pad keys only
                    append = True
                elif type.lower().startswith('functionkey') and key_attribute_dict['type'] == 'functionkey': # get num pad keys only
                    append = True
                elif type.lower().startswith('navigationkey') and key_attribute_dict['type'] == 'navigationkey': # get num pad keys only
                    append = True
                elif type.lower().startswith('nonprintable') and key_attribute_dict['type'] != 'characterkey'\
                        and key_attribute_dict['type'] != 'numericpad':  # get function keys only
                    append = True
                elif type == '':
                    append = True
                if append:
                    key_name = key_attribute_dict['name'] #get key name
                    key_attribute_dict.pop('name') #remove key name
                    key_attribute_dict.pop('type')  # remove type
                    exp_dict[key_name] = key_attribute_dict

            return exp_dict #sorted(exp_dict.iteritems(), key=lambda d:d[0])

        except ET.ParseError as error_parse:
            print ("Parse XML file error:%s" + error_parse)
            raise

#for debug only
if __name__ == '__main__':
    keymap = KeyMap();
    keymap.display_key_info("en-us","a");

    key = keymap.get_all_keys("en-us");
    print key