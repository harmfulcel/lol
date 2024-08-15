import hashlib
import json
from time import time
from random import randint, choice
import requests
from copy import deepcopy
from urllib.parse import quote
import os
from colorama import Fore, init  # Import colorama for coloring text

# Helper functions (no changes needed here)
def hex_string(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string

def RBIT(num):
    result = ''
    tmp_string = bin(num)[2:]
    while len(tmp_string) < 8:
        tmp_string = '0' + tmp_string
    for i in range(0, 8):
        result = result + tmp_string[7 - i]
    return int(result, 2)

def file_data(path):
    with open(path, 'rb') as f:
        result = f.read()
    return result

def reverse(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return int(tmp_string[1:] + tmp_string[:1], 16)

# XG class (no changes needed here)
class XG:
    def __init__(self, debug):
        self.length = 0x14
        self.debug = debug
        self.hex_CE0 = [0x05, 0x00, 0x50, choice(range(0, 0xFF)), 0x47, 0x1e, 0x00, choice(range(0, 0xFF)) & 0xf0]

    def addr_BA8(self):
        tmp = ''
        hex_BA8 = []
        for i in range(0x0, 0x100):
            hex_BA8.append(i)
        for i in range(0, 0x100):
            if i == 0:
                A = 0
            elif tmp:
                A = tmp
            else:
                A = hex_BA8[i - 1]
            B = self.hex_CE0[i % 0x8]
            if A == 0x05:
                if i != 1:
                    if tmp != 0x05:
                        A = 0
            C = A + i + B
            while C >= 0x100:
                C = C - 0x100
            if C < i:
                tmp = C
            else:
                tmp = ''
            D = hex_BA8[C]
            hex_BA8[i] = D
        return hex_BA8

    def initial(self, debug, hex_BA8):
        tmp_add = []
        tmp_hex = deepcopy(hex_BA8)
        for i in range(self.length):
            A = debug[i]
            if not tmp_add:
                B = 0
            else:
                B = tmp_add[-1]
            C = hex_BA8[i + 1] + B
            while C >= 0x100:
                C = C - 0x100
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            while E >= 0x100:
                E = E - 0x100
            F = tmp_hex[E]
            G = A ^ F
            debug[i] = G
        return debug

    def calculate(self, debug):
        for i in range(self.length):
            A = debug[i]
            B = reverse(A)
            C = debug[(i + 1) % self.length]
            D = B ^ C
            E = RBIT(D)
            F = E ^ self.length
            G = ~F
            while G < 0:
                G += 0x100000000
            H = int(hex(G)[-2:], 16)
            debug[i] = H
        return debug

    def main(self):
        result = ''
        for item in self.calculate(self.initial(self.debug, self.addr_BA8())):
            result = result + hex_string(item)

        return '8404{}{}{}{}{}'.format(hex_string(self.hex_CE0[7]), hex_string(self.hex_CE0[3]),
                                       hex_string(self.hex_CE0[1]), hex_string(self.hex_CE0[6]), result)

# X-Gorgon function (no changes needed here)
def X_Gorgon(param, data, cookie):
    gorgon = []
    ttime = time()
    Khronos = hex(int(ttime))[2:]
    url_md5 = hashlib.md5(bytearray(param, 'utf-8')).hexdigest()
    for i in range(0, 4):
        gorgon.append(int(url_md5[2 * i: 2 * i + 2], 16))
    if data:
        if isinstance(data, str):
            data = data.encode(encoding='utf-8')
        data_md5 = hashlib.md5(data).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(data_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    if cookie:
        cookie_md5 = hashlib.md5(bytearray(cookie, 'utf-8')).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(cookie_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    gorgon = gorgon + [0x1, 0x1, 0x2, 0x4]
    for i in range(0, 4):
        gorgon.append(int(Khronos[2 * i: 2 * i + 2], 16))
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}

# Function to get the stub (no changes needed here)
def get_stub(data):
    if isinstance(data, dict):
        data = json.dumps(data)

    if isinstance(data, str):
        data = data.encode(encoding='utf-8')
    if data is None or data == "" or len(data) == 0:
        return "00000000000000000000000000000000"

    m = hashlib.md5()
    m.update(data)
    res = m.hexdigest()
    res = res.upper()
    return res

# Function to retrieve TikTok profile (no changes needed here)
def get_profile(session_id, device_id, iid):
    """Retrieve the current TikTok username for a given session, device, and iid."""
    try:
        data = None
        parm = (
            f"device_id={device_id}&iid={iid}&id=kaa&version_code=34.0.0&language=en"
            "&app_name=lite&app_version=34.0.0&carrier_region=SA&tz_offset=10800&mcc_mnc=42001"
            "&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3"
            "&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone"
            "&device_type=iPhone13,4"
        )
        url = f"https://api16.tiktokv.com/aweme/v1/user/profile/self/?{parm}"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id}",
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; fewfwdw; Build/PI;tt-ok/3.12.13.1)",
        }
        response = requests.get(url, headers=headers, cookies={"sessionid": session_id})
        return response.json()["user"]["unique_id"]
    except Exception as e:
        return "None"

# Function to check if username has been changed (no changes needed here)
def check_is_changed(last_username, session_id, device_id, iid):
    """Check if the username has been changed in the TikTok profile."""
    return get_profile(session_id, device_id, iid) != last_username

