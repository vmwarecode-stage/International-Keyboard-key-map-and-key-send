-----------------------------------------
Run Environment Setup
-----------------------------------------
1. Install Python 2.7.x
2. Install necessary python module:
    a. Linux OS: need install virtkey, such as, use "sudo apt-get install python-virtkey" in Ubuntu.
    b. Mac OS: enable Accessibility from System Preference -> Security & Privacy

-----------------------------------------
Test Environment Setup
-----------------------------------------
1. Connect correct physical keyboard in host OS as requirement.
2. Set correct IME in local OS and client OS as requirement.
3. Open text editor in local OS or client OS as requirement.
4. Make sure Capslock and NumLock is off in Mac OS and Linux OS.

-----------------------------------------
Tool Execution
-----------------------------------------
1. Open  CMD/Terminal in local OS and go to project folder.
2 .Run command as below:
   python main.py <Argument...>

Argument:
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