# Function to change username (no changes needed here)
def change_username(session_id, device_id, iid, last_username, new_username):
    """Attempt to change a TikTok username."""
    data = f"aid=364225&unique_id={quote(new_username)}"
    parm = f"aid=364225&residence=&device_id={device_id}&version_name=1.1.0&os_version=17.4.1&iid={iid}&app_name=tiktok_snail&locale=en&ac=4G&sys_region=SA&version_code=1.1.0&channel=App%20Store&op_region=SA&os_api=18&device_brand=iPad&idfv=16045E07-1ED5-4350-9318-77A1469C0B89&device_platform=iPad&device_type=iPad13,4&carrier_region1=&tz_name=Asia/Riyadh&account_region=&tz_offset=10800"
    headers = {
        "Host": "api.tiktokv.com",
        "Connection": "keep-alive",
        "sdk-version": "2",
        "x-tt-token": "00000000000000000000000000000000",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "com.zhiliaoapp.musically/202100 (Linux; U; Android 8; en_US; samsung; SM-G930T; samsung; sm; en_US; tt-ok/1.1.0.0)",
        "Cookie": f"sessionid={session_id}",
        "Accept-Encoding": "gzip, deflate",
    }
    url = f"https://api.tiktokv.com/aweme/v1/commit/user/?{parm}"

    X_Gon = X_Gorgon(parm, data, f'sessionid={session_id}')
    response = requests.post(url, data=data, headers={**headers, **X_Gon})
    if check_is_changed(last_username, session_id, device_id, iid):
        return ""
    else:
        return f"Error has occurred. Details: {response.json()}"

# Initialize colorama
init(autoreset=True)

# ASCII Art with color
ascii_art = (
    Fore.LIGHTCYAN_EX + """
   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
  ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
  ▐░▌          ▐░▌       ▐░▌▐░▌▐░▌    ▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌          
  ▐░▌          ▐░▌       ▐░▌▐░▌ ▐░▌   ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌          ▐░▌     ▐░▌          
  ▐░▌          ▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌     ▐░▌          ▐░▌     ▐░▌          
  ▐░▌          ▐░▌       ▐░▌▐░▌   ▐░▌ ▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░▌          ▐░▌     ▐░▌          
  ▐░▌          ▐░▌       ▐░▌▐░▌    ▐░▌▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌          
  ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌      ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ 
  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
   ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
   
""" + Fore.WHITE + "                       To use this tool you need your TikTok Session ID. \n             Obtain your Session ID using " + Fore.LIGHTYELLOW_EX + "EditThisCookie (PC) " + Fore.WHITE + "or " + Fore.LIGHTYELLOW_EX + "Proxyman (iOS)" + Fore.RESET + """
   
""" + Fore.WHITE + "  Credits to: " + Fore.LIGHTRED_EX + "@vd_vd_vd" + Fore.WHITE + ", " + Fore.LIGHTGREEN_EX + "@ferrt17" + Fore.WHITE + " & " + Fore.LIGHTMAGENTA_EX + "@harbi" + Fore.WHITE + " on " + Fore.BLUE + "Discord" + Fore.RESET + "\n" +
      Fore.WHITE + "  For more updates join: " + Fore.CYAN + "discord.gg/conetic " +Fore.WHITE + "or " + Fore.CYAN + "t.me/olliescashouts" + Fore.RESET
)


# Function to clear the console
def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main function to handle user interaction and username change."""
    clear_console()
    print(ascii_art)

    # Ask for the session ID first
    session_id = input(Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + "+" + Fore.WHITE + "] " + "Session ID: " + Fore.LIGHTYELLOW_EX)

    device_id = str(randint(777777788, 999999999999))
    iid = str(randint(777777788, 999999999999))

    # Retrieve and display the current username
    user = get_profile(session_id, device_id, iid)
    if user != "None":
        print(Fore.WHITE + "  [" + Fore.LIGHTGREEN_EX + "+" + Fore.WHITE + "] " + "Current Username: " + Fore.LIGHTYELLOW_EX + f"{user}" + Fore.RESET)
    else:
        print(Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + "+" + Fore.WHITE + "] " + "Invalid session ID or other error.")
        return

    # Ask the user for "Redirect" or "User"
    mode = input(Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + "1" + Fore.WHITE + "] " + Fore.WHITE + "User Method " + Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + "2" + Fore.WHITE + "] " + Fore.WHITE + "Redirect Method " + Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + ">" + Fore.WHITE + "] " + Fore.WHITE + "Please enter a choice (1 or 2): " + Fore.LIGHTYELLOW_EX).strip().lower()

    if mode == "2":
        new_username = input(Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + "+" + Fore.WHITE + "] " + Fore.WHITE + "Please enter a new username (redirect method): " + Fore.LIGHTYELLOW_EX).strip()
        new_username = new_username.ljust(78) + "a"
    elif mode == "1":
        new_username = input(Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + "+" + Fore.WHITE + "] " + Fore.WHITE + "Please enter a new username (user method): " + Fore.LIGHTYELLOW_EX).strip()
    else:
        print(Fore.WHITE + "\n  [" + Fore.LIGHTGREEN_EX + "+" + Fore.WHITE + "] " + "Invalid mode selected. Please choose 'User' or 'Redirect'.")
        return

    # Change the username and print success message on the same line
    change_result = change_username(session_id, device_id, iid, user, new_username)
    print(Fore.LIGHTCYAN_EX + change_result + Fore.RESET)
    print(Fore.WHITE + "  [" + Fore.LIGHTGREEN_EX + "+" + Fore.WHITE + "] " + f"You have changed your username to: " + Fore.LIGHTYELLOW_EX + f"{new_username}")

if __name__ == "__main__":
    main()
